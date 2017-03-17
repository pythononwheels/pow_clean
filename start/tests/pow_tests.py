#
# Pow Default Tests
# 
# run:      pytest -q pow_tests.py
# on osx:   pytest -k-notonosx pow_tests.py
import pytest

MODELNAME = "pow_test_model"
class TestClass:
    @pytest.mark.notonosx
    def test_server(self):
        """ test if server starts"""
        from multiprocessing import Process
        import {{appname}}.server
        import requests
        import {{appname}}.config as cfg
        import time
        p = Process(target={{appname}}.server.main)
        p.start()
        testurl=cfg.myapp["base_url"] + ":" + str(cfg.server_settings["port"]) + "/test/12"  
        r = requests.get(testurl)
        p.terminate()
        assert int(r.text)==12
        
    def test_generate_model(self):
        """ test if sql model is generated"""
        import {{appname}}.generate_model as gm
        import uuid
        import os.path
        ret = gm.generate_model(MODELNAME, "sql", appname="{{appname}}")
        # generate model returns true in case of success
        assert ret is True
        assert os.path.exists(os.path.normpath("../models/sql/" + MODELNAME + ".py"))

    def test_model_type(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        from {{appname}}.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        assert isinstance(m, PowTestModel)

    def test_sql_dbsetup(self):
        """ test the setup of the alembic environment """
        import {{appname}}.init_migrations
        import os
        os.chdir("..")
        r = {{appname}}.init_migrations.init_migrations()
        assert r == True
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
    def test_sql_migration(self):
        """ test the setup of the alembic environment """
        import {{appname}}.init_migrations
        import os
        os.chdir("..")
        r = {{appname}}.init_migrations.init_migrations()
        assert r == True
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

    def test_model_insert(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        from {{appname}}.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        m.name = "Testname"
        
        assert isinstance(m, PowTestModel)



