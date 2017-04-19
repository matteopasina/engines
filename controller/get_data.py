import requests
from datetime import datetime

from model.Resource import Resource
from model.Template import Template
from model.Aged import Aged
from controller.utilities import mapMessage


def getTemplate(id_template):
    '''
    Makes a API call to get the details of a template having the id, fill a Template class and returns it
    :param id_template: id of the template to retrieve
    :return: template class filled
    '''
    json_template = requests.get('http://hoc3.elet.polimi.it:8080/c4aAPI/getTemplate/' + id_template).json()[0][
        'Template']

    template = Template(id_template)
    template.title = json_template['title']
    template.category = json_template['category']
    template.description = json_template['description']
    template.nmsgmax = json_template['max_number_messages']
    template.nmsgmin = json_template['min_number_messages']
    template.period = json_template['period']
    template.channels = json_template['channels']
    template.addressed_to = json_template['addressed_to']
    template.flowchart = json_template['flowchart']
    template.compulsory = json_template['compulsory']

    return template


def getResource(id_resource):
    '''
    Makes a API call to get the details of a resource having the id, fill a Resource class and returns it
    :param id_resource: id of the resource to retrieve
    :return: resource class filled
    '''
    json_resource = requests.get('http://hoc3.elet.polimi.it:8080/c4aAPI/getResource/' + id_resource).json()[0][
        'Resource']

    resource = Resource(id_resource)
    resource.url = json_resource['url']
    resource.name = json_resource['resource_name']
    resource.media = json_resource['media']
    resource.language = json_resource['language']
    resource.category = json_resource['category']
    resource.description = json_resource['description']
    resource.periodic = json_resource['periodic']
    resource.repeating_time = json_resource['repeating_time']
    resource.on_day = json_resource['repeating_on_day']
    resource.has_messages = json_resource['has_messages']
    resource.translated = json_resource['translated']
    resource.partner = json_resource['partner']
    resource.subjects = json_resource['subjects']

    # check dates are strings
    if isinstance(json_resource['from_date'], basestring):
        resource.from_date = datetime.strptime(json_resource['from_date'], '%d %b %Y')
    if isinstance(json_resource['to_date'], basestring):
        resource.to_date = datetime.strptime(json_resource['to_date'], '%d %b %Y')

    return resource


# TODO fix hour preference
def getAged(id_aged):
    '''
    Makes a API call to get the details of a user having the id, fill a User class and returns it
    :param id_user: id of the user to retrieve
    :return: user class filled
    '''
    json_aged = requests.get('http://hoc3.elet.polimi.it:8080/c4aAPI/getProfile/' + id_aged).json()[0]['Profile']

    aged = Aged(id_aged)
    aged.name = json_aged['name']
    aged.surname = json_aged['surname']

    json_communicative = \
    requests.get('http://hoc3.elet.polimi.it:8080/c4aAPI/getProfileCommunicativeDetails/' + id_aged).json()[0][
        'Profile']
    aged.channels = json_communicative['available_channels'].split(', ')
    aged.message_frequency = json_communicative['message_frequency']
    aged.topics = json_communicative['topics'].split(', ')
    aged.communication_style = json_communicative['communication_style']

    # json_hourPref = requests.get('http://hoc3.elet.polimi.it:8080/c4aAPI/getProfileHourPreferences/' + id_aged).json()
    # aged.hour_preference = json_hourPref[0]['Preferences']['hour_period_id']

    return aged


# TODO fix define(populate) miniplans in DB
def getMiniplans(id_user):
    all_messages = []
    miniplans = \
    requests.get('http://hoc3.elet.polimi.it:8080/c4aAPI/getAllProfileMiniplanFinalMessages/' + id_user).json()[0][
        'Final Messages']
    for m in miniplans:
        print m
    '''
        for key, value in json.loads(m['miniplan_body']).iteritems():
            mes = mapMessage(value)
            mes.expiration_date = datetime.strptime(m['to_date'], '%Y-%m-%d').date()
            all_messages.append(mes)
    return all_messages
    '''
