#!/usr/bin/env python3
#
# coding: utf-8

# Copyright (c) 2019-2020, NVIDIA CORPORATION.  All Rights Reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#



import os
import signal
# import socket
import urllib.request
import gi
import subprocess
import time
import threading, queue
import re
import sys
import traceback
import datetime
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib

import feedparser
import configparser
import yaml

import semver

import nvdsc
from nvdsc.tools.runner import DockerRunner
from nvdsc.tools.versions import VersionChecker
from nvdsc.tools.hardware import HWStats
from nvdsc.tools.payload_dialogs import PayloadDialog
from nvdsc.tools.license_dialogs import LicenseDialog




# print("script running under: " + pathlib.Path(__file__).parent.absolute())

PKG_DIR = str(pathlib.Path(__file__).parent.absolute())
# print(PKG_DIR)
HOME_DIR = os.environ['HOME']
config = configparser.ConfigParser()
# case-sensitive
config.optionxform = str
# config.read(HOME_DIR + 'config/config.ini')
config.read(PKG_DIR + '/config/config.ini')

# this is our app name 
APP_ID = config['MAIN']['APP_ID']
APP_DIR = HOME_DIR + "/.config" + '/' + APP_ID 

SETUP_SUCCEEDED_FILE = APP_DIR + '/' + config['MAIN']['SETUP_SUCCEEDED_FILE']
LICENSE_ACCEPTED_FILE = APP_DIR + '/' + config['MAIN']['LICENSE_ACCEPTED_FILE']
# APP_DIR = HOME_DIR + '/' + APP_ID 

img_pull_queue = queue.Queue()
try:
    os.stat(APP_DIR)
except:
    os.makedirs(APP_DIR)  

LOG_DIR = APP_DIR + '/' + config['MAIN']['LOG_DIR']
LOG_FILE = LOG_DIR + '/' + APP_ID + '.log'
LOG = logging.getLogger(APP_ID)
# LOG_FORMAT = config['MAIN']['LOG_FORMAT']
LOG_FORMAT = ('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')

try:
    os.stat(LOG_DIR)
except:
    os.mkdir(LOG_DIR)  

# logger.setLevel(logging.DEBUG)

# logging.basicConfig(filename = LOG_FILE, level=logging.DEBUG, format = LOG_FORMAT)
handler = TimedRotatingFileHandler(LOG_FILE, when="d", interval=int(config['MAIN']['LOG_ROLL_DAYS']), backupCount=int(config['MAIN']['LOG_BACKUPS']))
# logger.addHandler(handler)
logging.basicConfig(level=logging.DEBUG, format = LOG_FORMAT, handlers = [handler])

try:
    os.stat(SETUP_SUCCEEDED_FILE)
except:
    LOG.error("setup hasn't run, exiting")
    print("please run nvdsc-setup first")
    sys.exit(1)

# these will explode if not installed or if you are not on a laptop / desktop
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import GLib
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GObject
from gi.repository import GdkPixbuf

LICENSE = None

# with open (APP_DIR + "/LICENSE", "r") as lfile:
with open (PKG_DIR + "/LICENSE", "r") as lfile:  
    LICENSE = lfile.readlines()

# ICON_DEFAULT = os.path.abspath(APP_DIR + '/' + config['MAIN']['ICON_FILE'])
ICON_DEFAULT = os.path.abspath(PKG_DIR + "/" + config['MAIN']['ICON_FILE'])
# ICON_WARNING = 'dialog-warning'
ICON_WARNING = os.path.abspath(PKG_DIR + "/" + config['MAIN']['UPDATE_ICON_FILE']) 

VERSION_CHECK_INTERVAL = int(config['MAIN']['VERSION_CHECK_INTERVAL'])

RSS_FEED_URL = config['news']['RSS_FEED_URL']
MAX_ITEMS_IN_FEED = int(config['news']['MAX_ITEMS_IN_FEED'])
MAX_ITEM_TITLE_LEN = int(config['news']['MAX_ITEM_TITLE_LEN'])
MAX_ITEM_NOTIFICATIONS = int(config['news']['MAX_ITEM_NOTIFICATIONS'])
# in seconds
FEED_UPDATE_INTERVAL = int(config['news']['FEED_UPDATE_INTERVAL'])
NOTIFICATION_VISIBILITY_TIMEOUT_MS = int(config['news']['NOTIFICATION_VISIBILITY_TIMEOUT_MS'])
newest_item_timestamp = -1
notifs = []

DISPLAY_CONTAINER_INFO = config.getboolean('MAIN','DISPLAY_CONTAINER_INFO')

# this is supposed to be $HOME/.local/bin  except if there conda or venv
SCRIPT_DIR = ""
# the terms dialog window
# the idea is to prevent too many windows
about = None
child_procs = {}


GPUs = HWStats(config).get_gpus()

v = None
# moving this to main
# v = VersionChecker(config, SCRIPT_DIR)
# v.check_local()



# DSS_VER = "2.7.0"

LATEST_DSS_VER = config['MAIN']['LATEST_DSS_VERSION']

# DSS_UP_TO_DATE = False
# if semver.compare(v.local['dss'],config['MAIN']['LATEST_DSS_VERSION']) >= 0:
DSS_UP_TO_DATE = True

SPARK_PORT = "8080"

NVDSC_UP_TO_DATE = True
ALREADY_NOTIFIED_TO_UPGRADE = False
ALREADY_UPGRADED = False
# what happens when you click on the the menu item for the data science client?
NVDSC_MENU_ITEM_ACTION_HANDLER_ID = None

# what happens when you click on the the menu item for the data science stack?
DSS_MENU_ITEM_ACTION_HANDLER_ID = None


# should we disable notifications?

notify_disable = False
# we will be updating this periodically
# news_item = gtk.MenuItem.new_with_label('News' )
news_menu = gtk.Menu.new()
# sw_menu = gtk.Menu.new()
sw_menu_client = gtk.MenuItem()
sw_menu_stack = gtk.MenuItem()

def open_url(_,url):
#   cmd = ["/opt/google/chrome/chrome", url]
  cmd = ["/usr/bin/x-www-browser", url]
  subprocess.Popen(cmd)
#  subprocess.call(cmd)

def do_dss_cli(m):
  cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME']+"/data-science-stack", "--", "sh",  "-c", "./data-science-stack;bash"]
  subprocess.call(cmd)

