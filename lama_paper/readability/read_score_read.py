#!/usr/bin/env python3
import PyPDF2
import numpy as np
import re
import os
import glob
from readability import Readability

"""
Lastest update: 24/10/2022
Readme:

[] get the full text from pdf
[] apply the readability score to the whole document(string)
[returns]
	-  firm
	-  year
	- readability score
	- number of pages
	- number of words
	- % convered

"""


def get_text(path: str) -> list:
    '''
    This will transform the pdf into text capable of the Readability library to read it
    '''
    object = PyPDF2.PdfFileReader(str(path))
    numpages = object.getNumPages()
    analysed = 0
    final = ''
    for i in range(0, numpages):
        pageobj = object.getPage(i)
        if pageobj.getContents()==None:
            continue
        final += str(pageobj.extractText())
        analysed += 1
    if numpages==0:
        cover=0
    else:
        cover = (analysed/numpages)*100
    return [final,cover,numpages] 

def read_score(text: str) -> float:
    # this has the try becauce sometimes even if it has more than 100 words the code is unable to yield a score
    # PLEASE CHECK THIS INDIVIDUAL CASES IN DETAIL.
    numwords = len(text.split())
    if numwords>100:
        try:
            r = Readability(text)
            #fk = r.flesch_kincaid() #FOR THE FLESH KINCAID TEST
            fk = r.gunning_fog() #FOR THE GUNNING FOG TEST
            y = fk.score
            print('This is the score: ')
            return float(y), numwords
        except:
            return ' ', numwords
    else:
        print('Report has less than 100 words (min to run readability test)')
        return ' ', numwords



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
    y = get_text(path)
    cover = y[1]
    number_pages = y[2]
    score = read_score(y[0])[0]
    number_words = read_score(y[0])[1]
    name, year = baptise(path)
    print('[+] '+str(name)+' '+str(year)+' score: '+str(score)+'___covered:'+str(cover))
    data = str(name)+','+str(year)+','+str(score)+','+str(number_pages)+','+str(number_words)+','+str(cover)+'\n'
    file_object = open('sample.txt', 'a')
    file_object.write(data)
    file_object.close()


def engine():
    mkdir = os.path.dirname(os.path.realpath(__file__))+"/*.pdf"
    names = [os.path.basename(x) for x in glob.glob(str(mkdir))]
    file_object = open('sample.txt', 'a')
    file_object.write('firm,year,score,number_pages,number_words,covered\n')
    file_object.close()
    for j in names:
        sample(j)


def main():
    engine()

if __name__=="__main__":
    main()
