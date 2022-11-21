#!/usr/bin/env python3
import PyPDF2
import numpy as np
import re
import os
import glob
"""
[ ] makes the .txt files based on the text of the pdfs
[ ] returns .txt files named as FIRM_YEAR.txt and the sample_size.txt (with pdf and txt megabytes for each firm_year obs)
"""



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
    #object = PyPDF2.PdfFileReader(str(path))
    object = PyPDF2.PdfReader(str(path))
    #numpages = object.getNumPages()
    numpages = len(object.pages)
    if object.is_encrypted: 
    	print('files is encrypted'+str(path))
    print('Is it encrypted?'+str(object.is_encrypted))
    analysed = 0
    final = ''
    for i in range(0, numpages):
        #pageobj = object.getPage(i)
        pageobj = object.pages[i]
        #if pageobj.getContents()==None:
        if pageobj.get_contents()==None:
            continue
        #final += str(pageobj.extractText())
        final += str(pageobj.extract_text())
        analysed += 1
    if numpages==0:
        cover=0
    else:
        cover = (analysed/numpages)*100
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

def sample(path: str) -> float:
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
    file_name = '{}_{}.txt'.format(name,year)
    file_object = open(file_name, 'a', encoding="utf-8")
    file_object.write(str(y[0]))
    file_object.close()
    # TO GET THE SIZE OF THE PDF AND TXT
    pdf_size = os.path.getsize(path)/(1024*1024)
    txt_size = os.path.getsize(path[:-3]+'txt')/(1024*1024)
    print(path+'     size:{} megabytes'.format(pdf_size))
    print(path[:-3]+'txt    size:{} megabytes'.format(txt_size))
    return pdf_size, txt_size, name, year
	
def size_sample(pdf_size: float, txt_size: float, name: str, year: str) -> None:
    add = name+','+year+','+str(pdf_size)+','+str(txt_size)+'\n'
    sample = open('sample_size.txt', 'a')
    sample.write(add)
    sample.close()


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
        pdf_mb, txt_mb, name, year = sample(j)
        size_sample(pdf_mb, txt_mb, name, year)
	

def main():
    start = open('sample_size.txt','a')
    start.write('firm,year,pdf_size_mb,txt_size_mb\n')
    start.close()
    engine()

if __name__=="__main__":
    main()
