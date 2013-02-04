# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Ralph Vigne, <ralph.vigne@cern.ch>, 2012

import json

from nose.tools import raises

from rucio.common import exception
from rucio.rse import rsemanager


class TestRseRepository():
    def test_storage_success(self):
        """ RSE (RSE): Repository => Using a defined storage """
        credentials = {}
        with open('etc/rse-accounts.cfg') as f:
            data = json.load(f)
        credentials['username'] = str(data['lxplus.cern.ch']['username'])
        credentials['password'] = str(data['lxplus.cern.ch']['password'])
        credentials['host'] = 'lxplus.cern.ch'
        self.storage = rsemanager.RSE('lxplus.cern.ch')
        self.storage.connect()
        self.storage.close()

    @raises(exception.RSENotFound)
    def test_storage_failure(self):
        """ RSE (RSE): Repository => RSENotFound Exception """
        rsemanager.RSE('not.existing')

    @raises(exception.RSENotFound)
    def test_storage_failure_mgr(self):
        """ RSE (RSE): Repository => RSENotFound Exception (Mgr) """
        mgr = rsemanager.RSEMgr()
        mgr.download('not_existing_rse', 'not_existing_file.raw')
