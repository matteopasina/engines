#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, urllib2
from datetime import datetime, timedelta
from operator import attrgetter
from controller.Json_manager import mapMessage, encodePlan
from model.Message import Message
import random as rnd
import csv
import math


def checkMsgDay(sorted_messages):
    current_day = sorted_messages[0].date
    msg_this_day = [sorted_messages[0]]
    max_msgs_day = 5
    tot_msg = len(sorted_messages)
    user_pref = '0'

    for im in range(1, tot_msg):
        if sorted_messages[im].date == current_day:
            msg_this_day.append(sorted_messages[im])

        if sorted_messages[im].date != current_day:
            updated_times = checkMsgsPerHour(msg_this_day, user_pref)
            updated_times.reverse()
            for i in range(im - len(updated_times), im):
                sorted_messages[i] = updated_times.pop()
                sorted_messages[i].date = sorted_messages[i].date.date()
                sorted_messages[i].time = sorted_messages[i].time.time()
            current_day = sorted_messages[im].date
            msg_this_day = [sorted_messages[im]]

        if len(msg_this_day) > max_msgs_day:
            msg_this_day.pop()
            secondindex = im
            while sorted_messages[secondindex].date == current_day:
                sorted_messages[secondindex].date = sorted_messages[secondindex].date + timedelta(days=1)
                secondindex += 1
                if secondindex >= tot_msg:
                    break

            updated_times = checkMsgsPerHour(msg_this_day, user_pref)
            updated_times.reverse()
            for i in range(im - len(updated_times), im):
                sorted_messages[i] = updated_times.pop()
                sorted_messages[i].date = sorted_messages[i].date.date()
                sorted_messages[i].time = sorted_messages[i].time.time()
            current_day = sorted_messages[im].date
            msg_this_day = [sorted_messages[im]]

        if sorted_messages[im] is sorted_messages[-1]:
            updated_times = checkMsgsPerHour(msg_this_day, user_pref)
            updated_times.reverse()
            for i in range(im - len(updated_times) + 1, im + 1):
                sorted_messages[i] = updated_times.pop()
                sorted_messages[i].date = sorted_messages[i].date.date()
                sorted_messages[i].time = sorted_messages[i].time.time()


def checkMsgsPerHour(messages_same_day, pref=None):
    '''
    Schedules the messages in the same day to have at least one hour between them
    :param messages_same_day: a list with the messages in the same day
    :return: the list with the updated times
    '''
    for i in range(1, len(messages_same_day)):
        if messages_same_day[i].time - messages_same_day[i - 1].time < timedelta(hours=1):
            messages_same_day = scheduleMessagesInDay(messages_same_day, pref)
            return messages_same_day

    return messages_same_day


def scheduleMessagesInDay(messages_same_day, pref=None):
    '''
    Evenly distributes the number of messages in the interval set by the pref param
    :param messages_same_day: the messages in a day
    :param pref: user preferences for the time to send the messages
    :return: the messages distributed
    '''

    begin = 8
    interval = 12 / float(len(messages_same_day))
    min_to_rand = 60

    if pref == '1':
        begin = 12
        interval = 8 / float(len(messages_same_day))
        min_to_rand = 40
    if pref == '0':
        interval = 4 / float(len(messages_same_day))
        min_to_rand = 20

    beginoftheworld = datetime.strptime('1900-01-01', '%Y-%m-%d')
    minutes = str(rnd.randrange(0, 59))
    messages_same_day[0].time = datetime.strptime(str(begin) + ':' + minutes, '%H:%M').time()
    messages_same_day[0].time = datetime.combine(beginoftheworld.date(), messages_same_day[0].time)

    for i in range(1, len(messages_same_day)):
        hours = math.modf(begin + i * interval)
        minutes = hours[0] * 60
        minutes = rnd.randrange(0, min_to_rand) + minutes
        h = hours[1]

        if minutes > 60:
            h += 1
            minutes -= 60
        messages_same_day[i].time = datetime.strptime(str(int(h)) + ':' + str(int(minutes)), '%H:%M').time()
        messages_same_day[i].time = datetime.combine(beginoftheworld.date(), messages_same_day[i].time)

    return messages_same_day


def launch_engine_two():
    errors = {}
    id_user = 0
    all_messages = []
    # miniplans = json.load(urllib2.urlopen('https://api/c4a-DBmanager/getMiniplans/id_user=' + id_user))
    with open('csv/prova_miniplans.csv') as csvmessages:
        miniplans = csv.DictReader(csvmessages)
        for m in miniplans:
            for key, value in json.loads(m['miniplan_body']).iteritems():
                all_messages.append(mapMessage(value))

    sorted_messages = sorted(all_messages, key=attrgetter('date', 'time'))

    checkMsgDay(sorted_messages)

    return encodePlan(errors, sorted_messages)
