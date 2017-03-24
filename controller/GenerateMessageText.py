#!/usr/bin/python
# -*- coding: utf-8 -*-
import random


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
