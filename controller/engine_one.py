#!/usr/bin/python
# -*- coding: utf-8 -*-
from model.Template import Template
from model.User import User
from controller import Scheduler
from controller import Json_manager
import urllib2
import requests
import csv
import json

def launch_engine_one(json_req):
    # prendo json request
    #req = Json_manager.decodeRequest('{"resource_id": "In5","template_id":6,"user_id":7,"from_date":"22 Feb 2017","to_date":"10 Mar 2017"}')
    req= Json_manager.decodeRequestv2(json_req)

    # query al db con req.template_id
    template = Template(template_id=1,
                        category="Edu",
                        title="Titolo",
                        description="Descrizione molto bella",
                        nmsgmin=5,
                        nmsgmax=5,
                        period=2,
                        channels=["SMS", "Messenger"])

    # query al db con req.user_id
    user = User(user_id=1,
                name="Anselmo",
                channels=["WhatsApp","SMS", "Messenger"],
                hour_preference='0')

    # TODO get resource,template and user from DB
    # resource = Json_manager.getResource(req.resource_id)
    # template = Json_manager.getTemplate(req.template_id)
    # user = Json_manager.getUser(req.user_id)
    with open('csv/prova_import_resources.csv') as csvmessages:
        resources = csv.DictReader(csvmessages)
        for r in resources:
            if r['R_ID'] == req.resource_id:
                resource = Json_manager.mapResource(r)
                break

    '''Compose miniplan
    '''
    print resource.periodic
    if resource.periodic == 'Yes':
        response = Scheduler.schedulePeriodic(req, resource, template, user)
    elif template.category == 'Eventi' or template.category=='Opportunità':
        response = Scheduler.scheduleLogaritmic(req, resource, template, user)
    else:
        response = Scheduler.scheduleEquallyDividedPeriod(req, resource, template, user)

    '''Encode response: builds json
    '''
    return Json_manager.encodeResponse(response[0],response[1])
