# import sys
import requests
import re
import wikipedia
import nltk

from wikipedia.exceptions import WikipediaException, DisambiguationError
from bs4 import BeautifulSoup
from pymarkovchain import MarkovChain
from random import choice, shuffle


def soup_tag(tag, text):
    # Whatever tag is passed, the text inside of it is BeautifulSouped
    # and inserted into tag_text string
    soup = BeautifulSoup(text)
    if soup.body.find(tag):
        tag_text = ''
        print "Reading..."
        for i in soup.find_all(tag):
            clean = i.text
            clean = re.sub('[@#$"~+<>():/\{}_]', '', clean).strip()
            tag_text += clean + ' '
        return tag_text
    else:
        pass


def read_link_list(link_list):
    # Requests from a list of URLs.
    info = ''
    for url in link_list:
        # Each URL gets its own string of returned text
        full_article = ''
        try:
            r = requests.get(url, timeout=5)
            print "Opening article"
            if soup_tag('p', r.text):
                full_article += soup_tag('p', r.text)
            else:
                pass
        except requests.exceptions.RequestException:
            print "Request Error!"
        except requests.packages.urllib3.exceptions.LocationParseError:
            print "Location Parse Error!"
        info += full_article
    return info


class MarkovWriter(object):
    def __init__(self, text):
        self.text = text

    def generateModel(self):
        """ Generate a Markov chain based on retrieved strings. """

        mc = MarkovChain()
        mc.generateDatabase(self.text)
        result = r''

        print "Generating:"

        for i in range(0, 10):
            print "Sentence %d" % i
            # Create 10 sentences
            sentence = mc.generateString()
            result += sentence.capitalize() + '. '

        return result


class PosSorter(object):
    def __init__(self, text):
        self.text = text

    def analyze(self):
        """ Takes a collection of adjectives using NLTK tokenizer. """

        tokens = nltk.word_tokenize(self.text)
        adjectives = []
        nouns = []
        verbs = []
        print "Sorting words..."

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


class Tweets(object):
    def __init__(self, tag):
        self.tag = tag

    def extract_tweets(self):
        r = requests.get('https://twitter.com/search?q=' + self.tag + '&src=typd')
        soup = BeautifulSoup(r.text)
        text = ''
        for t in soup.find_all('p', class_="tweet-text"):
            for a in t.find_all('a'):
                a.decompose()
            text += t.text + ' '
        return text


class Wikipedia(object):
    def __init__(self, tag):
        self.tag = tag

    def extract_wikipedia_sources(self):
        # Find source links in a Wikipedia article. Returns a link list.
        r = wikipedia.search(self.tag)
        print "Wikipedia is doing something!"
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
                result = read_link_list(refs[-5:])
                print "Wikipedia returned the result"
                return result
            elif len(r) == 1:
                refs = wikipedia.WikipediaPage(r).references
                result = read_link_list(refs[-5:])
                print "Wikipedia returned the result"
                return result
            else:
                raise NameError('TRY A LITTLE BIT HARDER')


class TextFile(object):
    def __init__(self, file_, tag):
        self.file_ = file_
        self.tag = tag
        # Doesn't actually do anything with the tag yet.

    def read_text(self):
        with open(self.file_, "r") as file_obj:
            words = file_obj.read()
            return words

    def extract_links_text(self):
        # Reads from a text file of source links.
        links = []
        with open(self.file_, "r") as file_obj:
            lines = file_obj.read()
            try:
                links = lines.split('\n')
                for line in lines:
                    links.append(line)
            except AttributeError:
                print "No."
        result = read_link_list(links)
        return result

# class Craigslist(object):