def do_kaggle_cli(m):
  cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME'], "--", "sh",  "-c", "kaggle -v;bash"]
  subprocess.call(cmd)

def do_ngc_cli(m):
  cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME'], "--", "sh",  "-c", "ngc --version;bash"]
  subprocess.call(cmd)    


def do_aws_cli_wrapper(m,r):
  if do_aws_cli(m,r):
    LOG.debug("cli launched")
  else:
    LOG.error("could not launch CLI")
    show_dialog(gtk.MessageType.ERROR, 'Data Science Client', "AWS CLI failed to start. Please see logs", gtk.ButtonsType.OK,"Launch Error", None)
    
def do_aws_cli(m, r):
  # AWS CLI runs inside a container. So, does it exist?
  container_exists = False
  try:
    import docker
    client = r.docker.DockerClient()
    c = client.containers.get(config['MAIN']['AWS_CLI_CONTAINER_NAME'])
    num_tries = 0
    while c.status != 'running':
      if num_tries > 4:
        LOG.error("unable to start the container.")
        client.close()
        return False
      LOG.warning("the AWS CLI container exists but it is in non-running status " + c.status)
      LOG.debug("attempting to start... try " + str(num_tries))
      c.start()
      time.sleep(1)
      c.reload()
      num_tries = num_tries + 1

    client.close()
    container_exists =  True
  except docker.errors.NotFound:
    container_exists = False
  except docker.errors.APIError:
    LOG.warning("Unable to start AWS CLI: Docker API error")
    exc_type, exc_value, exc_tb = sys.exc_info()
    LOG.warning(traceback.format_exception(exc_type, exc_value, exc_tb))  
    return False
  except Exception:
    LOG.warning("Unable to start AWS CLI: Docker API error")
    exc_type, exc_value, exc_tb = sys.exc_info()
    LOG.warning(traceback.format_exception(exc_type, exc_value, exc_tb))  
    return False    
  
  
  if container_exists:
    cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME'], "--", "sh",  "-c", "docker attach " + config['MAIN']['AWS_CLI_CONTAINER_NAME']]
  else:
    mount_str = "-v " + os.environ['HOME'] + '/' + config['MAIN']['DEFAULT_DOCKER_SOURCE_MOUNT'] + ':' + config['MAIN']['DEFAULT_DOCKER_TARGET_MOUNT']

    cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME'], "--", "sh",  "-c", "docker run --name " + 
      config['MAIN']['AWS_CLI_CONTAINER_NAME'] + ' --entrypoint /bin/bash ' + mount_str + ' -ti ' + config['MAIN']['AWS_DOCKER_IMAGE'] + ' -c "aws;bash"']

  LOG.debug("aws docker cmd: " + ' '.join(cmd))
  subprocess.call(cmd)
  return True
  

def do_spyder(m):
    global child_procs
#    if m.get_active():
#      cmd = ["/bin/bash", "-c", "/home/dima/conda/envs/data-science-stack-2.7.0/bin/spyder &"]
    if 'spyder' in child_procs:
      LOG.info("spyder was previously launched. Checking to see if it's alive")
      if child_procs['spyder'].poll() is None:
        LOG.info("another process still running. No need to start a new one")
        return
      else:
        LOG.info("the old process died. Starting a new one.")
    else:
      LOG.info("starting a new spyder")
    child_procs['spyder'] = subprocess.Popen("/usr/bin/spyder3")
#    else:
#      LOG.debug("attempted murder of Spyder but we don't support it.  For obvious reasons.")
#      child_procs['spyder'].terminate()
#      cmd = ["pkill", "spyder"]

#    subprocess.call(cmd)

def do_code(m):
    global child_procs
    CODE_EXEC = "/snap/bin/code"
    # CODE_EXEC = "/usr/bin/code"
#    if m.get_active():
#      cmd = ["/bin/bash", "-c", "/snap/bin/code &"]
    if 'code' in child_procs:
      LOG.info("code was previously launched. Checking to see if it's alive")
      if child_procs['code'].poll() is None:
        LOG.info("another process still running. No need to start a new one")
        return
      else:
        LOG.info("the old process died. Starting a new one.")
    else:
      LOG.info("starting a new code")
    child_procs['code'] = subprocess.Popen(CODE_EXEC)
     # you can't just kill the process :(
#      child_procs['code'].kill()
#      cmd = ["pkill", "code"]
#      subprocess.call(cmd)


def disable_notification(self):
    global notify_disable
    notify_disable = self.get_active()
    if notify_disable and indicator.get_icon() == ICON_WARNING:
        clear_warning()

