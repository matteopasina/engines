#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from datetime import date, time, datetime

from model.Message import Message
from model.Request import Request
from model.Resource import Resource


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
            request.user_id = dict[key]
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
    request = Request(1, request_json['resource_id'], request_json['template_id'], request_json['user_id'])
    request.from_date = datetime.strptime(request_json['from_date'], '%d %b %Y')
    request.to_date = datetime.strptime(request_json['to_date'], '%d %b %Y')

    return request


def mapResource(res_dict):
    '''
    Maps a resource dictionary to a resource class
    :param res_dict: a resource dict
    :return: a resource class
    '''
    resource = Resource(res_dict['R_ID'])
    resource.url = res_dict['URL']
    resource.name = res_dict['Resource_Name']
    resource.media = res_dict['Media']
    resource.language = res_dict['Language']
    resource.category = res_dict['Category']
    resource.description = res_dict['Description']
    resource.subjects = res_dict['Subjects']
    resource.has_messages = res_dict['Has_messages']
    resource.partner = res_dict['Partner']
    resource.periodic = res_dict['Periodic']
    resource.translated = res_dict['Translated']
    resource.on_day = res_dict['On_day']
    resource.every = res_dict['Every']
    resource.repeating_time = res_dict['Repeating_time']
    if res_dict['From date'] != '':
        resource.from_date = datetime.strptime(res_dict['From date'], '%d/%m/%Y')
    if res_dict['To date'] != '':
        resource.to_date = datetime.strptime(res_dict['To date'], '%d/%m/%Y')
    return resource


def mapMessage(message_dict):
    message = Message(message_dict['message_id'], message_dict['user_id'], message_dict['intervention_session_id'])
    message.URL = message_dict['URL']
    message.attached_media = message_dict['attached_media']
    message.attached_audio = message_dict['attached_audio']
    message.channel = message_dict['channel']
    message.message_text = message_dict['message_text']
    message.miniplan_id = message_dict['miniplan_id']
    message.pilot_id = message_dict['pilot_id']
    if message_dict['date'] != '':
        message.date = datetime.strptime(message_dict['date'], '%Y-%m-%d')
    if message_dict['time'] != '':
        message.time = datetime.strptime(message_dict['time'], '%H:%M:%S')
    return message


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
