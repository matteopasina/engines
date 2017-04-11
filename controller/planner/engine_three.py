#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
from datetime import datetime
from operator import attrgetter

from controller.json_manager import mapMessage, encodeResponse
from controller.planner.controlConstraints import controlMsgsDay
from controller.utilities import rebuildMiniplans


def launch_engine_two(id_user):
    errors = {}
    all_messages = []
    dict_m = {}
    # miniplans = requests.get('http://..../endpoint/getAllProfileMiniplanFinalMessages/',id_user)
    with open('csv/prova_miniplans.csv') as csvmessages:
        miniplans = csv.DictReader(csvmessages)
        for m in miniplans:
            for key, value in json.loads(m['miniplan_body']).iteritems():
                mes = mapMessage(value)
                mes.expiration_date = datetime.strptime(m['to_date'], '%Y-%m-%d').date()
                all_messages.append(mes)

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

        # return encodePlan(errors, sorted_messages)
