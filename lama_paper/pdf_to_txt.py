#!/usr/bin/env python3
import PyPDF2
import numpy as np
import re
import os
import glob




def get_text(path: str) -> list:
    '''
    This will get the text from pdf by page and return text and document percentage covered

    Args:
        path (string): the pdf file location

    Returns:
        list[
            final (string): txt that PyPDF2 was able to extract
            cover (float): document percentage covered]
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
    print(final)
    return [final,cover] 

def baptise(path: str) -> str:
    '''
    This get us the company and the year based on the file name as NAME_YEAR.pdf

    Args:
        path (string): the pdf file location

    Returns:
        name (string): firm name
        year (string): report year
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

    Args: 
        path (string): the pdf file location

    Returns:
        None - but creates a .txt file with the text extracted from the pdf
    '''
    y = get_text(path)
    cover = y[1]
    #score = list((sent(y[0])).values())
    name, year = baptise(path)
    print('[+] '+str(name)+' '+str(year)+'___covered:'+str(cover))
    file_name = '{}_{}'.format(name,year)
    file_object = open(file_name, 'a', encoding="utf-8")
    file_object.write(str(y[0]))
    file_object.close()


def engine():
    """
    A loop that goes through all pdf files on the folder

    Args:
        None

    Returns:
        .txt file with text extracted from the pdf
    """
    mkdir = os.path.dirname(os.path.realpath(__file__))+"/*.pdf"
    names = [os.path.basename(x) for x in glob.glob(str(mkdir))]
    for j in names:
        sample(j)


def main():
    engine()

if __name__=="__main__":
    main()
