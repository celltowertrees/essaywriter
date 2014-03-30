import sys
import requests
import re
import wikipedia
import nltk

from wikipedia.exceptions import WikipediaException, DisambiguationError
from bs4 import BeautifulSoup
from pymarkovchain import MarkovChain
from random import choice, shuffle


# TODO:
# Add more keyword options
# Separate into more modules with more options


class Writer(object):

    def __init__(self, keyword):
        self.keyword = keyword
        self.links = self.extract_links_wikipedia()

    def stripWords(words):
        text = string.replace('"', '')
        return text

    def extract_links_text(self, file):
        """
        Reads from a text file of source links.
        Returns the links in a list.
        """
        links = []

        with open(file, "r") as file_obj:
            lines = file_obj.read()

            try:
                links = lines.split('\n')
                for line in lines:
                    links.append(line)

            except AttributeError:
                print "No."

        return links

    def extract_links_wikipedia(self):
        """ Find source links in a Wikipedia article. """
        r = wikipedia.search(self.keyword)
        # requests.get('http://en.wikipedia.org/wiki/' + tag)

        if r:
            if len(r) > 1:
                shuffle(r)
                print "Shuffling"
                try:
                    refs = wikipedia.WikipediaPage(r[1]).references

                except (WikipediaException, DisambiguationError, KeyError):
                    print "Exception!"
                    refs = wikipedia.WikipediaPage(r[2]).references

            shuffle(refs)
            return refs[-5:]

        elif len(r) == 1:
            refs = wikipedia.WikipediaPage(r).references
            return refs[-5:]

        else:
            raise NameError('TRY A LITTLE BIT HARDER')

    def generateModel(self, essay):
        """ Generate a Markov chain based on retrieved strings. """

        mc = MarkovChain()
        mc.generateDatabase(essay)
        result = r''

        print "Generating:"

        for i in range(0, 10):
            print "Sentence %d" % i
            # Create 10 sentences
            sentence = mc.generateString()
            result += sentence.capitalize() + '. '

        return result

    def analyze(self, text):
        """ Takes a collection of adjectives using NLTK tokenizer. """

        tokens = nltk.word_tokenize(text)
        adjectives = []
        nouns = []
        verbs = []

        for word, pos in nltk.pos_tag(tokens):
            if pos in ['VB']:
                if word not in verbs:
                    verbs.append(word)
                else:
                    pass
            elif pos in ['JJ']:
                if word not in adjectives:
                    adjectives.append(word)
                else:
                    pass
            elif pos in ['NN']:
                if word not in nouns:
                    nouns.append(word)
                else:
                    pass

        return verbs, adjectives, nouns

    def read_articles(self, link_list):
        """
        Request articles,
        inspect markup for any important strings,
        and return them, cleaned
        """
        info = ''

        def get_tag(tag):
            # Whatever tag is passed, the text inside of it is cleaned up a
            # nd inserted into tag_text
            if soup.find(tag):
                tag_text = ''
                print "Reading..."
                for i in soup.find_all(tag):
                    clean = i.text
                    clean = re.sub('[@#$"~+<>():/\{}_]', '', clean).strip()
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
                else:
                    pass

            except requests.exceptions.RequestException:
                print "Request Error!"

            info += full_article

        return info

    # Generates essay
    def write(self):
        """ Generator """
        articles = self.read_articles(self.links)
        return self.analyze(articles)


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
