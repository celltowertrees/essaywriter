from sys import argv
import scrapy

script, file = argv

essay = open(file, 'w')

sentence = raw_input('Sentence to insert into ' + file + ': ')

essay.write(sentence)
essay.close()
