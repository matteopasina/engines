#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import uuid
from datetime import date, time, datetime
import pendulum

from controller.post_data import postMiniplanGenerated, postGeneratedMessage
from model.Request import Request


#TODO fix miniplanid in response
def encodeResponse(errors, miniplan, req=None):
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
                if key == 'message_text':
                    json_message[key] = value.replace("'", " ")
                else:
                    json_message[key] = value
        miniplan_message[message.message_id] = json_message

    # print json.dumps({'Errors': errors}, default=json_serial, sort_keys=True, indent=4, separators=(',', ': '))
    # print json.dumps({'Miniplan': miniplan_message}, default=json_serial, sort_keys=True, indent=4, separators=(',', ': '))
    json_response['Errors'] = errors
    json_response['Miniplan'] = miniplan_message

    #postMiniplanFinal(miniplan,miniplan_message, req)

    jsonToPost=json.dumps(miniplan_message, default=json_serial, sort_keys=True, indent=4,separators=(',', ': '))

    miniplan_id=postMiniplanGenerated(jsonToPost,req)

    for msgs in miniplan_message:
        miniplan_message[msgs]['miniplan_id']=miniplan_id

    for m in miniplan:
        m.miniplan_id=miniplan_id
        mdict=encodeMessage(m)
        jsonMToPost = json.dumps(mdict, default=json_serial, sort_keys=True, indent=4, separators=(',', ': '))
        postGeneratedMessage(m,jsonMToPost)

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

def encodeMessage(message):
    dict={}
    dict['miniplan_id']=message.miniplan_id
    dict['intervention_session_id']=message.intervention_session_id
    dict['pilot_id']=message.pilot_id
    dict['time_2']=message.time_2
    dict['time_1']=message.time_1
    dict['time']=message.time
    dict['message_id']=message.message_id
    dict['channel']=message.channel
    dict['user_id']=message.user_id
    dict['date']=message.date
    dict['expiration_date']=message.expiration_date
    dict['attached_audio']=message.attached_audio
    dict['attached_media']=message.attached_media
    dict['message_text']=message.message_text.replace("'", " ")
    dict['URL']=message.URL
    return dict

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
    request = Request(1,request_json['pilot_id'],request_json['intervention_session_id'], request_json['resource_id'],request_json['template_id'], request_json['aged_id'])
    request.from_date = pendulum.parse(request_json['from_date'])
    request.to_date = pendulum.parse(request_json['to_date'])

    return request

#TODO
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
    if isinstance(obj,uuid.UUID):
        return str(obj)
    raise TypeError("Type not serializable")
