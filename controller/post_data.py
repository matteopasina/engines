import requests
from pendulum import Date
from utilities import getApipath

def postMiniplanGenerated(miniplan_messages, req):
    '''
    Post miniplan just generated in the DB and all the messages apart in a different table in the DB
    :param miniplan_messages: the miniplan
    :param req: the json request arrived
    :return: nothing
    '''

    params = {'generation_date': Date.today().to_date_string(), 'from_date': req.from_date.to_date_string(),
              'to_date': req.to_date.to_date_string(),
              'resource_id': req.resource_id, 'template_id': req.template_id,
              'intervention_id': req.intervention_session_id,
              'miniplan_body': miniplan_messages}

    print params

    r = requests.post(getApipath()+"setNewMiniplanGenerated/", data=params).json()

    print r

    if 'new_id' in r[0]:
        return r[0]['new_id']

def postGeneratedMessage(message,jsonMessage):
    paramsMessage = {'time_prescription': message.date, 'channel': message.channel, 'generation_date': Date.today().to_date_string(),
                     'message_body': jsonMessage, 'miniplan_generated_id': message.miniplan_id,
                     'intervention_session_id': message.intervention_session_id}

    print paramsMessage

    r = requests.post(getApipath()+"setNewMiniplanGeneratedMessage", data=paramsMessage).json()

    print r

def postFinalMessage(message):
    paramsMessage = {'time_prescription': message.date, 'channel': message.channel, 'is_modified': 'No',
                     'message_body': message, 'miniplan_id': message.miniplan_id,
                     'intervention_id': message.intervention_session_id}
    r = requests.post(getApipath()+"setNewMiniplanFinalMessage", data=paramsMessage).json()


def postMiniplanFinal(miniplan,miniplan_messages, req):
    params = {'commit_date': Date.today().to_date_string(), 'from_date': req.from_date.to_date_string(),
              'to_date': req.to_date.to_date_string(),
              'resource_id': str(req.resource_id), 'template_id': str(req.template_id),
              'intervention_id': str(req.intervention_session_id), 'caregiver_id': '1',
              'generated_miniplan_id': str(miniplan[0].miniplan_id),
              'miniplan_body': str(miniplan_messages)}

    r = requests.post(getApipath()+"setNewMiniplanFinal/", data=params).json()
