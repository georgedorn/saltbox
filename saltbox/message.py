# -*- coding: utf-8 -*-
"""
    Copyright 2012 Gordon Morehouse <gordon@morehouse.me>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
"""

class SaltboxMessage(object):
    owner = None
    nonce = None
    values = { }

    def __init__(self, owner, nonce, key=None, data=None, digest=None):
        self.owner = owner
        self.nonce = nonce
        self.values['key'] = key
        self.values['data'] = data
        self.values['digest'] = digest


class SaltboxResponse(SaltboxMessage):

    def __init__(self, response, message=None):
        self.values['response'] = response
        self.values['message'] = message
        super(SaltboxResponse, self).__init__()


class SaltboxRequest(SaltboxMessage):

    def __init__(self, request):
        self.values['request'] = request
        super(SaltboxRequest, self).__init__()
