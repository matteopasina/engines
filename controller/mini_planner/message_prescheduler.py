#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import random as rnd
import pendulum
from pendulum import Period, Pendulum
from datetime import datetime, timedelta

from controller.mini_planner.define_channels import getChannelsAvailable, channelWithProbability
from controller.mini_planner.engine_two_message_builder import generate_message_text
from controller.mini_planner.hour_manager import scheduleHour, scheduleHourFromDate
from controller.mini_planner.message_selector import getListMessages
from controller.utilities import mapDay, convertDatetime, checkMsgsOneDay, convertPendulum, checkMsgsOneDayPendulum
from model.Message import Message


# OLD
def scheduleRandom(request, resource, template, user):
    '''
    Returns the miniplan scheduled with random times
    :param request: a request class
    :param template: a template class
    :param user: a user class
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"

    times = convertDatetime(request, template)
    startime = times[0]
    endtime = times[1]
    period = times[2]

    valid_interval = endtime - startime
    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count) for count in xrange(nmsg)]

    channel = getChannelsAvailable(template, user)

    for i in range(0, nmsg):
        step_send_msg = timedelta(seconds=rnd.randrange(0, valid_interval.total_seconds(), 3600))
        miniplan[i].date = startime + step_send_msg
        miniplan[i].time = scheduleHourFromDate(user, miniplan[i].date).time()
        miniplan[i].channel = channel

        print miniplan[i].date, miniplan[i].channel, miniplan[i].time

    return miniplan


# OLD
def scheduleEquallyDivided(request, resource, template, user):
    '''
    Returns the miniplan with the temporal interval between the msgs divided equally
    WARN: It does not consider period
    :param request: a request class
    :param template: a template class
    :param user: a user class
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"

    # convert to datetime the times
    times = convertDatetime(request, template)
    startime = times[0]
    endtime = times[1]

    # compute the day step to send the msgs
    valid_interval = endtime - startime
    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax
    step_send_msg = valid_interval / nmsg
    print str(step_send_msg) + "\n"

    # creates miniplan that is a list of messages
    miniplan = [Message(count) for count in xrange(nmsg)]

    channel = getChannelsAvailable(template, user)

    # for nmsg fill the miniplan msgs
    date = endtime - timedelta(days=1)
    for i in range(0, nmsg):
        miniplan[i].date = date
        miniplan[i].time = scheduleHour(user, None)
        miniplan[i].channel = channel
        miniplan[i].message_text = generate_message_text(user,
                                                         main_text='Sapevi che il ballo migliora la coordinazione, '
                                                                   'ha effetti positivi sulla circolazione sanguigna '
                                                                   'e favorisce la socializzazione? È veramente il modo '
                                                                   'perfetto per tenersi in forma divertendosi :) '
                                                                   'Provalo sulla tua pelle: Il 22 settembre al '
                                                                   'Teatro Paisiello di Lecce avrà inizio la '
                                                                   'nuova edizione di Slowtango, una giornata interamente '
                                                                   'dedicata a questo stile di danza così affascinante. '
                                                                   'Non mancare, siamo sicuri che ti divertirai un mondo!')

        date -= step_send_msg
        print miniplan[i].date, miniplan[i].channel, miniplan[i].time

    return miniplan


