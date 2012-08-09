# -*- coding: utf-8 -*-
"""
    Copyright 2012 Gordon Morehouse <gordon@morehouse.me>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.

    API:
    
    owner == string identifying to which caller (program, service) the key-data pair belongs.
    key == unique primary key for the record; anything that can be made a string.
    data, new_data == data to be salted, hashed and then operated upon (created, verified, updated, deleted).

    create(owner, key, data) creates record and returns digest.
    verify(owner, key, data) verifies record and returns True (verified) or False.
    update(owner, key, data, new_data) updates record and returns digest iff data is verified.
    delete(owner, key, data) deletes record and returns digest iff data is verified.
    delete(owner, key) deletes record and returns digest iff owner is authorized. @todo
"""


class SaltboxInterface(object):
    """
    An API definition for interacting with Saltbox.  (Akin to a Java Interface,
    if that makes more sense for some folks who scratch their heads at the
    'raise NotImplementedError' in every method.)

    The usable Saltbox class will be composed of a class derived from
    SaltboxInterface and a class derived from SaltboxStorageEngine.
    """

    def create(cls, owner, key, data):
        """
        Create a saltbox record.

        @return boolean True if successful
        @raise SaltboxException
        """
        raise NotImplementedError


    def verify(cls, owner, key, data):
        """
        Verify a saltbox record.

        @return boolean True if data is verified against existing record, False if mismatch/no record.
        @raise SaltboxException
        """
        raise NotImplementedError


    def update(cls, owner, key, data, new_data):
        """
        Update a saltbox record with new data.

        @return boolean True if data verifies vs. existing record and update successful, False if mismatch/no record.
        @raise SaltboxException
        """
        raise NotImplementedError


    def delete(cls, owner, key, data=None):
        """
        Delete a saltbox record.

        @return boolean True iff (data != None and verifies, or data == None and owner authorized to delete @todo )
        @raise SaltboxException
        """
        raise NotImplementedError


class SaltboxStorageEngine(object):
    """
    An interface for the low-level workings of SaltboxMessage handling.

    The usable Saltbox class will be composed of a class derived from
    SaltboxInterface and a class derived from SaltboxStorageEngine.

    One must always at least override the set of (_send_request, _handle_response)
    or (_handle_request, _send_response) in derived classes.
    
    @todo split to SaltboxServer and SaltboxClient? do we care?
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
    given SaltboxInterface and SaltboxStorageEngine.
    """
    errors = []
    if not isinstance(interface_klass, SaltboxInterface):
        errors[] = 'interface_klass must inherit from SaltboxInterface'
    if not isinstance(messenger_klass, SaltboxStorageEngine):
        errors[] = 'messenger_klass must be a SaltboxStorageEngine'

    if errors:
        if len(errors) == 2:
            error = "%s and %s" % (errors[0], errors[1])
        else:
            error = errors[0]
        raise SaltboxException(error)

    class Saltbox(interface_klass, messenger_klass):
        pass

    return Saltbox
