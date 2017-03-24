#!/usr/bin/python
# -*- coding: utf-8 -*-

class Template:
    def __init__(self, template_id, category="", title="", description="", nmsgmin=0, nmsgmax=0, period=0, channels=[], compulsory="No"):
        self.template_id = template_id
        self.category = category
        self.title = title
        self.description = description
        self.nmsgmin = nmsgmin
        self.nmsgmax = nmsgmax
        self.period = period
        self.channels = channels
        self.compulsory = compulsory
