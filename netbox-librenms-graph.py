#!/usr/bin/python3
# This file is copyright under the latest version of the EUPL.
# Please see LICENSE file for your rights under this license.
import requests
import cgi
import cgitb
import time
import urllib.parse
import sys

#
# LibreNMS HOST and API token
#
librenms_host = 'https://LIBRENMS_HOST'
token = 'LIBRENMS_API_TOKEN'

#
# get form data
#
cgitb.enable()
form = cgi.FieldStorage()

if "device" in form and "interface" in form:

    timefrom = str(int(time.time()) - 28800)
    device = form.getvalue('device')
    interface = form.getvalue('interface')

    for i in range(0,9):
        device = device.replace(':' + str(i), '')

    device = urllib.parse.quote(device, safe='')
    interface = urllib.parse.quote(interface, safe='')

    url = librenms_host + '/api/v0/devices/' + device + '/ports/' + interface + '/port_bits?width=780&height=200&from=' + timefrom
    headers = {'X-Auth-Token': token}
    r = requests.get(url, headers = headers)

    #
    # if status code is 200, then redirect to device group
    #
    if r.status_code == requests.codes.ok:
        #
        # LibreNMS must return something like an ID
        # If there is no ID, then just list all devices
        #
        print ("Content-Type: image/png")
        print ()
        sys.stdout.flush()
        sys.stdout.buffer.write(r.content)

    else:
        print ('Content-Type: text/html')
        print ()
        print ('error')

#
# handle all other errors by just forwarding to the Snipe-IT host
#
else:
    print ('Content-Type: text/html')
    print ()
    print ('error')