# OLD
def scheduleProgressive(request, resource, template, user, const_div_interval=2):
    '''
    Returns the miniplan scheduled with more frequency at the end of the interval
    It divides the interval for every msg by const_div_interval e.g. if =2 -> :1 1/2 1/4 1/8
    WARN: It does not consider period
    Last message always sent the day before the event
    :param request: a request class
    :param template: a template class
    :param user: a user class
    :param const_div_interval: const that divides for every cicle the time interval to send the msgs
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"

    times = convertDatetime(request, template)
    startime = times[0]
    endtime = times[1]
    period = times[2]

    valid_interval = endtime - startime
    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, user)

    valid_interval = timedelta(seconds=valid_interval.total_seconds() / const_div_interval)
    for i in range(0, nmsg):
        date = endtime - valid_interval
        valid_interval = timedelta(seconds=valid_interval.total_seconds() / const_div_interval)

        miniplan[i].date = date.date()

        miniplan[i].time = scheduleHourFromDate(user, date).time()

        miniplan[i].channel = channelWithProbability(channels)

        # messages = json.load(urllib2.urlopen('https://api/c4a-DBmanager/getResource_messages/id_resource=' + request.resource+'&channels='))

        miniplan[i].message_text = generate_message_text(user,
                                                         main_text='Sapevi che il ballo migliora la coordinazione, '
                                                                   'ha effetti positivi sulla circolazione sanguigna '
                                                                   'e favorisce la socializzazione? È veramente il modo '
                                                                   'perfetto per tenersi in forma divertendosi :) '
                                                                   'Provalo sulla tua pelle: Il 22 settembre al '
                                                                   'Teatro Paisiello di Lecce avrà inizio la '
                                                                   'nuova edizione di Slowtango, una giornata interamente '
                                                                   'dedicata a questo stile di danza così affascinante. '
                                                                   'Non mancare, siamo sicuri che ti divertirai un mondo!')

        print miniplan[i].date, miniplan[i].channel, miniplan[i].time

    if (endtime - timedelta(days=1)).date() != miniplan[-1].date:
        miniplan[-1].date = (endtime - timedelta(days=1)).date()
        print miniplan[i].date, miniplan[i].channel, miniplan[i].time

    return miniplan


# OLD
def schedulePeriodProgressive(request, resource, template, user, const_div_interval=2):
    '''
    Returns the miniplan scheduled with more frequency at the end of the interval
    It divides the interval for every msg by const_div_interval e.g. if =2 -> :1 1/2 1/4 1/8
    Last message always sent the day before the event
    :param request: a request class
    :param template: a template class
    :param user: a user class
    :param const_div_interval: const that divides for every cicle the time interval to send the msgs
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"

    times = convertDatetime(request, template)
    startime = times[0]
    endtime = times[1]
    period = times[2]

    '''
    Check if the dates passed by the user and the dates of the resource are compatible
    json_resource = json.load(urllib2.urlopen('https://api/c4a-DBmanager/getResource/id_resource=' + request.resource_id))
    resource=Resource(json_resource['id_resource'])
    resource.from_date = datetime.strptime(json_resource['From'], '%d %b %Y')
    resource.to_date = datetime.strptime(json_resource['To'], '%d %b %Y')

    if endtime > resource.to_date:
        endtime = resource.to_date
    if startime > resource.to_date:
        miniplan=[]
        return miniplan
    '''

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period
    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, user)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    valid_interval = timedelta(seconds=valid_interval.total_seconds() / (const_div_interval / 2))
    for i in range(0, nmsg):
        date = endtime - valid_interval
        valid_interval = timedelta(seconds=valid_interval.total_seconds() / const_div_interval)

        miniplan[i].date = date.date()

        miniplan[i].time = scheduleHourFromDate(user, date).time()

        # messages = json.load(urllib2.urlopen('https://api/c4a-DBmanager/getResource_messages/id_resource=' + request.resource+'&channels='))
        # main_text = rnd.choice(messages)

        miniplan[i].message_text = generate_message_text(user,
                                                         main_text=msgs_tosend[i]['Text'])
        miniplan[i].attached_audio = msgs_tosend[i]['Audio']
        miniplan[i].attached_media = msgs_tosend[i]['Media']
        miniplan[i].URL = msgs_tosend[i]['URL']
        miniplan[i].channel = msgs_tosend[i]['Channel']

        print miniplan[i].date, miniplan[i].channel, miniplan[i].time

    if (endtime - timedelta(days=1)).date() != miniplan[-1].date:
        miniplan[-1].date = (endtime - timedelta(days=1)).date()
        print miniplan[i].date, miniplan[i].channel, miniplan[i].time

    return miniplan


