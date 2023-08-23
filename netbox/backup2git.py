#!/usr/bin/python3
import pynetbox
import requests
import urllib3
import pexpect
import sys
import json
import gitlab
from datetime import date
today = str(date.today())

###############################################################################
#
# Set global variables
#
###############################################################################
# Netbox URL and Token
netbox_url = "https://HOST_OR_IP"
netbox_token = "TOKEN"
# Gitlab URL and Token
gitlab_url = "https://HOST_OR_IP"
gitlab_token = "TOKEN"
# SCP User, Password and Host (SCP host can be same like Netbox host)
scp_user = "USERNAME"
scp_pass = "PASSWORD"
scp_host = "HOST_OR_IP"
# Set User, Password and Enable to connect with SSH to devices
backup_user = "USERNAME"
backup_pass = "PASSWORD"
backup_enable = "ENABLE_PASSWORD"
# Set Gitlab project ID
project_id = PROJECT_ID


###############################################################################
def getDevicesFromNetbox():
  urllib3.disable_warnings()
  requests.packages.urllib3.disable_warnings()
  netbox = pynetbox.api(
    url = netbox_url,
    token = netbox_token,
    threading = True
  )
  netbox.http_session.verify = False

  # init empty device array
  devices_netbox = []
  
  #
  # Build a list with Core-Switches
  # Note: The filtering by role depends on the roles defined in netbox
  #
  # the list needs at minimum the following information:
  # device / site / hostname / status / ipv4 address
  # device: used to determine the device and what CLI commands are required to start a backup
  # site: used to build a directory structure in gitlab project
  # hostname: the hostname of the device to build .cfg
  # status: to determine if device can be backed up or is out of it
  # ipv4: IP address to connect to the device

  core_switch = netbox.dcim.devices.filter(role='net-core-switch')
  for i in range(0, len(core_switch)):
    data = netbox.dcim.devices.get(name = core_switch[i])
    hostname = str(data).split(":")
    hostname = hostname[0]
    device_details = ["switch", str(data.site), hostname, str(data.primary_ip), str(data.status)]
    devices_netbox.append(device_details)

  access_switch = netbox.dcim.devices.filter(role='net-access-switch')
  for i in range(0, len(access_switch)):
    data = netbox.dcim.devices.get(name = access_switch[i])
    hostname = str(data).split(":")
    hostname = hostname[0]
    device_details = ["switch", str(data.site), hostname, str(data.primary_ip), str(data.status)]
    devices_netbox.append(device_details)

  wifi_controller = netbox.dcim.devices.filter(role='net-wireless-lan-controller')
  for i in range(0, len(wifi_controller)):
    data = netbox.dcim.devices.get(name = wifi_controller[i])
    hostname = str(data).split(":")
    hostname = hostname[0]
    device_details = ["wificontroller", str(data.site), hostname, str(data.primary_ip), str(data.status)]
    devices_netbox.append(device_details)

  wan_firewall = netbox.dcim.devices.filter(role='net-wan-firewall')
  for i in range(0, len(wan_firewall)):
    data = netbox.dcim.devices.get(name = wan_firewall[i])
    hostname = str(data).split(":")
    hostname = hostname[0]
    device_details = ["wanfirewall", str(data.site), hostname, str(data.primary_ip), str(data.status)]
    devices_netbox.append(device_details)

  return devices_netbox

###############################################################################
def cliCiscoSwitch():
  try:
    print ("INFO: Connecting to device: " + hostname + " with IP: " + ipv4)
    sshconn = pexpect.spawn('ssh %s@%s' % (backup_user, ipv4))
    #sshconn.logfile = sys.stdout.buffer
    sshconn.timeout = 30

    sshconn.expect('.*assword:.*')
    sshconn.sendline(backup_pass)
    sshconn.expect('#')
    sshconn.sendline('term len 0')
    sshconn.expect('#')

    print ('INFO: Set exec banner')
    sshconn.sendline('conf t')
    sshconn.expect('#')
    sshconn.sendline('file prompt quiet')
    sshconn.expect('#')
    sshconn.sendline('banner exec ^')
    sshconn.sendline(today + ' - Config saved by backup2git')
    sshconn.sendline('^')
    sshconn.expect('#')
    sshconn.sendline('exit')

    print ('INFO: Executing write memory command')
    sshconn.sendline('wr mem')
    sshconn.expect('.*OK.*')

    print ('INFO: Executing copy run scp command')
    sshconn.sendline('copy run scp://' + scp_user + ':' + scp_pass + '@' + scp_host + '//tmp/' + hostname + '.cfg')
    sshconn.expect('.*copied.*')

    print ('INFO: Log out from device: ' + hostname + " with ip: " + ipv4)
    sshconn.sendline('logout')

  except pexpect.TIMEOUT:
    print ("ERROR: No login to device: " + hostname + " with ip: " + ipv4)
    pass
  
