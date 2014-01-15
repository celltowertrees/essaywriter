import sys
import requests
import re
from bs4 import BeautifulSoup
from pymarkovchain import MarkovChain
from random import choice, shuffle


# Uses a Markov chain to rearrange words
    
def generateModel(essay):
    mc = MarkovChain()
    mc.generateDatabase(essay)
    result = r''

    for i in range(0, 10):
        print "Generating Model"
        sentence = mc.generateString()
        result += sentence.capitalize() + '. '

    return result


#Scrapes Wikipedia article for references

def extract_links(tag):
    r = requests.get('http://en.wikipedia.org/wiki/' + tag)
    soup = BeautifulSoup(r.text)
    refs = soup.find('ol', class_="references")
    links = []

    for a in refs.find_all('a', class_="external"):
        print "Extracting links"
        url = a['href']
        links.append(url)

    shuffle(links)
    return links[-5:]


# Reads articles from a list of URLs

def read_articles(link_list):
    info = ''

    def get_tag(tag):
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

def write(topic):
    links = extract_links(topic)
    articles = read_articles(links)
    print generateModel(articles)


write('North Korea')




#------------OLD SHIT----------------

# Scrapes tweets

def extract_tweets(tag):
    r = requests.get('https://twitter.com/search?q=' + tag + '&src=typd')
    soup = BeautifulSoup(r.text)
    text = ''
    
    for t in soup.find_all('p', class_="tweet-text"):
        for a in t.find_all('a'):
            a.decompose()
        text += t.text + ' '

    return text


# Formats tweets

def formatString(string):
    text = string.replace('"', '')
    return text

