#!/usr/bin/python
# -*- coding: utf-8 -*-

class User:
    def __init__(self, user_id, name="", channels="SMS", hour_preference=None):
        self.user_id = user_id
        self.name = name
        self.channels = channels
        self.hour_preference = hour_preference
