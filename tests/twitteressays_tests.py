from nose.tools import *
from twitteressays import app
import os


TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'test.txt')


class Test_Engine():
    
    def setup(self):
        self.list = []
        self.stuff = open(TESTDATA_FILENAME, 'r')

    def test_extract(self):
        app.extract(self.stuff, self.list)
        assert_equal(self.list, [u"My biggest issue with Duck Dynasty is that it's perpetuating our acceptance of  garbage as art."])

    def test_organize(self):
        app.extract(self.stuff, self.list)
        newlist = app.organize(self.list)
        assert_equal(newlist, [u'acceptance of garbage as art.'])
    
    def tearDown(self):
        self.stuff.close()
    
