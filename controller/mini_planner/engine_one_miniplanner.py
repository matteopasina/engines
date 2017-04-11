#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

from controller.get_data import *
from controller.json_manager import decodeRequest, encodeResponse
from controller.mini_planner import message_prescheduler


def launch_engine_one(json_req):
    # prendo json request
    # req = decodeRequest('{"resource_id": "In5","template_id":6,"user_id":7,"from_date":"22 Feb 2017","to_date":"10 Mar 2017"}')
    req = decodeRequest(json_req)

    '''
    template=getTemplate(req.template_id)
    resource=getResource(req.resource_id)
    user=getUser(req.user_id)
    '''

    # query al db con req.template_id
    template = Template(template_id=1,
                        category="Edu",
                        title="Titolo",
                        description="Descrizione molto bella",
                        nmsgmin=7,
                        nmsgmax=7,
                        period=2,
                        channels=["SMS", "Messenger"])

    # query al db con req.user_id
    user = User(user_id=1,
                name="Anselmo",
                channels=["WhatsApp", "SMS", "Messenger"],
                hour_preference='0')

    # TODO get resource,template and user from DB
    # resource = Json_manager.getResource(req.resource_id)
    # template = Json_manager.getTemplate(req.template_id)
    # user = Json_manager.getUser(req.user_id)
    with open('csv/prova_import_resources.csv') as csvmessages:
        resources = csv.DictReader(csvmessages)
        for r in resources:
            if r['R_ID'] == req.resource_id:
                resource = json_manager.mapResource(r)
                break

    '''Compose miniplan
    '''
    if resource.periodic == 'Yes':
        response = message_prescheduler.schedulePeriodic(req, resource, template, user)
    elif template.category == 'Eventi' or template.category == 'Opportunità':
        response = message_prescheduler.scheduleLogarithmic(req, resource, template, user)
    else:
        response = message_prescheduler.scheduleEquallyDividedPeriod(req, resource, template, user)

    '''
    bozza api post 
    data = {'generation_date': 'today', 'from_date': req.from_date, 'to_date': req.to_date,
            'resource_id': req.resource_id, 'template_id': req.template_id, 'intervention_id': 'int_id',
            'miniplan_body': 'json'}
    requests.post("http://.../endpoint/setNewMiniplanGenerated/", params=data)
    '''


    '''Encode response: builds json
    '''
    return encodeResponse(response[0], response[1])
