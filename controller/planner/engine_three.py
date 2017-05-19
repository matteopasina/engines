#!/usr/bin/python
# -*- coding: utf-8 -*-

from operator import attrgetter

from controller.delivery.engine_four_delivery import sendIntervention
from controller.get_data import getMessages
from controller.json_manager import encodePlan
from controller.planner.controlConstraints import controlMsgsDay
from controller.post_data import postMiniplanFinal, postFinalMessage
from controller.utilities import rebuildMiniplans
from model.Aged import Aged
from pendulum import parse


def launch_engine_three(post_req):
    aged_id = post_req.form["aged_id"]
    errors = {}
    all_messages = []
    response = [{}, {}]
    dict_m = {}

    '''
    with open('csv/prova_miniplans.csv') as csvmessages:
        miniplans = csv.DictReader(csvmessages)
        for m in miniplans:
            for key, value in json.loads(m['miniplan_body']).iteritems():
                mes = mapMessage(value)
                mes.expiration_date = datetime.strptime(m['to_date'], '%Y-%m-%d').date()
                all_messages.append(mes)
    '''
    '''
    aged = getAged(aged_id)
    if aged is None:
        response[0] = {'Error': 'Aged not found'}
        response[1] = {}
        return encodeResponse(response[0], response[1])
    '''
    # substitute with getAged
    aged = Aged('1')
    aged.mobile_phone_number = '393297634573'
    aged.email = 'matteopasina@gmail.com'

    (all_messages, temporaryMiniplans) = getMessages(aged_id)

    sorted_messages = sorted(all_messages, key=attrgetter('date', 'time'))

    for m in sorted_messages:
        if m.date not in dict_m:
            dict_m[parse(m.date)] = [m]
        else:
            dict_m[parse(m.date)].append(m)

    controlMsgsDay(dict_m)

    miniplans = rebuildMiniplans(sorted_messages)

    for mini in miniplans:
        for m in miniplans[mini]:
            if m.final is False:
                m.channel = "SMS"
                # tempDate=pendulum.parse(m.date)
                # tempTime=pendulum.parse(m.time)
                # m.date=tempDate.format('L',formatter='alternative')
                # m.time=tempTime.format('HH:mm',formatter='alternative')
                interventionResponse = sendIntervention(m, aged)
                break

    for t in temporaryMiniplans:
        id_final = postMiniplanFinal(t)
        for mini in miniplans:
            for m in miniplans[mini]:
                if m.final is False and m.miniplan_id == str(t['miniplan_generated_id']):
                    m.miniplan_id = id_final
                    m.final = True
                    postFinalMessage(m)

    return encodePlan(errors, sorted_messages)
