#!/usr/bin/python
# -*- coding: utf-8 -*-

from operator import attrgetter
import pendulum
from controller.json_manager import encodeResponse, encodePlan
from controller.planner.controlConstraints import controlMsgsDay
from controller.utilities import rebuildMiniplans
from controller.get_data import getMessages, getAged
from controller.delivery.engine_four_delivery import sendIntervention
from model.Aged import Aged



def launch_engine_three(json_req):
    aged_id = json_req["aged_id"]
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
    #substitute with getAged
    aged = Aged('1')
    aged.mobile_phone_number='393297634573'
    aged.email='matteopasina@gmail.com'

    all_messages=getMessages(aged_id)

    sorted_messages = sorted(all_messages, key=attrgetter('date', 'time'))

    for m in sorted_messages:
        if m.date not in dict_m:
            dict_m[m.date] = [m]
        else:
            dict_m[m.date].append(m)

    controlMsgsDay(dict_m)

    miniplans = rebuildMiniplans(sorted_messages)
    for mini in miniplans:
        for m in miniplans[mini]:
            m.channel="SMS"
            #tempDate=pendulum.parse(m.date)
            #tempTime=pendulum.parse(m.time)
            #m.date=tempDate.format('L',formatter='alternative')
            #m.time=tempTime.format('HH:mm',formatter='alternative')
            m.time="18:00"
            sendIntervention(m,aged)
    '''
    for mini in miniplans:
        encodeResponse(errors, miniplans[mini])
    '''
    return encodePlan(errors, sorted_messages)
