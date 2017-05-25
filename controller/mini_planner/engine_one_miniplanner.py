#!/usr/bin/python
# -*- coding: utf-8 -*-

from controller.get_data import *
from controller.json_manager import encodeResponse, decodeRequestPendulum
from controller.mini_planner import message_prescheduler


def launch_engine_one_Pendulum(post_req):
    '''
    This method gets the data and launches the engine one
    :param post_req: the post request
    :return: the miniplan built 
    '''
    response = [{}, {}]
    req = decodeRequestPendulum(post_req)
    template = None
    aged = None
    resource = None

    template = getTemplate(req.template_id)
    if template is None:
        response[0] = {'Error': 'Template not found'}
        response[1] = {}
        return encodeResponse(response[0], response[1], req)

    resource = getResource(req.resource_id)
    if resource is None:
        response[0] = {'Error': 'Resource not found'}
        response[1] = {}
        return encodeResponse(response[0], response[1], req)

    aged = getAged(req.aged_id)
    if aged is None:
        response[0] = {'Error': 'Aged not found'}
        response[1] = {}
        return encodeResponse(response[0], response[1], req)

    '''
    with open('csv/prova_templates.csv') as csvTemplates:
        templates = csv.DictReader(csvTemplates)
        for t in templates:
            if t['ID'] == req.template_id:
                template = mapTemplate(t)
                break
        if template is None:
            response[0] = {'Error': 'Template not found'}
            response[1] = {}
            return encodeResponse(response[0], response[1], req)

    with open('csv/prova_profiles.csv') as csvProfiles:
        profiles = csv.DictReader(csvProfiles)
        for p in profiles:
            if p['ID'] == req.aged_id:
                aged = mapProfile(p)
                break
        if aged is None:
            response[0] = {'Error': 'Aged not found'}
            response[1] = {}
            return encodeResponse(response[0], response[1], req)

    with open('csv/prova_import_resources.csv') as csvResources:
        resources = csv.DictReader(csvResources)
        for r in resources:
            if r['R_ID'] == req.resource_id:
                resource = mapResource(r)
                break
        if resource is None:
            response[0] = {'Error': 'Resource not found'}
            response[1] = {}
            return encodeResponse(response[0], response[1], req)
    '''

    '''Compose miniplan
    '''
    if resource.periodic == 'Yes':
        response = message_prescheduler.schedulePPendulum(req, resource, template, aged)
    elif template.category == 'Events' or template.category == 'Opportunities':
        response = message_prescheduler.scheduleLPendulum(req, resource, template, aged)
    else:
        response = message_prescheduler.scheduleEDPPendulum(req, resource, template, aged)

    '''Encode response: builds json and posts miniplan
    '''

    return encodeResponse(response[0], response[1], req)