###############################################################################
def cliCiscoWirelessController():
  try:
    print ("INFO: Connecting to device: " + hostname + " with IP: " + ipv4)
    sshconn = pexpect.spawn('ssh %s@%s' % (backup_user, ipv4))
    #sshconn.logfile = sys.stdout.buffer
    sshconn.timeout = 30

    sshconn.expect('.*ser:.*')
    sshconn.sendline(backup_user)
    sshconn.expect('.*assword:.*')
    sshconn.sendline(backup_pass)
    sshconn.expect('>')
    print ('INFO: Executing save config command')
    sshconn.sendline('save config')
    sshconn.expect('(y/n)')
    sshconn.sendline('y')

    print ('INFO: set transfer parameters')
    sshconn.sendline('transfer upload datatype config')
    sshconn.expect('>')
    sshconn.sendline('transfer upload mode sftp')
    sshconn.expect('>')
    sshconn.sendline('transfer upload serverip ' + scp_host)
    sshconn.expect('>')
    sshconn.sendline('transfer upload filename ' + hostname + ".cfg")
    sshconn.expect('>')
    sshconn.sendline('transfer upload path /tmp/')
    sshconn.expect('>')
    sshconn.sendline('transfer upload username ' + scp_user)
    sshconn.expect('>')
    sshconn.sendline('transfer upload password ' + scp_pass)
    sshconn.expect('>')

    print ('INFO: Executing transfer upload start command')
    sshconn.sendline('transfer upload start')
    sshconn.expect('(y/N)')
    sshconn.sendline('y')
    sshconn.expect('successfully.')

    print ('INFO: Log out from device: ' + hostname + " with ip: " + ipv4)
    sshconn.sendline('logout')

  except pexpect.TIMEOUT:
    print ("ERROR: No login to device: " + hostname + " with ip: " + ipv4)
    pass
  
###############################################################################
def cliCiscoAsaFirewall():
  try:
    print ("INFO: Connecting to device: " + hostname + " with IP: " + ipv4)
    sshconn = pexpect.spawn('ssh %s@%s' % (backup_user, ipv4))
    #sshconn.logfile = sys.stdout.buffer
    sshconn.timeout = 30

    sshconn.expect('.*assword:.*')
    sshconn.sendline(backup_pass)
    sshconn.expect('>')
    sshconn.sendline('enable')
    sshconn.expect('.*assword:.*')
    sshconn.sendline(backup_pass)

    print ('INFO: Executing write memory command')
    sshconn.sendline('wr mem')
    sshconn.expect('.*OK.*')

    print ('INFO: Executing copy run scp command')
    sshconn.sendline('copy run scp://' + scp_user + ':' + scp_pass + '@' + scp_host + '//tmp/' + hostname + '.cfg')
    sshconn.expect('.*ource')
    sshconn.sendline()
    sshconn.expect('.*ddress')
    sshconn.sendline()
    sshconn.expect('.*sername')
    sshconn.sendline()
    sshconn.expect('.*ilename')
    sshconn.sendline()
    sshconn.expect('continue connecting')
    sshconn.sendline('yes')
    sshconn.expect('copied')
    sshconn.sendline('logout')

    print ('INFO: Log out from device: ' + hostname + " with ip: " + ipv4)
    sshconn.sendline('logout')

  except pexpect.TIMEOUT:
    print ("ERROR: No login to device: " + hostname + " with ip: " + ipv4)
    pass
  
  
###############################################################################
# Get the devices from Netbox
devices = getDevicesFromNetbox()

  # Use a for-loop to go through the devices and check in the configuration files
  for i in range(0, len(devices)):

    # Split list
    role = str(devices[i][0])
    location = str(devices[i][1])
    hostname = str(devices[i][2])
    ipv4 = str(devices[i][3])[:len(str(devices[i][3]))-3]
    status = str(devices[i][4])

    # If device is active and has a primary IPv4 address (ssh connect action)
    if status == "Active" and ipv4 != "N":

      # role is a switch
        if role == "switch":
          cliCiscoSwitch()
        # role is a wlc
        elif role == "wificontroller":
          cliCiscoWirelessController()
        # role is a firewall
        elif role == "wanfirewall":
          cliCiscoAsaFirewall()

    # handle list from netbox if device is missing ipv4 or if
    # device status is set to something else than active
    else:
      print ("WARN: device not set to active or IP missing")

    # If device is active and has primary IPv4 address (open file action)
    if status == "Active" and ipv4 != "N":
      # open config file and read it into a string variable
      try:
        content = open('/tmp/' + hostname + '.cfg').read()
      except:
        print ("ERROR: Cannot open file: " + hostname + ".cfg")

      urllib3.disable_warnings()
      requests.packages.urllib3.disable_warnings()
      gl = gitlab.Gitlab(gitlab_url, ssl_verify=False, private_token=gitlab_token)
      # authenticate
      gl.auth()
      # get gitlab project
      project = gl.projects.get(project_id)

      # try with a commit create if file does not exist on gitlab project
      try:
        data_create = {
          'branch': 'master',
          'commit_message': 'Initial commit of config file on ' + today + ' by backup2git',
          'actions': [
            {
              'action': 'create',
               'file_path': location + '/' + hostname + '.cfg',
               'content': open('/tmp/' + hostname + '.cfg').read(),
            }
          ]
        }
      except:
        print ("Cannot build commit create JSON")
        pass
      # If file exists, use commit update to check in new version of file
      try:
        data_update = {
          'branch': 'master',
          'commit_message': 'Update of config file on ' + today + ' by backup2git',
          'actions': [
            {
              'action': 'update',
              'file_path': location + '/' + hostname + '.cfg',
              'content': open('/tmp/' + hostname + '.cfg').read(),
            }
          ]
        }
      except:
        print ("Cannot build commit update JSON")
        pass
