# network-automation-scripts
Repo with my Network Automation and/or Python scripts, Examples for "Custom Links" in Netbox to other applications by API calls, and so on.

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/sthierolf/network-automation-scripts)


## Ansible

Folder `ansible` conatins examples and code fragments for Cisco, Netbox and Ansible.


## NetBox

Folder `netbox` conatins examples and code fragments for Netbox, Snipe-IT, LibreNMS.

### netbox/backup2git.py
This backup script gets it's devices from Netbox, does a backup with CLI/pexpect and checks in into a gitlab repo. Details at:

[Part One: Backup2Git: Cisco configuration backup with Netbox and Gitlab](https://www.thierolf.org/posts/cisco-configuration-backup-with-netbox-and-gitlab/)

[Part Two: Backup2Git: Low Level Device functions for backup with Netbox and Gitlab](https://www.thierolf.org/posts/low-level-device-functions-for-backup-with-netbox-and-gitlab/)

[Part Three: Backup2Git: Check in of configuration files to a Gitlab server](https://www.thierolf.org/posts/check-in-of-configuration-files-to-a-gitlab-server/)



### netbox/netbox-snipeit.php
Integration of Snipe-IT Asset Management into Netbox DCIM/IPAM as Custom Link with a PHP script and using Snipe-IT API call. Runs on Snipe-IT server. Details at: ~~[Custom links in Netbox for Snipe-IT Asset Management](https://www.thierolf.org/blog/2020/custom-links-in-netbox-for-snipe-it-asset-management/)~~


### netbox/netbox-snipeit.py
Integration of Snipe-IT Asset Management into Netbox DCIM/IPAM as Custom Link in Python. Calls API for hardware (Snipe-IT) / device (NetBox) and location (Snipe-IT) / site (NetBox). Requires CGI module (a2enmod cgid) and apache web server config for CGI on NetBox server. Details at: ~~[Netbox Custom Links for Snipe-IT and LibreNMS](https://www.thierolf.org/blog/2020/netbox-custom-links-for-snipe-it-and-librenms/)~~


### netbox/netbox-librenms.py
Integration of LibreNMS Monitoring into Netbox DCIM/IPAM as Custom Link in Python. Calls API for devicegroup (LibreNMS) / site (NetBox). Requires CGI module (a2enmod cgid) and apache web server config for CGI on NetBox server. Details at: ~~[Netbox Custom Links for Snipe-IT and LibreNMS](https://www.thierolf.org/blog/2020/netbox-custom-links-for-snipe-it-and-librenms/)~~

### netbox/netbox-librenms-graph.py
Python version of [MrXermon/netbox-graph.php](https://gist.github.com/MrXermon/0b40d7b62bc67083529d01c8a33aa8be)


### netbox/qrcode-snipeit.py
Python script to look up Asset tags in Snipe-IT with a generated QR code.Details at: ~~[Looking up asset tags in Snipe-IT with QR code](https://www.thierolf.org/blog/2020/looking-up-asset-tags-in-snipe-it-with-qr-code/)~~



## Misc

### dds-quick-test.py
Simple DMARC DKIM SPF quick test. This script tests a domain for DMARC, DKIM and SPF records. To perform the test, the DKIM selector need to be extracted from an email. To see the DKIM selector you can send an email to yourself and look it up in the headers.

[Small Python script to quick test DMARC DKIM and SPF records](https://www.thierolf.org/posts/small-python-script-to-quick-test-dmarc-dkim-and-spf-records/)