def do_upgrade_dss(m):
  global DSS_UP_TO_DATE
  LOG.info("do_upgrade_dss called")
  driver_before_upgrade = v.local['driver']
  DRIVER_VER_CHANGED = False

  dialog = PayloadDialog(title = "Nvidia Data Science Client", label = None, cmd = None)
  dialog.set_label("Upgrading DS Stack to ver " + LATEST_DSS_VER)
  dialog.set_icon_from_file(ICON_DEFAULT)
  release_label = gtk.Label()
  release_label.set_markup("<a href='https://github.com/NVIDIA/data-science-stack/releases'>Release notes</a>")
  release_label.show()
  dialog.get_content_area().add(release_label)
  response = dialog.run()
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    LOG.info("the user chose to cancel the DSS upgrade") 
    dialog.destroy()
    return
  LOG.info("do_upgrade_dss confirmed")
  dialog.set_label("DSS upgrade in progress")
  dialog.button2.hide()
  # need to put this into a conf file?
  # rc = os.system(SCRIPT_DIR + '/iudss.sh') + LATEST_DSS_VER
  # the last 1 is a flag to use pkexec
  dialog.set_cmd(SCRIPT_DIR + '/iudss.sh ' + LATEST_DSS_VER + " 1")
  response = dialog.run()

  if response == gtk.ResponseType.CANCEL:
    LOG.debug("user chose to cancel the upgrade while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.DELETE_EVENT:
    LOG.debug("user chose to close the dialog while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.NONE:
    LOG.debug("dss upgrade completed normally")

#   v.local['dss']
  
  v.check_driver_local()
  if driver_before_upgrade != v.local['driver']:
    DRIVER_VER_CHANGED = True
  
  # we are only updating the driver and the dss. No other versions should change.
  v.check_dss_local()
 

  out = dialog.get_cmd_out()
  err = dialog.get_cmd_err()
  rc = dialog.get_cmd_rc()
  if rc == 0:
      LOG.info("DS Stack Upgrade successful")
      if out is not None:
        LOG.debug("stdout: " + out)
      if err is not None:
        LOG.debug("stderr: " + err) 

      if v.local['dss'] == LATEST_DSS_VER:
        DSS_UP_TO_DATE = True
        GLib.idle_add(update_sw_menu_dss_item, sw_menu_stack, ' DS Stack: '+ v.local['dss'])
        # flip the icon to normal if nvdsc is up to date
        if NVDSC_UP_TO_DATE:
          indicator.set_icon(ICON_DEFAULT)
      else:
        DSS_UP_TO_DATE = False
        LOG.error("the dss upgrade script completed fine, but the DSS version did not change. weird.")

    
      dialog.set_label("DS Stack Upgrade successful")
      dialog.set_cmd(None)

      if DRIVER_VER_CHANGED:
        release_label.set_markup("The driver was updated. Please reboot")
      else:
        release_label.set_markup("No reboot required.")

      dialog.button1.hide() # the cancel button we don't need
      dialog.button2.show()
      dialog.run()
      dialog.destroy()
      

  else:
      LOG.error("dss upgrade failed with rc: " + str(rc))
      LOG.error("stdout: " + out)
      LOG.error("stderr: " + err)
      dialog.set_label("DS Stack Upgrade failed")
      dialog.set_cmd(None)
      release_label.set_markup("Please see logs.")
#      dialog.get_content_area().remove(release_label)
#      release_label.destroy()
      dialog.button1.hide() # the cancel button we don't need
      # dialog.button2 = dialog.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)
      dialog.button2.show()
      dialog.run()
      dialog.destroy()
      return  

def do_upgrade(m):
  global ALREADY_UPGRADED
  if ALREADY_UPGRADED:
    LOG.info("do_upgraded called but we already upgraded, so..")
    return


  dialog = PayloadDialog(title = "Nvidia Data Science Client", label = None, cmd = None)
  dialog.set_label("Upgrading to ver " + v.remote[APP_ID])
  dialog.set_icon_from_file(ICON_DEFAULT)
  release_label = gtk.Label()
  release_label.set_markup("<a href='https://github.com/NVIDIA/data-science-stack/releases'>Release notes</a>")
  release_label.show()
  dialog.get_content_area().add(release_label)
  response = dialog.run()
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    LOG.info("the user chose to cancel the upgrade") 
    dialog.destroy()
    return

  LOG.info("do_upgrade confirmed")
  dialog.set_label("Upgrade in progress")
  dialog.button2.hide()
  dialog.set_cmd(VersionChecker.PIP_NVDSC_UPGRADE_CMD)
  response = dialog.run()

  if response == gtk.ResponseType.CANCEL:
    LOG.debug("user chose to cancel the upgrade while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.DELETE_EVENT:
    LOG.debug("user chose to close the dialog while it was running")
    dialog.destroy()
    return

  if response == gtk.ResponseType.NONE:
    LOG.debug("upgrade completed normally")

  out = dialog.get_cmd_out()
#  if out is not None:
#    out = out.decode('utf-8')
  err = dialog.get_cmd_err()
#  if err is not None:
#    err = err.decode('utf-8')

  rc = dialog.get_cmd_rc()
  if rc == 0:
      LOG.info("Upgrade successful")
      if out is not None:
        LOG.debug("stdout: " + out)
      if err is not None:
        LOG.debug("stderr: " + err) 
      ALREADY_UPGRADED = True  
      dialog.destroy()     
      do_restart(m)
      # if we are here, the user did not want to restart yet. so, we just update the menu and chill
      GLib.idle_add(update_sw_menu_client_item, sw_menu_client, "restart")
      

  else:
      LOG.error("upgrade failed with rc: " + str(rc))
      LOG.error("stdout: " + out)
      LOG.error("stderr: " + err)
      dialog.set_label("Upgrade failed, please see logs")
      dialog.set_cmd(None)
      dialog.button1.hide() # the cancel button we don't need
      # dialog.button2 = dialog.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)
      dialog.button2.show()
      dialog.run()
      dialog.destroy()
      return

def do_restart(m):
  dialog = PayloadDialog(title = "Nvidia Data Science Client", label = None, cmd = None)
  dialog.set_label("Restart Client now?")
  dialog.set_icon_from_file(ICON_DEFAULT)
  response = dialog.run()
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    LOG.info("the user chose not to restart") 
    dialog.destroy()
    return

  LOG.info("do_restart confirmed")
  dialog.set_label("Restart in progress")
  dialog.button2.hide()
  dialog.set_cmd(v.get_nvdscd_start_cmd())
  response = dialog.run()

  if response == gtk.ResponseType.CANCEL:
    LOG.debug("user chose to cancel the restart while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.DELETE_EVENT:
    LOG.debug("user chose to close the dialog while it was running")
    dialog.destroy()
    return

  if response == gtk.ResponseType.NONE:
    LOG.debug("restart completed normally")

  out = dialog.get_cmd_out()
#  if out is not None:
#    out = out.decode('utf-8')
  err = dialog.get_cmd_err()
#  if err is not None:
#    err = err.decode('utf-8')
  rc = dialog.get_cmd_rc()
  if rc == 0:
    LOG.info("the new instance is running so exiting")
    dialog.destroy()
    quit(m)
  else:
    LOG.error("Failed to launch. Please restart manually")
    dialog.set_label("Restart failed. Please try manually")
    dialog.set_cmd(None)
    dialog.button1.hide() # the cancel button we don't need
    dialog.button2.show() # the ok button we need
  #   dialog.button2 = dialog.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)
    dialog.run()
    dialog.destroy()  


  if confirm_upgrade():
    LOG.info("do_upgrade confirmed")
    out,err, rc = v.update_nvdsc()
    if rc == 0:
      LOG.info("upgrade successful")
      LOG.debug("stdout: " + out)
      LOG.debug("stderr: " + err) 
      ALREADY_UPGRADED = True       
      do_restart(m)
      # if we are here, the user did not want to restart yet. so, we just update the menu and chill
      GLib.idle_add(update_sw_menu_client_item, sw_menu_client, "restart")

    else:
      LOG.error("upgrade failed with rc: " + str(rc))
      LOG.error("stdout: " + out)
      LOG.error("stderr: " + err)
  else:
    LOG.info("the user chose to cancel the upgrade")    


def warn_couldnt_restart(*args):
    dialog = gtk.MessageDialog(None, 0, gtk.MessageType.WARNING,
        gtk.ButtonsType.OK, "Please restart the client manually")
    dialog.set_title("Nvidia Data Science Client")
    dialog.format_secondary_text("Upgrading to " + v.remote[APP_ID] + " failed")
    dialog.set_icon_from_file(ICON_DEFAULT)
    response = dialog.run()
    dialog.destroy()
    return response == gtk.ResponseType.OK    


def confirm_upgrade(*args):
    dialog = gtk.MessageDialog(None, 0, gtk.MessageType.WARNING,
        gtk.ButtonsType.OK_CANCEL, "Upgrading to " + v.remote[APP_ID])
    dialog.set_title("Nvidia Data Science Client")
#    dialog.set_logo(icon)
    dialog.set_icon_from_file(ICON_DEFAULT)
    dialog.format_secondary_text("Are you sure?")
    response = dialog.run()
    dialog.destroy()
    return response == gtk.ResponseType.OK  



def confirm_restart(*args):
    dialog = gtk.MessageDialog(None, 0, gtk.MessageType.INFO,
        gtk.ButtonsType.OK_CANCEL, "Upgrade successful")
    dialog.set_title("Nvidia Data Science Client")
    dialog.set_icon_from_file(ICON_DEFAULT)
#    about.set_logo(icon)
    dialog.format_secondary_text("Would you like to restart now?")
    
    response = dialog.run()
    dialog.destroy()
    return response == gtk.ResponseType.OK 

def do_forced_ver_check(m):
  global NVDSC_UP_TO_DATE
  dialog = PayloadDialog(title = "Nvidia Data Science Client", label = None, cmd = None)
  dialog.set_label("Check for updates?")
  dialog.set_icon_from_file(ICON_DEFAULT)
  response = dialog.run()
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    LOG.info("the user canceled a forced version check") 
    dialog.destroy()
    return
  dialog.set_label("Checking for updates")
  # dialog.button2.destroy()
#  dialog.button2.hide()
  dialog.destroy_ok_button()
  dialog.set_cmd(VersionChecker.PIP_VER_CHECK_CMD)
  response = dialog.run()

  if response == gtk.ResponseType.CANCEL:
    LOG.debug("user chose to cancel the workload while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.DELETE_EVENT:
    LOG.debug("user chose to close the dialog")
    dialog.destroy()
    return

  if response == gtk.ResponseType.NONE:
    LOG.debug("workload completed normally")

  out = dialog.get_cmd_out()
  err = dialog.get_cmd_err()
  if err is not None:
    LOG.debug(" err: " +  err)
#    LOG.debug(" err: " +  err.decode('utf-8'))
#   LOG.debug("pip out: " + out.decode('utf-8') + " err: " +  err.decode('utf-8'))
  new_ver = check_ver_dyn(v, out)
  if new_ver is not None:
    LOG.warning("new version detected: " + new_ver)
    NVDSC_UP_TO_DATE = False
    indicator.set_icon(ICON_WARNING)
    GLib.idle_add(update_sw_menu_client_item, sw_menu_client, "upgrade")
#       notify_upgrade()
    
  else:
    NVDSC_UP_TO_DATE = True 
    dialog.set_label("No upgrades available")
    dialog.set_cmd(None)
    # dialog.button1.destroy() # the cancel button we don't need
    # dialog.button1.hide()
    dialog.destroy_cancel_button()
    dialog.button2 = dialog.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)
    #dialog.button2.show()
    dialog.run()
    dialog.destroy()
    return
#    show_noupgrades()

  # upgrade
  dialog.destroy()
  do_upgrade(m)

def check_ver_dyn(versions, out):  
    LOG.info('version check running')
    versions.parse_pip_output(out)
    if APP_ID in versions.remote:
      if semver.compare(nvdsc.__version__, versions.remote[APP_ID]) >=0:
        LOG.info("up to date: local: " + nvdsc.__version__ + ", remote: " + versions.remote[APP_ID])
        return None
      else:
        LOG.info("NOT up to date: local: " + nvdsc.__version__ + ", remote: " + versions.remote[APP_ID])
        return versions.remote[APP_ID]
    else:
      LOG.info(APP_ID + ' not in list of obsolete packages')
      return None
        

def show_dialog(type, title, sec_txt, btn_type, primary_txt, buttons):
  dialog = gtk.MessageDialog(None, 0, type,
        btn_type, primary_txt)
  dialog.set_title(title)
  dialog.format_secondary_markup(sec_txt)
  dialog.set_icon_from_file(ICON_DEFAULT)
  if buttons is not None:
    for k,v in buttons.items():
      dialog.add_buttons(k,v)
  response = dialog.run()
  dialog.destroy()
  return response == gtk.ResponseType.OK  

def show_info_dialog(type, title, sec_txt, btn_type, primary_txt, license_url):
  dialog = gtk.MessageDialog(None, 0, type,
        btn_type, primary_txt)
  dialog.set_title(title)
  dialog.format_secondary_text(sec_txt)
  dialog.set_icon_from_file(ICON_DEFAULT)
  label = gtk.Label()
  label.set_markup('By launching, you accept the <a href="' + license_url + '">License Agreement</a>')
  label.show()
  vbox = dialog.get_message_area()
  vbox.set_spacing(4)
  vbox.pack_end(label, True, True, 0)
  response = dialog.run()
  dialog.destroy()
  return response == gtk.ResponseType.OK   

def do_about(_):
  global about
  
  if about is not None:
    return

  about = gtk.AboutDialog()
  about.set_program_name("Nvidia Data Science Client")
  about.set_version("ver: " + nvdsc.__version__)
  about.set_icon_from_file(ICON_DEFAULT)
  about.set_resizable(True)
  icon = GdkPixbuf.Pixbuf.new_from_file(ICON_DEFAULT)
#  GdkPixbuf *example_logo = gdk_pixbuf_new_from_file ("./logo.png", NULL);
  about.set_logo(icon)
#  about.set_authors("Nvidia Corp.")
  about.set_copyright("(c) Nvidia")
  about.set_comments("Driver: " + v.local['driver'] + "\nCUDA: " + v.local['cuda'] + "\nDocker: " + v.local['docker'] + "\nNvidia Container Toolkit: " + v.local['nvdocker'] + 
   "\nNGC CLI: " + v.local['ngc'] + "\nKaggle CLI: " + v.local['kaggle'] + "\nAWS CLI: " + v.local['aws'] + 
   "\nData Science Stack: " + v.local['dss'])
##  about.set_comments('Man said, "Collect additional data." (Isaac Asimov)')
#  about.set_license_type(gtk.License.GPL_3_0)
  about.set_license(' '.join(LICENSE))
#   about.present()
#  about.set_website("https://forums.developer.nvidia.com/t/data-science-client/174270")
  about.set_website(config['links']['Forums'])
  about.set_website_label("Forums")
  
  about.present()
  about.run()
  about.destroy()
  about = None


def quit_warn(m):
  if not show_dialog(gtk.MessageType.INFO, 'Nvidia Data Science Client', "All running containers will be removed", gtk.ButtonsType.OK_CANCEL,"Quitting", None):
    LOG.debug('the user chose not to quit')
    return

  quit(m)

def quit(_):
  LOG.debug("exiting")
#  subprocess.call(["xhost", "-local:"])
  subprocess.run(["xhost", "-local:"], stdout=subprocess.PIPE)
  DockerRunner.stop_all()
  global notifs
  for n in notifs:
    LOG.debug("removing " + n.props.summary +  " " + str(n.props.closed_reason))
    notifs.remove(n)
  notify.uninit()
  gtk.main_quit()
  LOG.debug("after gtk quit")
  sys.exit(0)


def async_docker_stoprm(m, runner, ydict):
  runner.stop(ydict)
  m._browser_port = None
  m._ports = None
  m._container_launched = False

def async_docker_run(m, runner, ydict):
  if runner.run(ydict):
    LOG.debug("the container successfully launched.")
    if ydict['browser'] == 'y':
      c = runner.running_cs[ydict['container_name']]
      p = c.attrs['NetworkSettings']['Ports']
      LOG.debug("network settings of the new container: " + str(p))
      # we used to be mapping the first listed port 
#      internal_port = list(ydict['ports'].keys())[0]
      browser_port = ydict['browser_port']
      LOG.debug("the internal port is: " + browser_port)
      # we are assuming that these containers have only one port exposed; or if the have multiple, it is the first one listed that is mapped to the browser. So,
      # >>> c.attrs['NetworkSettings']['Ports']
      # {'6006/tcp': None, '6064/tcp': None, '8888/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '49154'}]}    
      bp = p[browser_port][0]['HostPort']
      m._ports = {}
      for pk in p.keys():
        pv = p[pk]
        if pv is not None:
          m._ports[pk] = pv[0]['HostIp'] + ':' + pv[0]['HostPort']

      LOG.debug("docker assigned random port " + bp)
      m._volumes = c.attrs['Mounts']
      # the runner has made sure the container is up. But, is the port ready?
 #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      ntries = 0
      clen = 0
#      while s.connect_ex(("127.0.0.1", int(bp))) != 0:
#        time.sleep(0.1)
#        ntries = ntries + 1
#        if ntries > 200:
#          raise Exception("timed out while waiting for container port to become available")
#      s.close()
      while clen == 0:
        try:
          with urllib.request.urlopen("http://localhost:" + bp + "/lab") as response:
            html = response.read()
            clen = len(html)
            if clen > 100:
              break
        except Exception:
          LOG.debug("connection refused")
        ntries = ntries + 1
        if ntries > 200:
          break
        time.sleep(0.1)

      if clen == 0:
        # the container came up, but the port is not working.. hmm
        LOG.error("launched container, but the port never became available")
        show_dialog(gtk.MessageType.ERROR, 'Data Science Client', "docker container failed to start. Please see logs", gtk.ButtonsType.OK,"Launch Error", None)
        m._container_launched = False
        m._browser_port = None
        m.set_active(False)  
        # clean up
        runner.stop(ydict)   
        return   

      open_url(m, "http://localhost:" + bp + "/lab")
      m._browser_port = bp
    m._container_launched = True
    
  else:
    LOG.error("could not launch container")
    show_dialog(gtk.MessageType.ERROR, 'Data Science Client', "docker container failed to start. Please see logs", gtk.ButtonsType.OK,"Launch Error", None)
    m._container_launched = False
    m._browser_port = None
    m.set_active(False)



def do_d(m, conf, ydict):
  runner = DockerRunner(conf)
  if m.get_active():
    if m._container_launched: # already running?
      LOG.debug("active clicked but the container is already launched")
      return

    if DISPLAY_CONTAINER_INFO:
      if not show_info_dialog(gtk.MessageType.INFO, 'Nvidia Data Science Client', ydict['description'], gtk.ButtonsType.OK_CANCEL,"Launching " + ydict['name'], ydict['license_url']):
        LOG.debug('the user chose not to launch')
        m._container_launched = False
        m.set_active(False)
        return
    GLib.idle_add(async_docker_run, m, runner, ydict)

  else:
    if not m._container_launched: # already not running?
      LOG.debug("de-activate clicked but the container is not running")
      return
    vstr = ""
    if hasattr(m, '_volumes') and m._volumes is not None:
      # m._volumes = c.attr['Mounts']
      # [{'Type': 'bind', 'Source': '/home/dima/data', 'Destination': '/workspace/data', 'Mode': 'rw', 'RW': True, 'Propagation': 'rprivate'}]
      for v in m._volumes:
        if v['Type'] != 'bind':
          continue

        if vstr == "":
          vstr = "Mounted volumes:\n"
        vstr = vstr + v['Destination'] + "\t" + v['Source'] + "\n"
    pstr = "" 
    if hasattr(m, '_ports') and m._ports is not None:
      for pk in m._ports.keys():
        pv = m._ports[pk]
        # 0.0.0.0:49154
        if pstr == "":
          pstr = "Exposed Ports:\n"
        pstr = pstr + pk + "\t" + "<a href = 'http://localhost:" + pv.split(':')[1] + "'>" + pv + "</a>" + "\n"
    buttons = {}
    buttons[gtk.STOCK_CANCEL] = gtk.ResponseType.CANCEL
    buttons['STOP AND REMOVE'] = gtk.ResponseType.OK
    
    if not show_dialog(gtk.MessageType.INFO, 'Nvidia Data Science Client', pstr + vstr, gtk.ButtonsType.NONE, ydict['name'] + " is running", buttons):
      LOG.debug('the user chose not to stop')
      m.set_active(True)
      return
    GLib.idle_add(async_docker_stoprm, m, runner, ydict)

def build_menu(config):
    global newest_item_timestamp
    global NVDSC_MENU_ITEM_ACTION_HANDLER_ID
    global DSS_MENU_ITEM_ACTION_HANDLER_ID
    global img_pull_queue
    runner = DockerRunner(config)

    menus_fname = PKG_DIR + "/" + config['MAIN']['MENUS_YAML']
#    menus_fname = APP_DIR + '/' + config['MAIN']['MENUS_YAML']
    
    try:
      ymenus = yaml.load(open(menus_fname, 'r'), Loader=yaml.SafeLoader) 
    except FileNotFoundError:
      LOG.error("menus file not found " + menus_fname)

    menu = gtk.Menu()

    item = gtk.MenuItem.new_with_label('Tools' )

    m = gtk.Menu.new()

    ji = gtk.MenuItem.new_with_label(' Jupyter')
    jupyters = ymenus['jupyter']

    
    jm = gtk.Menu.new()
    
    for j in jupyters:

      if config['MAIN']['REMOVE_CONTAINERS_ON_STARTUP'] == 'True':
        runner.remove_container_if_exists(j['container_name'])
      
      if runner.img_pulled(j['image']):
        i = gtk.CheckMenuItem(label = '  ' + j['name'])
        i._container_launched = False
        i.connect('activate', do_d, config, j)
      else:
        i = gtk.MenuItem(label = '  ' + j['name'] + " [pulling]")
        fj = yaml.dump(j)
        img_pull_queue.put({i,fj})
      jm.append(i)


    ji.set_submenu(jm)
    m.append(ji)
 
    item_code = gtk.MenuItem(label = ' VS Code')
    item_code.connect('activate', do_code)
    m.append(item_code)

    item_spyder = gtk.MenuItem(label = ' Spyder')
    item_spyder.connect('activate', do_spyder)
    m.append(item_spyder)

    cli_menu_item = gtk.MenuItem(label = 'CLI')
    m.append(cli_menu_item)
    cli_menu = gtk.Menu.new()
    cli_menu_item.set_submenu(cli_menu)
    

    item_dss_cli = gtk.MenuItem(label = ' DSS')
    item_dss_cli.connect('activate', do_dss_cli)
    cli_menu.append(item_dss_cli)

    item_ngc_cli = gtk.MenuItem(label = ' NGC')
    item_ngc_cli.connect('activate', do_ngc_cli)
    cli_menu.append(item_ngc_cli)

    item_kaggle_cli = gtk.MenuItem(label = ' Kaggle')
    item_kaggle_cli.connect('activate', do_kaggle_cli)    
    cli_menu.append(item_kaggle_cli)

    item_aws_cli = gtk.MenuItem(label = ' AWS')
    item_aws_cli.connect('activate', do_aws_cli_wrapper, runner)    
    cli_menu.append(item_aws_cli)    

#  #  m.append(cli_menu)

#     item_spark = gtk.CheckMenuItem(label = ' Spark')
#     item_spark.connect('activate', do_spark)
#     m.append(item_spark)

    item.set_submenu(m)
    menu.append(item)

    item = gtk.MenuItem.new_with_label('Demos' )
    m = gtk.Menu.new()
    demos = ymenus['demos']
    for j in demos:
      if runner.img_pulled(j['image']):
        i = gtk.CheckMenuItem(label = '  ' + j['name'])
        i._container_launched = False
        i.connect('activate', do_d, config, j)
      else:
        i = gtk.MenuItem(label = '  ' + j['name'] + " [pulling]")
        fj = yaml.dump(j)
        img_pull_queue.put({i,fj})
      m.append(i)




    item.set_submenu(m)
    menu.append(item)


#     menu.append(gtk.SeparatorMenuItem())
    item = gtk.MenuItem.new_with_label('Links' )
    m = gtk.Menu.new()

    for name in config['links']:
      i = gtk.MenuItem.new_with_label(' ' + name)
      u = config['links'][name]
      i.connect('activate', open_url, u)
      m.append(i)

    item.set_submenu(m)
    menu.append(item)

    menu.append(gtk.SeparatorMenuItem())
# this is defined globally
    item = gtk.MenuItem.new_with_label('News' )
#    m = gtk.Menu.new()
    feed = feedparser.parse(RSS_FEED_URL)
    pubdate = feed['entries'][0].published
    pubDate = "-".join(pubdate.split()[1:5])
#    newest_item_timestamp = datetime.datetime.strptime(pubDate , "%d-%b-%Y-%H:%M:%S").timestamp()

    try:
      for i in range(MAX_ITEMS_IN_FEED):
        title = feed['entries'][i]['title'][:MAX_ITEM_TITLE_LEN]
        href = feed['entries'][i]['link']
        item_news = gtk.MenuItem(label = ' ' + title)
        item_news.connect('activate', open_url, href)
        news_menu.append(item_news)
    except:
      LOG.error("RSS Connection error")
      LOG.error("RSS Unexpected error:" + sys.exc_info()[0])

    item.set_submenu(news_menu)
    menu.append(item)

    item = gtk.MenuItem.new_with_label('Hardware')
    m1 = gtk.Menu.new()
    item1 = gtk.MenuItem.new_with_label(' GPU (' + str(len(GPUs)) + ')' )
    m = gtk.Menu.new()
    for g in GPUs:
      i = gtk.MenuItem.new_with_label('  ' + g)
      m.append(i)

    item1.set_submenu(m)
    m1.append(item1)
    item.set_submenu(m1)
    menu.append(item)

#    menu.append(gtk.SeparatorMenuItem())
    item = gtk.MenuItem.new_with_label('Software')
    sw_menu = gtk.Menu.new()

    # sw_menu_client is externally defined
    if NVDSC_UP_TO_DATE:
#      sw_menu_client = gtk.MenuItem.new_with_label(' DS Client: '+ nvdsc.__version__)
      sw_menu_client.set_label(' DS Client: '+ nvdsc.__version__)
      NVDSC_MENU_ITEM_ACTION_HANDLER_ID = sw_menu_client.connect('activate', do_forced_ver_check)
    else:
#      sw_menu_client = gtk.MenuItem.new_with_label(' Upgrade Client to: '+ v.remote[APP_ID])
      sw_menu_client.set_label(' Upgrade Client to: '+ v.remote[APP_ID])
      NVDSC_MENU_ITEM_ACTION_HANDLER_ID = sw_menu_client.connect('activate', do_upgrade)
    sw_menu.append(sw_menu_client)

    # sw_menu_stack is externally defined
    # there is no need to check for the latest remote DSS version in a loop or on demand because we read it from the config file
    if DSS_UP_TO_DATE:
#      sw_menu_stack = gtk.MenuItem.new_with_label(' DS Stack: '+ v.local['dss'])
      sw_menu_stack.set_label(' DS Stack: '+ v.local['dss'])
      # disable this check. we want to control this by the version of the client.
#      DSS_MENU_ITEM_ACTION_HANDLER_ID = i.connect('activate', do_forced_ver_check_dss)
    else:
#      sw_menu_stack = gtk.MenuItem.new_with_label(' Upgrade Stack to: '+ LATEST_DSS_VER)
      sw_menu_stack.set_label(' Upgrade Stack to: '+ LATEST_DSS_VER)
      DSS_MENU_ITEM_ACTION_HANDLER_ID = sw_menu_stack.connect('activate', do_upgrade_dss)  
    sw_menu.append(sw_menu_stack)

    item.set_submenu(sw_menu)
    menu.append(item)

    i = gtk.MenuItem.new_with_label('About')
    i.connect('activate', do_about)
    menu.append(i)

    menu.append(gtk.SeparatorMenuItem())
    item_quit = gtk.MenuItem.new_with_label('Quit')
    item_quit.connect('activate', quit_warn)
    menu.append(item_quit)

    menu.show_all()
    return menu    


def notify_upgrade_dss():
    if notify_disable:
      return

    indicator.set_icon(ICON_WARNING)
    warning_dss.update("DS Stack version " + LATEST_DSS_VER + " available")
    warning_dss.add_action('default', 'Action', do_notify_upgrade_dss)
    warning_dss.show()


def notify_upgrade():
    global ALREADY_NOTIFIED_TO_UPGRADE
    if notify_disable:
      return

    if ALREADY_NOTIFIED_TO_UPGRADE:
      return 

    indicator.set_icon(ICON_WARNING)
#     warning.update("DSS version " + LATEST_DSS_VER + " available")
    warning.update("Nvidia Data Science Client version " + v.remote[APP_ID] + " available")
    warning.add_action('default', 'Action', do_notify_upgrade)
    warning.show()
    ALREADY_NOTIFIED_TO_UPGRADE = True

def do_notify_upgrade(x,y):
  return do_upgrade(x)

def do_notify_upgrade_dss(x,y):
  return do_upgrade_dss(x)  

def action_open_url(a,b,c):
  global notifs
  # this notification will become invisible, so remove it
  notifs.remove(a)
  LOG.debug("length of remaining notifs: " + str(len(notifs)))
  open_url(b,c)


def do_notify_rss_item(title, desc, href):
    global notifs
    if notify_disable:
      return

    info = notify.Notification.new(title, None)
    info.set_timeout(NOTIFICATION_VISIBILITY_TIMEOUT_MS)

    info.add_action('default', 'Action', action_open_url, href)

    info.show()
    notifs.append(info)




def wait_event(queue, event):
    while True:
        queue.put(event.wait_event())


def clean_notifs():
  global notifs
  # do some cleaning just in case we have exceeded the limit that the desktop has and some have become invisible
  LOG.debug("clean notifs running.. notifs: " + str(len(notifs)))
  for n in notifs:
    if n.props.closed_reason > -1:
      LOG.debug("removing " + n.props.summary +  " " + str(n.props.closed_reason))
      notifs.remove(n)

def nu(n_menu):
    i1 = 0
    # we'll overwrite it below
    global newest_item_timestamp
    
 
    while True:
      time.sleep(FEED_UPDATE_INTERVAL)
      i1 = i1 + 1
      LOG.debug("updater run " + str(i1))
      try: 
        feed = feedparser.parse(RSS_FEED_URL)
      except Exception:
        log.warning("unable to parse feed")
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.warning(traceback.format_exception(exc_type, exc_value, exc_tb)) 
        continue

      # we assume that the first item in the feed is the newest
      pubdate = feed['entries'][0].published
      pubDate = "-".join(pubdate.split()[1:5])
      n0 = datetime.datetime.strptime(pubDate , "%d-%b-%Y-%H:%M:%S").timestamp()      
      titles = []
      hrefs = []
#      print(n)
#      print(newest_item_timestamp)
      if n0 > newest_item_timestamp:
        LOG.debug("new news items detected!")          
#      if True:
        
        # the most recent item goes on top
        for i in reversed(range(MAX_ITEMS_IN_FEED)):
          pubdate = feed['entries'][0].published
          pubDate = "-".join(pubdate.split()[1:5])
          n = datetime.datetime.strptime(pubDate , "%d-%b-%Y-%H:%M:%S").timestamp()
          if n > newest_item_timestamp:
            titles.append(feed['entries'][i]['title'][:MAX_ITEM_TITLE_LEN])
#            description.append(feed['description'][i]['link'])
            hrefs.append(feed['entries'][i]['link'])

#            time.sleep(2)

        newest_item_timestamp = n0
        LOG.debug("adding " + str(len(titles)) + " new items to menu")

        # notifications
        # the most recent item goes last (on top)
        for i in range(len(titles) - MAX_ITEM_NOTIFICATIONS, len(titles)):
            do_notify_rss_item(titles[i], None, hrefs[i])


        GLib.idle_add(update_menu, n_menu, titles, hrefs)

      clean_notifs()

def update_sw_menu_dss_item(dss_item, msg):
  global DSS_MENU_ITEM_ACTION_HANDLER_ID
  LOG.debug("update_sw_menu_dss_item is called with: " + msg)
  # there is only one operation here, the normal
  dss_item.set_label(msg)
  dss_item.disconnect(DSS_MENU_ITEM_ACTION_HANDLER_ID)

def update_sw_menu_client_item(nvdsc_item, msg):
  global NVDSC_MENU_ITEM_ACTION_HANDLER_ID
  LOG.debug("update_sw_menu_client_item is called with: " + msg)
  if msg == "upgrade":
    nvdsc_item.set_label(' Upgrade to: ' + v.remote[APP_ID])
    if NVDSC_MENU_ITEM_ACTION_HANDLER_ID is not None:
      nvdsc_item.disconnect(NVDSC_MENU_ITEM_ACTION_HANDLER_ID)
    NVDSC_MENU_ITEM_ACTION_HANDLER_ID = nvdsc_item.connect('activate', do_upgrade)
  else: # restart
    nvdsc_item.set_label(' Restart required')
    if NVDSC_MENU_ITEM_ACTION_HANDLER_ID is not None:
      nvdsc_item.disconnect(NVDSC_MENU_ITEM_ACTION_HANDLER_ID)
    NVDSC_MENU_ITEM_ACTION_HANDLER_ID = nvdsc_item.connect('activate', do_restart)



def update_menu(n_menu, titles, hrefs):

  for i in range(len(titles)):
    item_news = gtk.MenuItem(label = ' ' + titles[i])
    item_news.connect('activate', open_url, hrefs[i])
    item_news.show()
    #  upstream in reversed order
    # we're pushing the existing elements down
#    n_menu.insert(item_news,i)
    n_menu.append(item_news)
  
  # now we just need to remove elements at the end since we got too many
  i=0
  for c in n_menu.get_children():
    if i >= MAX_ITEMS_IN_FEED:
      n_menu.remove(c)
    i = i + 1

#  n_menu.show_all()


# AppIndicator3 doesn't handle SIGINT, wire it up.
signal.signal(signal.SIGINT, signal.SIG_DFL)

notify.init(APP_ID)
warning = notify.Notification()
warning_dss = notify.Notification()


indicator = appindicator.Indicator.new(APP_ID, ICON_DEFAULT, appindicator.IndicatorCategory.SYSTEM_SERVICES)

indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
# indicator.set_menu(build_menu(config))


## if not DSS_UP_TO_DATE:
##   do_warning()

def ver_check_loop(versions):
  global NVDSC_UP_TO_DATE
  while True:
    new_ver = check_ver(versions)
    if new_ver is not None:
      LOG.warning("new version detected: " + new_ver)
      NVDSC_UP_TO_DATE = False
      GLib.idle_add(update_sw_menu_client_item, sw_menu_client, "upgrade")
      notify_upgrade()
    else:
      NVDSC_UP_TO_DATE = True

    time.sleep(VERSION_CHECK_INTERVAL)
    if ALREADY_NOTIFIED_TO_UPGRADE:
      LOG.info("upgrade notification presented. the version check loop exits now..")
      break  

def img_pull_loop():
  global img_pull_queue
  runner = DockerRunner(config)
  while True:
    m, j = img_pull_queue.get()
    j = yaml.safe_load(j)
    img_name = j['image']
    LOG.info("img_pull_thread starting to pull " + img_name)
    runner.pull_img(img_name)
    LOG.info("img_pull_thread finished pulling " + img_name)
    GLib.idle_add(enable_pulled_menu_item, m, j)
    
def enable_pulled_menu_item(menu_item, j):
  parent = menu_item.get_parent()
  i=0
  pos = None
  for c in parent.get_children():
    if c == menu_item:
      pos = i
      break
    i = i + 1

  if pos is None:
    LOG.error('unable to find menu item')
    return 

  parent.remove(menu_item)

  LOG.debug('inserting check menu item ' + j['name'] + ' at position ' + str(i))
  i = gtk.CheckMenuItem(label = '  ' + j['name'])
  i._container_launched = False
  i.connect('activate', do_d, config, j)
  parent.insert(i, pos)
  i.show()
  
def check_ver(versions):  
    LOG.info('version check running')
    versions.check_pip_remote()
    if APP_ID in versions.remote:
      if semver.compare(nvdsc.__version__, versions.remote[APP_ID]) >=0:
        LOG.info("up to date: local: " + nvdsc.__version__ + ", remote: " + versions.remote[APP_ID])
        return None
      else:
        LOG.info("NOT up to date: local: " + nvdsc.__version__ + ", remote: " + versions.remote[APP_ID])
        return versions.remote[APP_ID]
    else:
      LOG.info(APP_ID + ' not in list of obsolete packages')
      return None


def main_with_path(script_dir):
  global SCRIPT_DIR
  SCRIPT_DIR = script_dir
  return main()

def main():
  global v
  global DSS_UP_TO_DATE
  LOG.info("in main.. script dir: " + SCRIPT_DIR)
  LOG.warn("allowing local users to access X.. this is for demos")
  # subprocess.call(["xhost", "local:"])
  subprocess.run(["xhost", "local:"], stdout=subprocess.PIPE)

  LOG.info("checking versions")
  v = VersionChecker(config, SCRIPT_DIR)
  v.check_local()

  if v.local['dss'] != "not found":
    if semver.compare(v.local['dss'],LATEST_DSS_VER) < 0:
      # likely ought to notify here with a link to the upgrade function. But, prevent nagging.
      DSS_UP_TO_DATE = False
      notify_upgrade_dss()

  try:
    os.stat(LICENSE_ACCEPTED_FILE)
    LOG.debug('license was previously accepted')
  except:
    LOG.debug('license was NOT previously accepted')
    license_str = ' '.join(LICENSE)
    comments = 'Please carefully review the terms of the End User License Agreement located in the License tab and then indicate your agreement by clicking below.\n\nTo exit, choose "I do not accept".'
    dialog = LicenseDialog(title = "Data Science Client", comments = comments, license_str = license_str, icon_file = ICON_DEFAULT)
    dialog.set_modal(True)
    response = dialog.run()
    if response == gtk.ResponseType.OK:
      LOG.debug("license accepted!")
      dialog.destroy()
      with open(LICENSE_ACCEPTED_FILE, 'a'):
        os.utime(LICENSE_ACCEPTED_FILE, None)

    else:
      LOG.warning("license not accepted, exiting")
      sys.exit(2)

  LOG.info("building menu: ")
  indicator.set_menu(build_menu(config))

  news_thread = threading.Thread(target=nu, args=[news_menu])
  news_thread.daemon = True
  news_thread.start()

  ver_thread = threading.Thread(target=ver_check_loop, args=[v])
  ver_thread.daemon = True
  ver_thread.start()

  img_pull_thread = threading.Thread(target=img_pull_loop)
  img_pull_thread.daemon = True
  img_pull_thread.start()

  gtk.main()


if __name__ == '__main__':
  sys.exit(main())
