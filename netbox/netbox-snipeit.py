#!/usr/bin/python3
# This file is copyright under the latest version of the EUPL.
# Please see LICENSE file for your rights under this license.
import requests
import cgi
import cgitb
import json

#
# Snipe-IT HOST and API token
#
snipeit_host = 'https://SNIPE-IT_HOST'
token = 'Bearer SNIPE-IT_API_TOKEN'

#
# get form data
#
cgitb.enable()
form = cgi.FieldStorage()

#
# handle devices
#
if "device" in form:
    device = form.getvalue('device')
    url = snipeit_host + '/api/v1/hardware?limit=1&offset=0&search='
    headers = {'authorization': token}
    r = requests.get(url + device, headers = headers)

    #
    # if status code is 200, then redirect to hardware
    #
    if r.status_code == requests.codes.ok:
        #
        # Snipe-IT must return something like an ID
        # If there is no ID, then just list all hardware
        #
        try:
            data = r.json()
            device_id = str(data['rows'][0]['id'])
            print ('Location: ' + snipeit_host + '/hardware/' + device_id + '\n')
        except IndexError:
            print ('Location: ' + snipeit_host + '/hardware/' + '\n')
    else:
        print ('Location: ' + snipeit_host +'\n')
#
# handle locations
#
elif "location" in form:
    location = form.getvalue('location')
    url = snipeit_host + '/api/v1/locations?limit=1&offset=0&search='
    headers = {'authorization': token}
    r = requests.get(url + location, headers = headers)

    #
    # if status code is 200, then redirect to location
    #
    if r.status_code == requests.codes.ok:
        #
        # Snipe-IT must return something like an ID
        # If there is no ID, then just list all locations
        #
        try:
            data = r.json()
            location_id = str(data['rows'][0]['id'])
            print ('Location: ' + snipeit_host + '/locations/' + location_id + '\n')
        except IndexError:
            print ('Location: ' + snipeit_host + '/locations/' +'\n')
    else:
        print ('Location: ' + snipeit_host +'\n')
#
# handle all other errors by just forwarding to the Snipe-IT host
#
else:
    print ('Location: ' + snipeit_host +'\n')
