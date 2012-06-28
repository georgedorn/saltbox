# -*- coding: utf-8 -*-
"""
    Copyright 2012 Gordon Morehouse <gordon@morehouse.me>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
"""


class SaltboxException(Exception):
    pass


class BaseHashEntity(object):
    """
    Represents a primary key (identifier) and an associated "digest" (aka hash,
    which is a reserved word in Python).
    """
    key = None
    data = None
    digest = None

    def __init__(self, key, data=None, digest=None):
        """Constructor."""
        if data is not None:
            self.data = data
            self.digest()
        elif digest is not None:
            self.digest = digest
        elif data is not None and digest is not None:
            self.data = data
            self.digest = digest


    def digest(self, data=None):
        """
        Calculates the digest of self.data and sets self.digest.

        @param data If set, replaces self.data before calculating digest.
        @return None
        """
        self.data = data or self.data

        if self.data is None:
            raise SaltboxException('Cannot calculate digest with no data.')

        self.digest = self._calculate_digest()


    def verify(self, data=None):
        """
        Calculates the digest of self.data and compares to self.digest.

        @param data If set, replaces self.data before verifying digest.
        @return boolean True if the digest of self.data matches self.digest, else False.
        """
        self.data = data or self.data

        if self.data is None:
            raise SaltboxException('Cannot verify digest with no data.')

        if self.digest is None:
            raise SaltboxException('Cannot verify empty digest.')

        return self.digest == self._calculate_digest()


    def clear(self):
        """
        Clears all member variables.
        """
        self.key = None
        self.data = None
        self.digest = None


    def _calculate_digest():
        raise NotImplementedError

