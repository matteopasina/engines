#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
import requests
from datetime import datetime
from operator import attrgetter

from controller.json_manager import encodeResponse, encodePlan
from controller.planner.controlConstraints import controlMsgsDay
from controller.utilities import rebuildMiniplans, mapMessage
from controller.get_data import getMiniplans


def launch_engine_three(json_req):
    id_user = json_req["user_id"]
    errors = {}
    all_messages = []
    dict_m = {}

    #miniplans = requests.get('http://..../endpoint/getAllProfileMiniplanFinalMessages/',id_user)

    with open('csv/prova_miniplans.csv') as csvmessages:
        miniplans = csv.DictReader(csvmessages)
        for m in miniplans:
            for key, value in json.loads(m['miniplan_body']).iteritems():
                mes = mapMessage(value)
                mes.expiration_date = datetime.strptime(m['to_date'], '%Y-%m-%d').date()
                all_messages.append(mes)

    # will replace the above read from csv
    # all_messages=getMiniplans(id_user)

    sorted_messages = sorted(all_messages, key=attrgetter('date', 'time'))

    for m in sorted_messages:
        if m.date.date() not in dict_m:
            dict_m[m.date.date()] = [m]
        else:
            dict_m[m.date.date()].append(m)

    controlMsgsDay(dict_m)

    miniplans = rebuildMiniplans(sorted_messages)

    for mini in miniplans:
        encodeResponse(errors, miniplans[mini])
        '''
        params = {'commit_date': 'today', 'from_date': miniplans[mini].from_date, 'to_date': miniplans[mini].to_date,
                  'resource_id': miniplans[mini].resource_id, 'template_id': miniplans[mini].template_id, 'intervention_id': 1,
                  'miniplan_body': miniplans[mini], 'caregiver_id': '?'}
        requests.post("http://hoc3.elet.polimi.it:8080/c4aAPI/setNewMiniplanFinal/", data=params)
        '''

    return encodePlan(errors, sorted_messages)
