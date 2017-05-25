#!/usr/bin/python
# -*- coding: utf-8 -*-
import random


# OLD
def generate_message_text(user, main_text, url):
    '''
    Returns the text of the message
    :param user: user class to use user hour preference to choose the greeting and to use the name to substitute the variables
    :param main_text: text of the message to modify
    :return: the text of the message with the greetings and the variables
    '''
    complete_text = ''

    greetings = {
        None: ['Ciao,',
               'Hey,',
               'Salve,',
               'Ciao ' + user.name + '!Bella giornata, vero?',
               user.name + ', bella giornata!',
               user.name + ' come stai?',
               user.name + ',',
               'Ciao ' + user.name + ', cosa stai facendo?'],

        '1': ['Buonasera!',
              'Buon pomeriggio!',
              'Buonasera ' + user.name + '!',
              'Buon pomeriggio ' + user.name + '!'],

        '0': ['Buongiorno!',
              'Buon mattino!',
              'Buongiorno ' + user.name + '!',
              'Buon mattino ' + user.name + '!']}

    for greeting in greetings:
        if greeting == user.hour_preference:
            complete_text += (random.choice(greetings[greeting]))

    complete_text += ' ' + main_text
    complete_text += ' ' + url

    return complete_text


def buildMessage(aged, resourceMessage):
    '''
        Returns the text of the message
        :param aged: aged class to use user hour preference to choose the greeting and to use the name to substitute the variables
        :param resourceMessage: resourceMessage class
        :return: the text of the message with the greetings and the variables
        '''
    complete_text = ''

    greetings = {
        None: ['Ciao,',
               'Hey,',
               'Salve,',
               'Ciao ' + aged.name + '!Bella giornata, vero?',
               aged.name + ', bella giornata!',
               aged.name + ' come stai?',
               aged.name + ',',
               'Ciao ' + aged.name + ', cosa stai facendo?'],

        '1': ['Buonasera!',
              'Buon pomeriggio!',
              'Buonasera ' + aged.name + '!',
              'Buon pomeriggio ' + aged.name + '!'],

        '0': ['Buongiorno!',
              'Buon mattino!',
              'Buongiorno ' + aged.name + '!',
              'Buon mattino ' + aged.name + '!']}

    for greeting in greetings:
        if greeting == aged.hour_preference:
            complete_text += (random.choice(greetings[greeting]))

    complete_text += ' ' + resourceMessage.text
    complete_text += ' ' + resourceMessage.url

    return complete_text
