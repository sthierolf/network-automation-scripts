#!/usr/bin/python3
# This file is copyright under the latest version of the EUPL.
# Please see LICENSE file for your rights under this license.
import requests
import cgi
import cgitb
import json

#
# LibreNMS HOST and API token
#
librenms_host = 'https://LIBRENMS_HOST'
token = 'LIBRENMS_TOKEN'

#
# get form data
#
cgitb.enable()
form = cgi.FieldStorage()

#
# handle devices
#
if "devicegroup" in form:
    devicegroup = form.getvalue('devicegroup')
    url = librenms_host + '/api/v0/devicegroups'
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
        try:
            data = r.json()
            #
            # LibreNMS API returns a count of device groups
            #
            rows = data['count']

            #
            # Look up ID by group name
            #
            for i in range(0, rows):
                group_name = str(data['groups'][i]['name'])

                #
                # if group_name matches the passed devicegroup,
                # then get the corresponding ID
                #
                if group_name == devicegroup:
                    group_id = str(data['groups'][i]['id'])
                    print ('Location: ' + librenms_host + '/devices/group=' + group_id + '\n')
                else:
                    print ('Location: ' + librenms_host + '/devices/' + '\n')

        except IndexError:
            print ('Location: ' + librenms_host + '/devices/' + '\n')
    else:
        print ('Location: ' + librenms_host +'\n')

#
# handle all other errors by just forwarding to the LibreNMS host
#
else:
    print ('Location: ' + librenms_host +'\n')
