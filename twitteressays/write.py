import sys
import requests
import re
from bs4 import BeautifulSoup
from pymarkovchain import MarkovChain
from random import choice, shuffle


class Writer(object):

    def __init__(self, keyword):
        self.keyword = keyword


    def extract_links(self, tag):
        """ Find source links in article """
        r = requests.get('http://en.wikipedia.org/wiki/' + tag)
        # TODO: find a more flexible way of searching Wikipedia
        soup = BeautifulSoup(r.text)
        refs = soup.find('ol', class_="references")
        links = []
        try:
            for a in refs.find_all('a', class_="external"):
                print "Extracting links"
                url = a['href']
                links.append(url)
                shuffle(links)
                # Shuffle list and get last 5 links (don't want to overdo it at this time)
                return links[-5:]

        except AttributeError:
            print "There are no sources for the keyword '%s'. Wikipedia probably didn't have an article for it." % self.keyword

    
    def generateModel(self, essay):
        """ Generate a Markov chain based on retrieved strings """
        mc = MarkovChain()
        mc.generateDatabase(essay)
        result = r''

        for i in range(0, 10):
            # Create 10 sentences
            sentence = mc.generateString()
            result += sentence.capitalize() + '. '
            print "Generating Model"

        return result


    def read_articles(self, link_list):
        """ Request articles, inspect markup for any important strings, and return them, cleaned """
        info = ''

        def get_tag(tag):
            # Whatever tag is passed, the text inside of it is cleaned up and inserted into a bigger string
            if soup.find(tag):
                tag_text = ''
                print "Reading %s" % tag
                for i in soup.find_all(tag):
                    clean = i.text.strip()
                    clean = re.sub('[@#$"~+<>():/\{}_]', '', clean)
                    tag_text += clean
                return tag_text
            else:
                pass

        for url in link_list: 
            # Each URL gets its own string of returned text
            full_article = ''

            try:
                r = requests.get(url, timeout=5)
                print "Opening article"
                soup = BeautifulSoup(r.text)
                
                if get_tag('p'):
                    full_article += get_tag('p')
                    print "Got a tag."
                else: 
                    pass

            except requests.exceptions.RequestException:
                print "Request Error!"

            info += full_article

        return info


    # Generates essay

    def write(self):
        """ Generator """
        links = self.extract_links(self.keyword)
        articles = self.read_articles(links)
        return self.generateModel(articles)



#------------OLD SHIT----------------

def extract_tweets(tag):
    r = requests.get('https://twitter.com/search?q=' + tag + '&src=typd')
    soup = BeautifulSoup(r.text)
    text = ''
    
    for t in soup.find_all('p', class_="tweet-text"):
        for a in t.find_all('a'):
            a.decompose()
        text += t.text + ' '

    return text


def formatString(string):
    text = string.replace('"', '')
    return text

