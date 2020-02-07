# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from AD_VINA.AD_VINAImpl import AD_VINA
from AD_VINA.AD_VINAServer import MethodContext
from AD_VINA.authclient import KBaseAuth as _KBaseAuth


3dnf_clean_pdb = "37778/2/1"
test_compound_set = "37778/4/2"






class AD_VINATest(unittest.TestCase):

    def test(self):
        params = {
            "pdb_refs": [3dnf_clean_pdb],
            'ligand_list_ref': test_compound_set
            }
        ret = self.serviceImpl.ad_vina(self.ctx, params)

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('AD_VINA'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'AD_VINA',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = AD_VINA(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def _test_static_AD_VINA(self):
        inparams = {
            "receptor" : "lck_small.pdbqt",
            "ligand" : "lck-active-26.pdbqt",
            "center" :  "18.273, 44.681, 80.351",
            "size" : "50, 50, 50",
            "outname" : "out.pdbqt"
        }
        ret = self.getImpl().ad_vina(self.getContext(), inparams)[0]



        


