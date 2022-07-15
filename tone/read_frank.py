#!/usr/bin/env python3
import PyPDF2
import numpy as np
import re
import os
import glob
import pysentiment2 as ps



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
    return [final,cover] 

def sent(text: str) -> dict:
    lm = ps.LM()
    tokens = lm.tokenize(text)
    score = lm.get_score(tokens)
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
    #smean, smax, smin, gmean, gmax, gmin, score = get_text(path)
    y = get_text(path)
    cover = y[1]
    score = list((sent(y[0])).values())
    name, year = baptise(path)
    print('[+] '+str(name)+' '+str(year)+' score: '+str(score)+'___covered:'+str(cover))
    data = str(name)+','+str(year)+','+str(score[0])+','+str(score[1])+','+str(score[2])+','+str(score[3])+','+str(cover)+'\n'
    file_object = open('sample.txt', 'a')
    file_object.write(data)
    file_object.close()


#[ ] LAST THING CHANGE
def engine():
    mkdir = os.path.dirname(os.path.realpath(__file__))+"/*.pdf"
    names = [os.path.basename(x) for x in glob.glob(str(mkdir))]
    file_object = open('sample.txt', 'a')
    file_object.write('firm,year,score_pos,score_neg,score_pol,score_sub,covered\n')
    file_object.close()
    for j in names:
        sample(j)


def main():
    engine()

if __name__=="__main__":
    main()
