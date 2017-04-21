import requests


def postMiniplanGenerated(miniplan_messages, req):
    '''
    Post miniplan just generated in the DB and all the messages apart in a different table in the DB
    :param miniplan_messages: the miniplan
    :param req: the json request arrived
    :return: nothing
    '''
    params = {'generation_date': 'today', 'from_date': req.from_date.to_date_string(),
              'to_date': req.to_date.to_date_string(),
              'resource_id': req.resource_id, 'template_id': req.template_id, 'intervention_id': 1,
              'miniplan_body': miniplan_messages}

    r = requests.post("http://hoc3.elet.polimi.it:8080/c4aAPI/setNewMiniplanGenerated/", data=params).json()

    miniplan_id = r[0]['new_id']

    for message in miniplan_messages:
        paramsMessage = {'time_prescription': message.date, 'channel': message.channel, 'generation_date': 'today',
                         'message_body': message, 'miniplan_id': miniplan_id, 'intervention_id': 1}
        requests.post("http://hoc3.elet.polimi.it:8080/c4aAPI/setNewMiniplanGeneratedMessage/", data=paramsMessage)
