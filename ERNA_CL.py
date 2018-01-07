
# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems

# !/usr/bin/env python3

import requests
import json
import time
import datetime
import requests.packages.urllib3
import logging
import sys
import select

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth  # for Basic Auth

from ERNA_init import SPARK_AUTH, TROPO_KEY

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# The following declarations need to be updated based on your lab environment

CMX_URL = 'https://172.16.11.27/'
CMX_USER = 'python'
CMX_PASSW = 'Clive!17'
CMX_AUTH = HTTPBasicAuth(CMX_USER, CMX_PASSW)

SPARK_URL = 'https://api.ciscospark.com/v1'
ROOM_NAME = 'ERNA'

ASAv_URL = 'https://10.93.130.40'
ASAv_USER = 'python'
ASAv_PASSW = 'cisco'
ASAv_AUTH = HTTPBasicAuth(ASAv_USER, ASAv_PASSW)


UCSD_URL = 'https://10.94.132.69'
UCSD_USER = 'gzapodea'
UCSD_PASSW = 'cisco.123'
UCSD_KEY = '1D3FD49A0D474481AE7A4C6BD33EC82E'
UCSD_CONNECT_FLOW = 'Gabi_VM_Connect_VLAN_10'
UCSD_DISCONNECT_FLOW = 'Gabi_VM_Disconnect_VLAN_10'

DNAC_URL = 'https://172.28.97.216'
DNAC_USER = 'admin'
DNAC_PASS = 'Cisco123'

