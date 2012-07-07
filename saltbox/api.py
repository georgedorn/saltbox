# -*- coding: utf-8 -*-
"""
    Copyright 2012 Gordon Morehouse <gordon@morehouse.me>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.

    API, in pseudocode:

    create(identifier, key, data) creates record and returns digest.
    verify(identifier, key, data) verifies record and returns True (verified) or False.
    update(identifier, key, data, new_data) updates record and returns digest iff data is verified.
    delete(identifier, key, data) deletes record and returns digest iff data is verified.
    delete(identifier, key) deletes record and returns digest iff identifier is authorized. @todo
"""


class SaltboxInterface(object):
    """
    An API definition for interacting with Saltbox.

    The Saltbox class is composed of a SaltboxInterface derived class and a
    SaltboxMessenger derived class.
    """

    def create(cls, identifier, key, data):
        """
        Create a saltbox record.

        @return boolean True if successful
        @raise SaltboxException
        """
        raise NotImplementedError


    def verify(cls, identifier, key, data):
        """
        Verify a saltbox record.

        @return boolean True if data is verified against existing record, False if mismatch/no record.
        @raise SaltboxException
        """
        raise NotImplementedError


    def update(cls, identifier, key, data, new_data):
        """
        Update a saltbox record with new data.

        @return boolean True if data verifies vs. existing record and update successful, False if mismatch/no record.
        @raise SaltboxException
        """
        raise NotImplementedError


    def delete(cls, identifier, key, data=None):
        """
        Delete a saltbox record.

        @return boolean True iff (data != None and verifies, or data == None and identifier authorized to delete @todo )
        @raise SaltboxException
        """
        raise NotImplementedError


class SaltboxMessenger(object):
    """
    An interface for the low-level workings of SaltboxMessage handling.

    The Saltbox class is composed of a SaltboxInterface derived class and a
    SaltboxMessenger derived class.

    One must always at least override the set of (_send_request, _handle_response)
    or (_handle_request, _send_response) in derived classes.
    """

    def _send_request(self, msg):
        """
        Send a SaltboxRequest to the storage entity.

        @param msg SaltboxRequest
        @return boolean
        @raise SaltboxException @todo ??
        """
        raise NotImplementedError


    def _send_response(self, msg):
        """
        Send a SaltboxResponse to requester.

        @param msg SaltboxResponse
        @raise SaltboxException @todo ??
        """
        raise NotImplementedError


    def _handle_request(self, msg):
        """
        Unpack and deal with a SaltboxRequest.

        @param msg SaltboxRequest
        @raise SaltboxException @todo ??
        """


    def _handle_response(self, msg):
        """
        Unpack a SaltboxResponse and return nicely.

        @param msg SaltboxResponse
        @return boolean
        @raise SaltboxException An exception containing message from server if something broke. @todo ??
        """
        raise NotImplementedError


def build_saltbox(interface_klass, messenger_klass):
    """
    Factory function which hands back a Saltbox class composed of the
    given SaltboxInterface and SaltboxMessenger.
    """
    errors = []
    if not isinstance(interface_klass, SaltboxInterface):
        errors[] = 'interface_klass must inherit from SaltboxInterface'
    if not isinstance(messenger_klass, SaltboxMessenger):
        errors[] = 'messenger_klass must be a SaltboxMessenger'

    if errors:
        if len(errors) == 2:
            error = "%s and %s" % (errors[0], errors[1])
        else:
            error = errors[0]
        raise SaltboxException(error)

    class Saltbox(interface_klass, messenger_klass):
        pass

    return Saltbox
