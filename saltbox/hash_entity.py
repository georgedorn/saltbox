# -*- coding: utf-8 -*-
"""
    Copyright 2012 Gordon Morehouse <gordon@morehouse.me>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
"""

from passlib.context import CryptContext

from saltbox import SaltboxException


class HashEntity(object):
    """
    Represents a primary key (identifier) and an associated digest (aka hash,
    which is a reserved word in Python).  Also stores data for convenience,
    though it's not ever saved.

    @todo needs work on what inconsistent (is_verified = False) states it
    can and can't exist in, etc.
    """
    key = None
    data = None
    digest_str = None
    cryptcontext = None

    def __init__(self, key, data=None, digest=None, cryptcontext=None):
        if cryptcontext is None:
            self.cryptcontext = CryptContext(schemes=['ldap_pbkdf2_sha512'],
                                             default='ldap_pbkdf2_sha512',
                                             all__vary_rounds=0.1)
        else:
            self.cryptcontext = cryptcontext

        if data is not None and digest is not None:
            self.data = data

            # okay, first verify the digest we got to check for a mismatch --
            # we have to use the passlib verify, in case an older scheme was
            # used, instead of just calculating the new digest and comparing
            # strings
            if not self.cryptcontext.verify(data, digest):
                raise SaltboxException("Given data doesn't verify with given digest")

            # if self.digest_str isn't our default hash scheme, recalculate it
            # and save it as default hash scheme
            # @todo this always recalculates; wasteful
            self.digest()

        elif data is not None:
            self.data = data
            self.digest()

        elif digest is not None:
            self.digest_str = digest


    def __str__(self):
        my_data = self.data or ''
        my_digest = self.digest_str or ''

        return "HashEntity: data length %d, digest '%s'" % (len(my_data), my_digest)


    def digest(self, data=None):
        """
        Calculates the digest of self.data and sets self.digest_str.

        @param data If set, replaces self.data before calculating digest.
        @return None
        """
        self.data = data or self.data

        if self.data is None:
            raise SaltboxException('Cannot calculate digest with no data.')

        self.digest_str = self._calculate_digest()


    def verify(self, data=None):
        """
        Calculates the digest of some data and compares to self.digest_str.  If the data
        argument is None, self.data will be verified against self.digest_str.

        @param data If set, replaces self.data before verifying digest.
        @return boolean True if the digest of self.data matches self.digest_str, else False.
        """
        check_data = data or self.data

        if check_data is None:
            raise SaltboxException('Cannot verify digest with no data.')

        if self.digest_str is None:
            raise SaltboxException('Cannot verify an empty digest.')

        return self._verify_digest(check_data)


    @property
    def is_verified(self):
        return self.verify()


    def clear(self):
        """
        Clears all data variables, but not the cryptcontext.
        """
        self.key = None
        self.data = None
        self.digest_str = None


    def save(self):
        assert self.is_verified, "Cannot save HashEntity which doesn't verify."
        raise NotImplementedError   # @todo


    def _calculate_digest(self, data=None):
        data = data or self.data
        return self.cryptcontext.encrypt(data)


    def _verify_digest(self, data=None):
        data = data or self.data
        return self.cryptcontext.verify(data, self.digest_str)
