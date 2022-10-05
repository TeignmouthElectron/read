#!/usr/bin/env python3
import PyPDF2
from readability import Readability
import numpy as np
import re
import os
import glob


def score(text: str) -> float:
    '''
    This will get me the score 
    '''
    r = Readability(text)
    #flesch-kindcaid test
    #fk =  r.flesch_kincaid()
    #Gunning fog index
    fk = r.gunning_fog()
    y = fk.score
    #I went ot their code and this is how they calculate the grade level by rounding the score.
    x = round(y)
    print('This is the score: {}'.format(y))
    print('This is the grade level: {}'.format(x))
    return float(y),float(x)


def get_text(path: str) -> None:
    '''
    This will transform the pdf into text capable of the Readability library to read it 
    '''
    scoring = []
    grading = []

    object = PyPDF2.PdfFileReader(str(path))
    # gEt the # of pages
    numpages = object.getNumPages()
    analysed = 0
    for i in range(0, numpages):
        pageobj = object.getPage(i)
        text = pageobj.extractText()
        if len(text.split())>100:
            analysed += 1
            print('Page: {}'.format(i))
            y,x = score(text)
            scoring.append(y)
            grading.append(x)
    cover = (analysed/numpages)*100
    s1, s2, s3 = concat(scoring)
    g1, g2, g3 = concat(grading)
    return s1,s2,s3,g1,g2,g3,cover

def concat(values: list) -> float:
    '''
    This get the average, maximum and the minimum for the list recieved.
    '''
    return (sum(values)/len(values)) , max(values),min(values)

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
    smean, smax, smin, gmean, gmax, gmin, score = get_text(path)
    name, year = baptise(path)
    data = str(name)+','+str(year)+','+str(smean)+','+str(smax)+','+str(smin)+','+str(gmean)+','+str(gmax)+','+str(gmin)+','+str(score)+'\n'
    file_object = open('sample.txt', 'a')
    file_object.write(data)
    file_object.close()

def engine():
    mkdir = os.path.dirname(os.path.realpath(__file__))+"/*.pdf"
    names = [os.path.basename(x) for x in glob.glob(str(mkdir))]
    file_object = open('sample.txt', 'a')
    file_object.write('firm,year,score_mean,score_max,score_min,grade_mean,grade_max,grade_mix,covered\n')
    file_object.close()
    for j in names:
        sample(j)


def main():
    engine()

if __name__=="__main__":
    main()
