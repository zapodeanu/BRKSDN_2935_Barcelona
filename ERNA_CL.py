
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


# import provided modules

import utils
import spark_apis
import dnac_apis


from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth  # for Basic Auth
from PIL import Image, ImageDraw, ImageFont

from ERNA_init import SPARK_AUTH, SPARK_URL, TROPO_KEY

from ERNA_init import DNAC_URL, DNAC_USER, DNAC_PASS
DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

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

ROOM_NAME = 'ERNA'
IT_ENG_EMAIL = 'gabriel.zapodeanu@gmail.com'


def main():
    """
    Vendor will join Spark Room with the name {ROOM_NAME}
    It will ask for access to an IP-enabled device - named {IPD}
    The code will map this IP-enabled device to the IP address {172.16.41.55}
    Access will be provisioned to allow connectivity from DMZ VDI to IPD
    """

    # save the initial stdout
    initial_sys = sys.stdout

    # the user will be asked if interested to run in demo mode
    # production (logging to files - erna_log.log, erna_err.log))

    #user_input = utils.get_input_timeout('If running in Demo Mode please enter y ', 10)
    user_input = 'y'
    if user_input != 'y':

        # open a log file 'erna.log'
        file_log = open('erna_log.log', 'w')

        # open an error log file 'erna_err.log'
        err_log = open('erna_err.log', 'w')

        # redirect the stdout to file_log and err_log
        sys.stdout = file_log
        sys.stderr = err_log

        # configure basic logging to send to stdout, level DEBUG, include timestamps
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=('%(asctime)s - %(levelname)s - %(message)s'))

    # the local date and time when the code will start execution

    DATE_TIME = str(datetime.datetime.now().replace(microsecond=0))
    print('\nThe app started running at this time ' + DATE_TIME)

    # verify if Spark Space exists, if not create Spark Space, and add membership (optional)

    spark_room_id = spark_apis.get_room_id(ROOM_NAME)
    if spark_room_id is None:
        spark_room_id = spark_apis.create_room(ROOM_NAME)
        print('- ', ROOM_NAME, ' -  Spark room created')

        # invite membership to the room
        spark_apis.add_room_membership(spark_room_id, IT_ENG_EMAIL)

        spark_apis.post_room_message(ROOM_NAME, 'To require access enter :  IPD')
        spark_apis.post_room_message(ROOM_NAME, 'Ready for input!')
        print('Instructions posted in the room')
    else:
        print('- ', ROOM_NAME, ' -  Existing Spark room found')

        spark_apis.post_room_message(ROOM_NAME, 'To require access enter :  IPD')
        spark_apis.post_room_message(ROOM_NAME, 'Ready for input!')
    print('- ', ROOM_NAME, ' -  Spark room id: ', spark_room_id)

    # check for messages to identify the last message posted and the user's email who posted the message
    # check for the length of time required for access

    last_message = (spark_apis.last_user_message(ROOM_NAME))[0]

    while last_message == 'Ready for input!':
        time.sleep(5)
        last_message = (spark_apis.last_user_message(ROOM_NAME))[0]
        if last_message == 'IPD':
            last_person_email = (spark_apis.last_user_message(ROOM_NAME))[1]
            spark_apis.post_room_message(ROOM_NAME, 'How long time do you need access for? (in minutes)  : ')
            time.sleep(10)
            if (spark_apis.last_user_message(ROOM_NAME))[0] == 'How long time do you need access for? (in minutes)  : ':
                timer = 30 * 60
            else:
                timer = int(spark_apis.last_user_message(ROOM_NAME)[0]) * 60
        elif last_message != 'Ready for input!':
            spark_apis.post_room_message(ROOM_NAME, 'I do not understand you')
            spark_apis.post_room_message(ROOM_NAME, 'To require access enter :  IPD')
            spark_apis.post_room_message(ROOM_NAME, 'Ready for input!')
            last_message = 'Ready for input!'

    print('\nThe user with this email: ', last_person_email, ' will be granted access to IPD for ', (timer/60), ' minutes')

    # get UCSD API key
    # ucsd_key = get_ucsd_api_key()

    # execute UCSD workflow to connect VDI to VLAN, power on VDI
    # execute_ucsd_workflow(ucsd_key, UCSD_CONNECT_FLOW)

    print('UCSD connect flow executed')

    # get the WJT Auth token to access DNA
    dnac_token = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
    print('\nThe DNA Center auth token is: ', dnac_token)

    # IPD IP address - DNS lookup if available

    ipd_ip = '10.93.140.35'

    # locate IPD in the environment using DNA C
    dnac_apis.get_


    # restore the stdout to initial value
    sys.stdout = initial_sys

    # the local date and time when the code will end execution

    DATE_TIME = str(datetime.datetime.now().replace(microsecond=0))
    print('End of application run at this time ', DATE_TIME)


if __name__ == '__main__':
    main()

