#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from json import dumps

from controller.utilities import getDeliverypath


def sendIntervention(message, aged):
    if message.channel == "SMS":
        i = 0
        f = 160
        while i < len(message.message_text):
            params = {"user": "C4A", "pass": "cb5e72d9db4d39613910dd0ef60cd5f5ad5e0041cedb3b18ef8ef9ab504323e3",
                      "channel": "sms",
                      "mode": "relay",
                      "to": aged.mobile_phone_number,
                      "msg": message.message_text.encode('utf8')[i:f]}  # DD/MM/YYYY HH:mm

            r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()
            i += 160
            f += 160


    elif message.channel == 'Email':

        params = {'user': 'C4A', 'pass': 'cb5e72d9db4d39613910dd0ef60cd5f5ad5e0041cedb3b18ef8ef9ab504323e3',
                  'channel': 'email',
                  'mode': 'relay',
                  'to': aged.email,
                  'msg': message.message_text,
                  'sendTime': message.time}  # DD/MM/YYYY HH:mm

        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    elif message.channel == 'Telegram':

        params = {'user': 'C4A', 'pass': 'cb5e72d9db4d39613910dd0ef60cd5f5ad5e0041cedb3b18ef8ef9ab504323e3',
                  'channel': 'telegram',
                  'mode': 'relay',
                  'to': aged.telegram,
                  'msg': message.message_text,
                  'sendTime': message.time}  # DD/MM/YYYY HH:mm

        r = requests.post(getDeliverypath() + "sendIntervention/", data=dumps(params)).json()

    return r
