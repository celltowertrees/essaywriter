import requests
from bs4 import BeautifulSoup
# from sys import argv

# script, file = argv
# essay = open(file, 'r+')


# Grabs what we want from the twitter request

def extract(stuff, list):
    print "Extracting..."
    soup = BeautifulSoup(stuff)
    
    for t in soup.find_all('p', class_="tweet-text"):
        for a in t.find_all('a'):
            a.decompose()
        
        words = t.text
        list.append(words)


# Takes the last 5 words of each tweet and creates a new list of those sentences
    
def organize(l):
    new_l = []
    print "Organizing..."

    for i in l:
        sentence = []
        words = i.split()
        chopped = words[-5:]
        
        for w in chopped:
            sentence.append(w)
    
        new_l.append(" ".join(sentence))

    return new_l
        

# Fetches tweets from web scrape, and returns them as complete package

def get_tweets(tag):
    print "Getting Tweets..."
    data = []

    r = requests.get('https://twitter.com/search?q=' + tag + '&src=typd')
    content = r.text
    
    extract(content, data)
    print " ".join(organize(data))


get_tweets('bomb')




# later to be used for storing tweets

def add(to_essay):
    prompt = get_prompt(to_essay)
    new_sentence = raw_input(prompt + " ")

    to_essay.write(" " + new_sentence)
    to_essay.close()