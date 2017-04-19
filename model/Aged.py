#!/usr/bin/python
# -*- coding: utf-8 -*-

class Aged:
    def __init__(self, aged_id, name="", surname="", channels="SMS", hour_preference=None, message_frequency=None,
                 communication_style=None, topics=None):
        self.aged_id = aged_id
        self.name = name
        self.surname = surname
        self.channels = channels
        self.hour_preference = hour_preference
        self.message_frequency = message_frequency
        self.communication_style = communication_style
        self.topics = topics
