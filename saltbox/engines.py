# -*- coding: utf-8 -*-
"""
    Copyright 2012 Gordon Morehouse <gordon@morehouse.me>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
"""

from sqlalchemy import schema, types

from saltbox import SaltboxInterface, SaltboxStorageEngine


class AlchemyStorage(SaltboxStorageEngine):
    """
    Class for SQLAlchemy 'back end' (@todo ??? running on 'the same box'?)
    
    This should take a DSN and just use anything SQLAlchemy supports.
    """
   
    def __init__(self):
        saltbox_table = schema.Table('page', metadata,
            schema.Column('owner', types.String(255), primary_key=True),    # default? @todo
            schema.Column('key', types.String(255), primary_key=True),
            schema.Column('digest', types.String(4096), default='')
        )
        
        from sqlalchemy.engine import create_engine
        
        engine = create_engine('sqlite:///:memory:', echo=True)
        metadata.bind = engine
        
        metadata.create_all(checkfirst=True)
    

#class SQLiteStorage(AlchemyStorage):
    #pass


#class MySQLStorage(AlchemyStorage):
    #pass


#class PostgreSQLStorage(AlchemyStorage):
    #pass


############## pipe dreams...

class POSIXPasswdStorage(SaltboxStorageEngine):
    pass


class MemcacheStorage(SaltboxStorageEngine):
    pass


class PAMStorage(SaltboxStorageEngine):
    pass


class DotNetBullshitStorage(SaltboxStorageEngine):
    pass

    