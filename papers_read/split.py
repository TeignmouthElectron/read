#!/usr/bin/env python3
import PyPDF2


FULL_PATH = '/home/sanctus/projects/read/Sasol_2018.pdf'

def info(path):
    object = PyPDF2.PdfFileReader(str(path))
    info = object.getDocumentInfo()
    return info


def main():
    print(info(FULL_PATH))


if __name__=='__main__':
    main()
