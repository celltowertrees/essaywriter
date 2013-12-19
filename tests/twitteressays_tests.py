from nose.tools import *
import twitteressays

def test_extract():
    list = []
    stuff = open(test.txt, 'r')
    assert_equal(extract(stuff, list), "My biggest issue with Duck Dynasty is that it&#39;s perpetuating our acceptance of garbage as art.")

def setup():
    print "SETUP!"
    
def teardown():
    print "TEAR DOWN!"
    
def test_basic():
    print "I RAN!"