#!/usr/bin/python
# -*- coding: utf-8 -*-

class Request:
    def __init__(self, request_id, resource_id, template_id, user_id, category="", resource="", subjects="",
                 from_date=None, to_date=None):
        self.request_id = request_id
        self.resource_id = resource_id
        self.template_id = template_id
        self.user_id = user_id
        self.category = category
        self.resource = resource
        self.subjects = subjects
        self.from_date = from_date
        self.to_date = to_date
