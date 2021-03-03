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
# Todo: function to checkin cfg files to gitlab
###############################################################################
