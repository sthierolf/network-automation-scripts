# netbox-custom-links
Examples for "Custom Links" in Netbox to other applications by API calls

# Code and details

## netbox-snipeit.php
Integration of Snipe-IT Asset Management into Netbox DCIM/IPAM as Custom Link with a PHP script and using Snipe-IT API call.
Runs on Snipe-IT server.
  
Details at: [Custom links in Netbox for Snipe-IT Asset Management](https://www.thierolf.org/blog/2020/custom-links-in-netbox-for-snipe-it-asset-management/)

## netbox-snipeit.py
Integration of Snipe-IT Asset Management into Netbox DCIM/IPAM as Custom Link in Python. 

Calls API for hardware (Snipe-IT) / device (NetBox) and locaton (Snipe-IT) / site (NetBox)

Requires CGI module (a2enmod cgid) and apache web server config for CGI on NetBox server.

Details at: [Netbox Custom Links for Snipe-IT and LibreNMS](https://www.thierolf.org/blog/2020/netbox-custom-links-for-snipe-it-and-librenms/)


## netbox-librenms.py

Integration of LibreNMS Monitoring into Netbox DCIM/IPAM as Custom Link in Python. 

Calls API for devicegroup (LibreNMS) / site (NetBox)

Requires CGI module (a2enmod cgid) and apache web server config for CGI on NetBox server.

Details at: [Netbox Custom Links for Snipe-IT and LibreNMS](https://www.thierolf.org/blog/2020/netbox-custom-links-for-snipe-it-and-librenms/)