def scheduleEDPPendulum(request, resource, template, aged):
    '''
        Returns the miniplan with the temporal interval between the msgs divided equally with Pendulum
        :param request: a request class
        :param template: a template class
        :param aged: a user class
        :return: a miniplan that is a list of messages class with all the fields completed
        '''
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not Pendulum:
        times = convertPendulum(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = pendulum.Period(startime, startime.add(weeks=template.period))

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    # creates miniplan that is a list of messages
    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, None, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    step_send_msg = valid_interval / lenloop

    date = startime + (step_send_msg / 2)
    for i in range(0, lenloop):
        miniplan[i].date = date.date()
        miniplan[i].time = scheduleHour(aged, None)
        miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'], msgs_tosend[i]['URL'])
        miniplan[i].attached_audio = msgs_tosend[i]['Audio']
        miniplan[i].attached_media = msgs_tosend[i]['Media']
        miniplan[i].URL = msgs_tosend[i]['URL']
        miniplan[i].channel = msgs_tosend[i]['Channel']

        date += step_send_msg

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def scheduleLPendulum(request, resource, template, aged):
    '''
    Returns the miniplan scheduled with more frequency at the end of the interval
    It divides the interval for every msg with logaritmic growth:1 1/2 1/3 1/4
    Check on period(valid weeks): if request interval is larger that period then user period as interval
    Last message always sent the day before the event
    With Pendulum
    :param request: a request class
    :param template: a template class
    :param aged: a user class
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not Pendulum:
        times = convertPendulum(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = pendulum.Period(startime, startime.add(weeks=template.period))
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    for i in range(0, lenloop):
        date = endtime - valid_interval

        miniplan[i].date = date.date()

        miniplan[i].time = scheduleHourFromDate(aged, date).time()

        '''
        # messages = json.load(urllib2.urlopen('http://..../endpoint/getResource/' + request.resource_id))
        '''

        miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'], msgs_tosend[i]['URL'])

        miniplan[i].attached_audio = msgs_tosend[i]['Audio']
        miniplan[i].attached_media = msgs_tosend[i]['Media']
        miniplan[i].URL = msgs_tosend[i]['URL']
        miniplan[i].channel = msgs_tosend[i]['Channel']

        valid_interval = valid_interval / (i + 2)

    miniplan = checkMsgsOneDayPendulum(miniplan, endtime)

    return errors, miniplan


def schedulePPendulum(request, resource, template, aged):
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not Pendulum:
        times = convertPendulum(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = pendulum.Period(startime, startime.add(weeks=template.period))
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    day_of_event = mapDay(resource.on_day)
    if day_of_event == None:
        errors['ErrorNoDay'] = 'Error no day specified for periodic messages'
        miniplan = []
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    c = 0
    i = 0
    for dt in valid_interval.range("days"):
        if dt.day_of_week == day_of_event:
            if c % int(resource.every) == 0:
                if i > lenloop:
                    break
                miniplan[i].date = dt.date()
                miniplan[i].time = scheduleHour(aged, None)
                miniplan[i].attached_audio = msgs_tosend[i]['Audio']
                miniplan[i].attached_media = msgs_tosend[i]['Media']
                miniplan[i].URL = msgs_tosend[i]['URL']
                miniplan[i].channel = msgs_tosend[i]['Channel']
                miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'],
                                                                 msgs_tosend[i]['URL'])
                i += 1
            c += 1

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def scheduleEquallyDividedPeriod(request, resource, template, aged):
    '''
    Returns the miniplan with the temporal interval between the msgs divided equally
    :param request: a request class
    :param template: a template class
    :param aged: a user class
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not datetime:
        times = convertDatetime(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = timedelta(days=template.period * 7)

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax
    step_send_msg = valid_interval / nmsg

    # creates miniplan that is a list of messages
    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, None, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    # for nmsg fill the miniplan msgs
    date = startime
    for i in range(0, lenloop):
        miniplan[i].date = date.date()
        miniplan[i].time = scheduleHour(aged, None)
        miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'], msgs_tosend[i]['URL'])
        miniplan[i].attached_audio = msgs_tosend[i]['Audio']
        miniplan[i].attached_media = msgs_tosend[i]['Media']
        miniplan[i].URL = msgs_tosend[i]['URL']
        miniplan[i].channel = msgs_tosend[i]['Channel']

        date += step_send_msg

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def scheduleLogarithmic(request, resource, template, aged):
    '''
    Returns the miniplan scheduled with more frequency at the end of the interval
    It divides the interval for every msg with logaritmic growth:1 1/2 1/3 1/4
    Check on period(valid weeks): if request interval is larger that period then user period as interval
    Last message always sent the day before the event
    :param request: a request class
    :param template: a template class
    :param aged: a user class
    :return: a miniplan that is a list of messages class with all the fields completed
    '''
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not datetime:
        times = convertDatetime(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = timedelta(days=template.period * 7)
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    valid_interval = endtime - startime
    if valid_interval > period:
        valid_interval = period

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    valid_interval = timedelta(seconds=valid_interval.total_seconds())
    for i in range(0, lenloop):
        date = endtime - valid_interval

        miniplan[i].date = date.date()

        miniplan[i].time = scheduleHourFromDate(aged, date).time()

        '''
        # messages = json.load(urllib2.urlopen('http://..../endpoint/getResource/' + request.resource_id))
        '''

        miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'], msgs_tosend[i]['URL'])

        miniplan[i].attached_audio = msgs_tosend[i]['Audio']
        miniplan[i].attached_media = msgs_tosend[i]['Media']
        miniplan[i].URL = msgs_tosend[i]['URL']
        miniplan[i].channel = msgs_tosend[i]['Channel']

        valid_interval = timedelta(seconds=valid_interval.total_seconds() / (i + 2))

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def schedulePeriodic(request, resource, template, aged):
    print "Schedule Day"
    errors = {}

    if type(request.from_date) is not datetime:
        times = convertDatetime(request, template, resource)
        startime = times[0]
        endtime = times[1]
        period = times[2]
        expirationtime = times[3]
    else:
        startime = request.from_date
        endtime = request.to_date
        period = timedelta(days=template.period * 7)
        expirationtime = resource.to_date
        if expirationtime == None:
            expirationtime = endtime

    valid_interval = endtime - startime
    if valid_interval > period:
        endtime = startime + period

    if template.nmsgmin != template.nmsgmax:
        nmsg = rnd.randrange(template.nmsgmin, template.nmsgmax + 1)
    else:
        nmsg = template.nmsgmax

    miniplan = [Message(count, aged.aged_id, intervention_session_id=1) for count in xrange(nmsg)]

    channels = getChannelsAvailable(template, aged)

    with open('csv/prova_import_messages.csv') as csvmessages:
        messages = csv.DictReader(csvmessages)
        msgs_tosend = getListMessages(messages, nmsg, resource, channels)

    er = checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, len(msgs_tosend))
    errors = er[0]
    miniplan = er[1]
    if er[2]:
        endtime = er[3]
    else:
        return errors, miniplan

    day_of_event = mapDay(resource.on_day)
    if day_of_event == None:
        errors['ErrorNoDay'] = 'Error no day specified for periodic messages'
        miniplan = []
        return errors, miniplan

    # length of the loop depending on the msgs found
    if len(msgs_tosend) < nmsg:
        lenloop = len(msgs_tosend)
    else:
        lenloop = nmsg

    c = 0
    i = 0
    current_date = startime.date()
    while current_date < endtime.date():
        if current_date.weekday() == day_of_event - 1:
            if c % int(resource.every) == 0:
                if i > lenloop:
                    break
                miniplan[i].date = current_date
                miniplan[i].time = scheduleHour(aged, None)
                miniplan[i].attached_audio = msgs_tosend[i]['Audio']
                miniplan[i].attached_media = msgs_tosend[i]['Media']
                miniplan[i].URL = msgs_tosend[i]['URL']
                miniplan[i].channel = msgs_tosend[i]['Channel']
                miniplan[i].message_text = generate_message_text(aged, msgs_tosend[i]['Text'],
                                                                 msgs_tosend[i]['URL'])
                i += 1
            c += 1

        current_date += timedelta(days=1)

    miniplan = checkMsgsOneDay(miniplan, endtime)

    return errors, miniplan


def checkForErrors(errors, endtime, expirationtime, startime, miniplan, nmsg, msgs_tosend_len):
    if expirationtime != None:
        if endtime > expirationtime:
            endtime = expirationtime
            errors['ErrorEndtime'] = 'Endtime: spostato perchè resource finisce prima della data settata come endtime'
            return errors, miniplan, True, endtime
        elif startime > expirationtime:
            errors['ErrorExpiration'] = 'ERROR: start date dopo expiration date resource'
            return errors, miniplan, False

    if msgs_tosend_len == 0:
        errors['ErrorZeroMsg'] = 'Error: zero messaggi compatibili'
        miniplan = []
        return errors, miniplan, False

    if msgs_tosend_len < nmsg:
        errors['ErrorLessMsg'] = 'Numero di messaggi compatibili trovati minore del numero di messaggi da mandare'

    return errors, miniplan, True, endtime
