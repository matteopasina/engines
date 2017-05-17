import requests
import pendulum
import json
from datetime import datetime

from model.Resource import Resource
from model.Template import Template
from model.Aged import Aged
from model.ResourceMessage import ResourceMessage
from controller.utilities import getApipath
from controller.json_manager import decodeMessage


def getTemplate(id_template):
    '''
    Makes a API call to get the details of a template having the id, fill a Template class and returns it
    :param id_template: id of the template to retrieve
    :return: template class filled
    '''

    json_template = requests.get(getApipath()+'getTemplate/' + id_template).json()[0]

    if 'Template' in json_template:
        json_template=json_template['Template']
    else:
        return None

    template = Template(id_template)
    template.title = json_template['title']
    template.category = json_template['category']
    template.description = json_template['description']
    template.nmsgmax = json_template['max_number_messages']
    template.nmsgmin = json_template['min_number_messages']
    template.period = json_template['period']
    template.addressed_to = json_template['addressed_to']
    template.flowchart = json_template['flowchart']
    template.compulsory = json_template['compulsory']
    for c in json_template['channels']:
        template.channels.append(c['channel_name'])

    return template


def getResource(id_resource):
    '''
    Makes a API call to get the details of a resource having the id, fill a Resource class and returns it
    :param id_resource: id of the resource to retrieve
    :return: resource class filled
    '''

    json_resource = requests.get(getApipath()+'getResource/' + id_resource).json()[0]

    if 'Resource' in json_resource:
        json_resource=json_resource['Resource']
    else:
        return None

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
        resource.from_date = pendulum.parse(json_resource['from_date'])
    if isinstance(json_resource['to_date'], basestring):
        resource.to_date = pendulum.parse(json_resource['to_date'])

    return resource

def getResourceMessages(id_resource):
    '''
    Makes a API call to get the messages of a resource having the id, fill a list of ResourceMessage classes and returns it
    :param id_resource: the id of the resource owner of the messages
    :return: list of ResourceMessage of the desired resource
    '''

    messages=[]
    json_messages_resource = requests.get(getApipath()+'getResourceMessages/' + id_resource).json()[0]

    if 'Messages' in json_messages_resource:
        json_messages_resource=json_messages_resource['Messages']
    else:
        return None

    for m in json_messages_resource:
        rm=ResourceMessage(m['message_id'])
        rm.channels=m['channels']
        rm.is_compulsory=m['is_compulsory']
        rm.communication_style=m['communication_style']
        rm.semantic_type=m['semantic_type']
        rm.audio=m['audio']
        rm.video=m['video']
        rm.media=m['media']
        rm.text=m['text']
        rm.url=m['url']
        messages.append(rm)

    return messages

# TODO fix hour preference
def getAged(id_aged):
    '''
    Makes a API call to get the details of a user having the id, fill a User class and returns it
    :param id_user: id of the user to retrieve
    :return: user class filled
    '''

    json_aged = requests.get(getApipath()+'getProfile/' + id_aged).json()[0]

    if 'Profile' in json_aged:
        json_aged=json_aged['Profile']
    else:
        return None

    aged = Aged(id_aged)
    aged.name = json_aged['name']
    aged.surname = json_aged['surname']

    json_communicative = \
    requests.get(getApipath()+'getProfileCommunicativeDetails/' + id_aged).json()[0]

    if 'Profile' in json_communicative:
        json_communicative=json_communicative['Profile']
    else:
        return None

    aged.channels = []
    for c in json_communicative['available_channels'].split(', '):
        if c == 'FB':
            aged.channels.append('Facebook')
        else:
            aged.channels.append(c)
    aged.message_frequency = json_communicative['message_frequency']
    aged.topics = json_communicative['topics'].split(', ')
    aged.communication_style = json_communicative['communication_style']

    json_tech = requests.get(getApipath() + 'getProfileTechnicalDetails/' + id_aged).json()[0]

    if 'Profile' in json_tech:
        json_tech = json_tech['Profile']
    else:
        return None

    aged.address = json_tech['address']
    aged.telephone_home_number = json_tech['telephone_home_number']
    aged.mobile_phone_number = json_tech['mobile_phone_number']
    aged.email=json_tech['email']
    aged.facebook=json_tech['facebook_account']
    aged.telegram=json_tech['telegram_account']

    # json_hourPref = requests.get('http://hoc3.elet.polimi.it:8080/c4aAPI/getProfileHourPreferences/' + id_aged).json()
    # aged.hour_preference = json_hourPref[0]['Preferences']['hour_period_id']

    return aged


# TODO fix getMiniplanMessagesCommitted
def getMessages(id_user):

    all_messages = []

    messages=requests.get(getApipath()+'getMiniplanGeneratedMessages/' + id_user).json()[0]['Messages']

    for m in messages:
        all_messages.append(decodeMessage(json.loads(m['message_body'])))

    return all_messages
