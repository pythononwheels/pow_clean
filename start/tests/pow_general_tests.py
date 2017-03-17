#
# Pow Default Tests
# 
# run: pytest -q pow_tests.py
#


MODELNAME = "pow_test_model"
class TestClass:
    def test_server(self):
        """ test if server starts"""
        from multiprocessing import Process
        import powtest.server
        import requests
        import powtest.config as cfg
        import time
        p = Process(target=powtest.server.main)
        p.start()
        testurl=cfg.myapp["base_url"] + ":" + str(cfg.server_settings["port"]) + "/test/12"  
        r = requests.get(testurl)
        p.terminate()
        assert int(r.text)==12
        
    def test_generate_model(self):
        """ test if sql model is generated"""
        import powtest.generate_model as gm
        import uuid
        import os.path
        ret = gm.generate_model(MODELNAME, "sql", appname="powtest")
        # generate model returns true in case of success
        assert ret is True
        assert os.path.exists(os.path.normpath("../models/sql/" + MODELNAME + ".py"))

    def test_model_type(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        from powtest.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        assert isinstance(m, PowTestModel)

    def test_sql_dbsetup(self):
        """ test the setup of the alembic environment """
        import powtest.init_migrations
        import os
        os.chdir("..")
        r = powtest.init_migrations.init_migrations()
        assert r == True
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
     def test_sql_migration(self):
        """ test the setup of the alembic environment """
        import powtest.init_migrations
        import os
        os.chdir("..")
        r = powtest.init_migrations.init_migrations()
        assert r == True
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

    def test_model_insert(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        from powtest.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        m.name = "Testname"
        
        assert isinstance(m, PowTestModel)



