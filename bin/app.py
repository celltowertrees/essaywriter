import requests
from bs4 import BeautifulSoup
# from sys import argv

# script, file = argv
# essay = open(file, 'r+')

def get_tweets(tag):

    r = requests.get('https://twitter.com/search?q=' + tag + '&src=typd')
    content = r.text
    soup = BeautifulSoup(content)
    for tweet in soup.find_all('p', class_="tweet-text"):
        for a in tweet.find_all('a'):
            a.decompose()
        print tweet.text

    
get_tweets('garbage')

def get_prompt(txt):
    sentences = txt.readlines()
    word_list = []

    for single in sentences:
        words = single.split()
        for word in words:
            word_list.append(word)
            
    prompt = " ".join(word_list[-5:])
    
    return prompt


def add(to_essay):
    prompt = get_prompt(to_essay)
    new_sentence = raw_input(prompt + " ")

    to_essay.write(" " + new_sentence)
    to_essay.close()

# add(essay)