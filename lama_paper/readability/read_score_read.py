#!/usr/bin/env python3
import PyPDF2
import fitz
import numpy as np
import re
import os
import glob
from readability import Readability
import textstat

#Testing
import time
import nltk
nltk.download('stopwords')
from nltk.tokenize import TweetTokenizer


"""
Lastest update: 10/04/2023
Readme:

[] get the full text from pdf with stopwords method to clean tables
[] apply the readability score to the whole document(string)
[returns]
	-  firm
	-  year
	- readability score
	- number of pages
	- number of words
	- % convered

"""
PDF_READER_PDF2 = False #True #False

READABILITY_LIBRARY = True #False

STOPWORDS = nltk.corpus.stopwords.words('english')

THRESHOLD_STOPWORDS = 2

THRESHOLD_NUMBER = 3


def num_there(s: str) -> bool:
    #this is to check if there is any number in the string
    return any(i.isdigit() for i in s)

def table_cleaner(q: str) -> str:
    # => https://stackoverflow.com/questions/59347873/ignore-tables-while-parsing-pdf + the number count
    tk = TweetTokenizer()
    word_tokens = tk.tokenize(q)
    stopwords_x = [w for w in word_tokens if w in STOPWORDS]
    numbers_x = [n for n in word_tokens if num_there(n)]
    if len(stopwords_x)>THRESHOLD_STOPWORDS and len(numbers_x)<THRESHOLD_NUMBER:
        return q
    else:
        return ''       

def get_text(path: str) -> list:
    #This will transform the pdf into text(string). Returning string, % covered, and the # of pages. With PyPDF2 or Fitz libraries
    if PDF_READER_PDF2:
        object = PyPDF2.PdfReader(str(path))
        ### check the encrypted and tries an empty password
        if object.isEncrypted:
            if object.decrypt("") ==0:
                return ['encrypted',0,0]
        numpages = len(object.pages)
        analysed = 0
        final = ''
        for i in range(0, numpages):
            pageobj = object.pages[i]
            if pageobj.get_contents()==None:
                continue
            #tesingnggngggggggggggggggggggggggggggggggggggggggggggg
            paragraph = ''
            for j in pageobj.extract_text().split('\n'):
                #the stopwords method 
                paragraph += table_cleaner(j)          
            final += paragraph
            analysed += 1
        if numpages==0:
            cover=0
        else:
            cover = (analysed/numpages)*100
        return [final,cover,numpages]

    else:  #   FITZ LIBRARY  #
        # Does it has any encription files solution??????????????????????????????????????????????????????????????????????
        object = fitz.open(path)
        if object.isEncrypted:
            if object.authenticate("") ==0:
                return ['encrypted',0,0]
        text = ""
        for page_num in range(object.page_count): 
        # Extract the page as a Page object 
            page = object.load_page(page_num) 
        # Extract the text from the page, excluding text within tables        
            for block in page.get_text("blocks"):
                paragraph = ''
                for j in block[4].split('\n'):
                    paragraph += table_cleaner(j)
                text += paragraph

        return [text, 0,0]


def read_score(text: str) -> float:
    # this has the try becauce sometimes even if it has more than 100 words the code is unable to yield a score
    # PLEASE CHECK THIS INDIVIDUAL CASES IN DETAIL.
    
    #check the encrypted files
    if text=='encrypted':
        return 'encrypted', 0
    
    numwords = len(text.split())
    if numwords>100:
        try:
            if READABILITY_LIBRARY:
                #THIS IS USING THE OLD LIBRARY
                r = Readability(text)
                #fk = r.flesch() #FOR THE FLESH READING EASE
                #fk = r.flesch_kincaid() #FOR THE FLESH KINCAID TEST
                fk = r.gunning_fog() #FOR THE GUNNING FOG TEST
                
                y = fk.score

            else:    
                #y = textstat.flesch_reading_ease(text)
                y = textstat.gunning_fog(text)
                #y = textstat.flesch_kincaid_grade(text)
                #y = textstat.char_count(text, ignore_spaces=True)


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
    #time 
    start_time = time.time()
    engine()
    end_time = time.time()
    print('\n[+] Time used {:.0f}s\n'.format(end_time - start_time))

if __name__=="__main__":
    main()
