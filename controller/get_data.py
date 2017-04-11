import json
import urllib2
import requests
from datetime import datetime

from model.Resource import Resource
from model.Template import Template
from model.User import User


def getTemplate(id_template):
    '''
    Makes a API call to get the details of a template having the id, fill a Template class and returns it
    :param id_template: id of the template to retrieve
    :return: template class filled
    '''
    json_template = json.load(urllib2.urlopen('https://api/c4a-DBmanager/getTemplate/id_template=' + id_template))
    #json_template=requests.get('https://api/c4a-DBmanager/getTemplate/id_template=',id_template)
    template = Template(id_template)
    template.title = json_template['title']
    template.category = json_template['category']
    template.description = json_template['description']
    template.nmsgmax = json_template['max_messages_number']
    template.nmsgmin = json_template['min_messages_number']
    template.period = json_template['period']
    template.channels = json_template['channel']
    return template


def getResource(id_resource):
    '''
    Makes a API call to get the details of a resource having the id, fill a Resource class and returns it
    :param id_resource: id of the resource to retrieve
    :return: resource class filled
    '''
    json_resource = json.load(urllib2.urlopen('https://api/c4a-DBmanager/getResource/id_resource=' + id_resource))
    # json_resource=requests.get('https://api/c4a-DBmanager/getTemplate/id_resource=',id_resource)
    resource = Resource(id_resource)
    resource.url = json_resource['url']
    resource.name = json_resource['resource_name']
    resource.media = json_resource['media']
    resource.language = json_resource['language']
    resource.category = json_resource['category']
    resource.description = json_resource['description']
    resource.from_date = datetime.strptime(json_resource['from_date'], '%d %b %Y')
    resource.to_date = datetime.strptime(json_resource['to_date'], '%d %b %Y')
    return resource


def getUser(id_user):
    '''
    Makes a API call to get the details of a user having the id, fill a User class and returns it
    :param id_user: id of the user to retrieve
    :return: user class filled
    '''
    json_user = json.load(urllib2.urlopen('https://api/c4a-DBmanager/getResource/id_user=' + id_user))
    # json_resource=requests.get('https://api/c4a-DBmanager/getTemplate/id_resource=',id_resource)
    user = User(id_user)
    user.name = json_user['name']
    user.channels = json_user['channels']
    user.hour_preference = json_user['hour_preference']
    return user