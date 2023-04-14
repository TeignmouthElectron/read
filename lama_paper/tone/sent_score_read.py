#!/usr/bin/env python3
import numpy as np
import re
import os
import glob
import utils

"""
Lastest update: 14/04/2023
Readme:
[] get the full text from pdf with stopwords method to clean tables
[] get the Lm word dictionary
[returns]
	-  firm
	-  year
	- total number of words
	- number of Negative
    - number of Positive
    - number of Uncertainty
    - number of Litigious
    - number of Strong_Modal
    - number of Weak_Modal
    - number of Constraining
	- % convered

"""

def sent(text: str) -> dict:
    word_dict = utils.Lm_dict()
    tokens = utils.tokenize(text)
    score = {}
    score['Total'] = len(tokens)
    for j in word_dict.keys():
        match = [i for i in tokens if i in word_dict[j]]
        score[j] = len(match)  
    return score


def baptise(path: str) -> str:
    '''
    This get us the company and the year
    '''
    base = path.split('/')
    nameyear = base[-1]
    y = nameyear.split('_')
    name = y[0]
    year = ((y[-1]).split('.'))[0]
    return name, year

def sample(path: str) -> None:
    '''
    For each report this function inserts the values on the file sample.txt
    '''
    y = utils.get_text(path)
    cover = y[1]
    score = list((sent(y[0])).values())
    name, year = baptise(path)
    print('[+] '+str(name)+' '+str(year)+'___covered:'+str(cover))
    data = str(name)+','+str(year)+','+str(score[0])+','+str(score[1])+','+str(score[2])+','+str(score[3])+','+str(score[4])+','+str(score[5])+','+str(score[6])+','+str(score[7])+','+str(cover)+'\n'
    file_object = open('sample.txt', 'a')
    file_object.write(data)
    file_object.close()


def engine():
    mkdir = os.path.dirname(os.path.realpath(__file__))+"/*.pdf"
    names = [os.path.basename(x) for x in glob.glob(str(mkdir))]
    file_object = open('sample.txt', 'a')
    file_object.write('firm,year,total,neg,pos,uncertainty,litigious,strong,weak,constraining,covered\n')
    file_object.close()
    for j in names:
        sample(j)


def main():
    engine()

if __name__=="__main__":
    main()
