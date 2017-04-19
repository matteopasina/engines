#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from datetime import date, time, datetime
import pendulum

from model.Request import Request


def encodeResponse(errors, miniplan):
    '''
    Composes the Json to send back with all the information computed
    :param miniplan: the list of Message classes to send
    :return: the string/the json to send back
    '''
    json_response = {}
    miniplan_message = {}

    for message in miniplan:
        json_message = {}

        for key, value in message.__dict__.iteritems():
            if not callable(value) and not key.startswith('__'):
                json_message[key] = value
        miniplan_message[message.message_id] = json_message

    #print json.dumps({'Errors': errors}, default=json_serial, sort_keys=True, indent=4, separators=(',', ': '))
    #print json.dumps({'Miniplan': miniplan_message}, default=json_serial, sort_keys=True, indent=4, separators=(',', ': '))
    json_response['Errors'] = errors
    json_response['Miniplan'] = miniplan_message
    return json.dumps({'Response': json_response}, default=json_serial, sort_keys=True, indent=4,
                      separators=(',', ': '))


def encodePlan(errors, plan):
    '''
    Composes the Json to send back with all the information computed
    :param miniplan: the list of Message classes to send
    :return: the string/the json to send back
    '''
    json_response = {}
    plan_message = {}
    id = 0

    for message in plan:
        json_message = {}

        for key, value in message.__dict__.iteritems():
            if not callable(value) and not key.startswith('__'):
                json_message[key] = value
        plan_message[id] = json_message
        id += 1

    # print json.dumps({'Errors': errors}, default=json_serial, sort_keys=True, indent=4, separators=(',', ': '))
    # print json.dumps({'Miniplan': miniplan_message}, default=json_serial, sort_keys=True, indent=4, separators=(',', ': '))
    json_response['Errors'] = errors
    json_response['Plan'] = plan_message
    return json.dumps({'Response': json_response}, default=json_serial, sort_keys=True, indent=4,
                      separators=(',', ': '))


def decodeRequestOld(request_json):
    '''
    Maps the request Json to Request class
    :param request_json: json sent by the user with the request
    :return: request class with the info in the json
    '''
    dict = json.loads(request_json)
    request = Request(1, 1, 1, 1)

    for key in dict:
        if key == 'request_id':
            request.request_id = dict[key]
        if key == 'resource_id':
            request.resource_id = dict[key]
        if key == 'template_id':
            request.template_id = dict[key]
        if key == 'user_id':
            request.aged_id = dict[key]
        if key == 'category':
            request.category = dict[key]
        if key == 'from_date':
            request.from_date = dict[key]
        if key == 'to_date':
            request.to_date = dict[key]
        if key == 'subjects':
            request.subjects = dict[key]
    return request


def decodeRequest(request_json):
    '''
    Maps the request Json to Request class
    :param request_json: json sent by the user with the request
    :return: request class with the info in the json
    '''
    request = Request(1, request_json['resource_id'], request_json['template_id'], request_json['aged_id'])
    request.from_date = datetime.strptime(request_json['from_date'], '%d %b %Y')
    request.to_date = datetime.strptime(request_json['to_date'], '%d %b %Y')

    return request

def decodeRequestPendulum(request_json):
    '''
    Maps the request Json to Request class
    :param request_json: json sent by the user with the request
    :return: request class with the info in the json
    '''
    request = Request(1, request_json['resource_id'], request_json['template_id'], request_json['aged_id'])
    request.from_date = pendulum.parse(request_json['from_date'])
    request.to_date = pendulum.parse(request_json['to_date'])

    return request

def decodeFlowchart(flowchart):
    pass

def json_serial(obj):
    '''
    JSON serializer for objects not serializable by default json code, date and time objects
    :param obj: object
    :return: object serialized
    '''
    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, time):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")
