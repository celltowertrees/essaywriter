import requests
from bs4 import BeautifulSoup
# from sys import argv

# script, file = argv
# essay = open(file, 'r+')

def parse(stuff):
    soup = BeautifulSoup(stuff)
    
    for t in soup.find_all('p', class_="tweet-text"):
        for a in t.find_all('a'):
            a.decompose()
    
        return t.text
        # tweet = txt.split()
        #return tweet
        
        # words = " ".join(tweet[-5:])

def split(words):
    print parse(words).split()
    
def get_tweets(tag):

    r = requests.get('https://twitter.com/search?q=' + tag + '&src=typd')
    content = r.text
    
    return split(content)


get_tweets('xmas')



# takes stored tweets and returns the last 5 words

def get_prompt(txt):
    sentences = txt.readlines()
    word_list = []

    for single in sentences:
        words = single.split()
        
        for word in words:
            word_list.append(word)
            
    prompt = " ".join(word_list[-5:])
    
    return prompt


# to be used for storing tweets

def add(to_essay):
    prompt = get_prompt(to_essay)
    new_sentence = raw_input(prompt + " ")

    to_essay.write(" " + new_sentence)
    to_essay.close()

# add(essay)