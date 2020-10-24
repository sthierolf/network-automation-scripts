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
snipeit_host = '[SNIPE_IT_HOST]'
token = 'Bearer [SNIPE_IT_AUTH_TOKEN]'

#
# get form data
#
cgitb.enable()
form = cgi.FieldStorage()

#
# handle devices
#
if "tag" in form:
    tag = form.getvalue('tag')
    url = snipeit_host + '/api/v1/hardware/bytag/'
    headers = {'authorization': token}
    r = requests.get(url + tag, headers = headers)

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
            device_id = str(data['id'])
            print ('Location: ' + snipeit_host + '/hardware/' + device_id + '\n')
        except:
            print ('Location: ' + snipeit_host + '/hardware/' + '\n')
    else:
        print ('Location: ' + snipeit_host +'\n')
#
# handle all other errors by just forwarding to the Snipe-IT host
#
else:
    print ('Location: ' + snipeit_host +'\n')
