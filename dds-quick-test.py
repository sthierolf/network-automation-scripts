#!/usr/bin/python3
import argparse
import dns.resolver

print ("______ ___  ___  ___  ______  _____   ______  _   __ _____ ___  ___   _____ ______ ______ ")
print ("|  _  \|  \/  | / _ \ | ___ \/  __ \  |  _  \| | / /|_   _||  \/  |  /  ___|| ___ \|  ___|")
print ("| | | || .  . |/ /_\ \| |_/ /| /  \/  | | | || |/ /   | |  | .  . |  \ `--. | |_/ /| |_   ")
print ("| | | || |\/| ||  _  ||    / | |      | | | ||    \   | |  | |\/| |   `--. \|  __/ |  _|  ")
print ("| |/ / | |  | || | | || |\ \ | \__/\  | |/ / | |\  \ _| |_ | |  | |  /\__/ /| |    | |    ")
print ("|___/  \_|  |_/\_| |_/\_| \_| \____/  |___/  \_| \_/ \___/ \_|  |_/  \____/ \_|    \_|    ")
print ("                                               |  _        '   _  |     |_   _   ,_  |_ ")
print ("            Copyright (C) 2021 Stefan Thierolf | (_|  (_)  |  (_  |<    |_  (/_  _\  |_ ")
print ("                                 License GPLv3 |   |                                    ")
print ()


parser = argparse.ArgumentParser(description='Simple DMARC DKIM SPF quick test.')
parser.add_argument('domain', help='Domain name to test')
parser.add_argument('selector', help='DKIM Selector, can be extracted from email')
args = parser.parse_args()
domain = args.domain
selector = args.selector

#
# Testing DMARC
#
print()
print ("Testing domain", domain, "for DMARC record...")
try:
    test_dmarc = dns.resolver.resolve('_dmarc.' + domain , 'TXT')
    for dns_data in test_dmarc:
        if 'DMARC1' in str(dns_data):
            print ("  [PASS] DMARC record found :",dns_data)
except:
    print ("  [FAIL] DMARC record not found.")
    pass
#
# Testing DKIM
#
print()
print ("Testing domain", domain, "for DKIM record with selector", selector, "...")
try:
    test_dkim = dns.resolver.resolve(selector + '._domainkey.' + domain , 'TXT')
    for dns_data in test_dkim:
        if 'DKIM1' in str(dns_data):
            print ("  [PASS] DKIM record found  :",dns_data)
except:
    print ("  [FAIL] DKIM record not found.")
    pass

#
# Testing SPF
#
print()
print ("Testing domain", domain, "for SPF record...")
try:
    test_spf = dns.resolver.resolve(domain , 'TXT')
    for dns_data in test_spf:
        if 'spf1' in str(dns_data):
            print ("  [PASS] SPF record found   :",dns_data)
except:
    print ("  [FAIL] SPF record not found.")
    pass
