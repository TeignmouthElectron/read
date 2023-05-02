#!/usr/bin/env python3
import nltk
nltk.download('stopwords')
import pandas as pd
from nltk.tokenize import TweetTokenizer
import PyPDF2
import fitz
import numpy as np
"""
This code was based on the Bill McDonald Routine to load master dictionary Version for LM 2020 Master Dictionary

"""
#THIS ONE IS IN LOWERCASE =??? maybe try to change this to a class and features of the class 
STOPWORDS = nltk.corpus.stopwords.words('english')
METRICS = ['Negative', 'Positive','Uncertainty','Litigious', 'Strong_Modal', 'Weak_Modal','Constraining']

PDF_READER_PDF2 = True #False

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
#########################

def tokenize(text: str):
    tk = TweetTokenizer()
    word_tokens = tk.tokenize(text)
    return [w for w in word_tokens if w not in STOPWORDS]


def clean(path, word, metric):
    data = pd.read_csv(path)
    out = {}
    for i in metric:
        d = data[[word,i]].copy()
        d[i] = d[i].map(lambda x: x if x==0 else 1)
        d = d[d[i]==1].copy()
        out[i] = [j.lower() for j in list(d[word].unique())]
    return out

def Lm_dict():
    '''
    returns a dictionary with the list of word for each metric
    '''
    try:
        return clean('Lm_MasterDictionary.csv', 'Word',METRICS)
    except Exception: 
        print('Please download the Lm dictionary in the following link: https://sraf.nd.edu/loughranmcdonald-master-dictionary/')

def complex():
    return ['accruable','accrual',
'accruals'	,
'accrue'	,
'accrued'	,
'accrues'	,
'accruing'	,
'acquire'	,
'acquired'	,
'acquiree'	,
'acquirees'	,
'acquirer'	,
'acquirers'	,
'acquires'	,
'acquiring'	,
'acquiror'	,
'acquirors'	,
'acquisition'	,
'acquisitions'	,
'acquisitive'	,
'affiliate'	,
'affiliated'	,
'affiliates'	,
'affiliating'	,
'affiliation'	,
'affiliations'	,
'alliance'	,
'alliances'	,
'bankrupt'	,
'bankruptcies'	,
'bankruptcy'	,
'bankrupted'	,
'carryback'	,
'carrybacks'	,
'carryforward'	,
'carryforwards'	,
'collaborate'	,
'collaborated'	,
'collaborates'	,
'collaborating'	,
'collaboration'	,
'collaborations'	,
'collaborative'	,
'collaboratively'	,
'collaborator'	,
'collaborators'	,
'collateral'	,
'collateralization'	,
'collateralize'	,
'collateralized'	,
'collateralizes'	,
'collateralizing'	,
'collaterals'	,
'complex'	,
'complexities'	,
'complexity'	,
'complexly'	,
'conglomerate'	,
'conglomerates'	,
'contingencies'	,
'contingency'	,
'contingent'	,
'contingently'	,
'contract'	,
'contracted'	,
'contractholder'	,
'contractholders'	,
'contracting'	,
'contracts'	,
'contractual'	,
'contractually'	,
'contractuals'	,
'contractural'	,
'conversion'	,
'conversions'	,
'convertibility'	,
'convertible'	,
'convertibles'	,
'copyright'	,
'copyrightable'	,
'copyrighted'	,
'copyrighting'	,
'copyrights'	,
'counterparties'	,
'counterparty'	,
'covenant'	,
'covenanted'	,
'covenanting'	,
'covenants'	,
'derivative'	,
'derivatives'	,
'embedded'	,
'entities'	,
'exercisability'	,
'exercisable'	,
'exerciseability'	,
'exerciseable'	,
'exercised'	,
'floating'	,
'foreign'	,
'franchise'	,
'franchised'	,
'franchisee'	,
'franchisees'	,
'franchiser'	,
'franchisers'	,
'franchises'	,
'franchising'	,
'franchisor'	,
'franchisors'	,
'futures'	,
'global'	,
'globalization'	,
'globalize'	,
'globalized'	,
'globalizing'	,
'globally'	,
'hedge'	,
'hedged'	,
'hedges'	,
'hedging'	,
'imbedded'	,
'infringe'	,
'infringed'	,
'infringement'	,
'infringements'	,
'infringer'	,
'infringers'	,
'infringes'	,
'infringing'	,
'insolvencies'	,
'insolvency'	,
'insolvent'	,
'intangible'	,
'intangibles'	,
'interconnect'	,
'interconnected'	,
'interconnectedness'	,
'interconnecting'	,
'interconnection'	,
'interconnections'	,
'interconnects'	,
'international'	,
'internationalization'	,
'internationally'	,
'lawsuit'	,
'lawsuits'	,
'leasable'	,
'lease'	,
'leaseable'	,
'leaseback'	,
'leasebacks'	,
'leased'	,
'leasehold'	,
'leaseholder'	,
'leaseholders'	,
'leaseholds'	,
'leaser'	,
'leases'	,
'leasing'	,
'lessee'	,
'lessees'	,
'lessor'	,
'lessors'	,
'licence'	,
'licenced'	,
'licences'	,
'licencing'	,
'licensable'	,
'license'	,
'licensed'	,
'licensee'	,
'licensees'	,
'licenses'	,
'licensing'	,
'licensor'	,
'licensors'	,
'lien'	,
'lienholder'	,
'lienholders'	,
'liens'	,
'liquidate'	,
'liquidated'	,
'liquidates'	,
'liquidating'	,
'liquidation'	,
'liquidations'	,
'liquidator'	,
'liquidators'	,
'litigate'	,
'litigated'	,
'litigates'	,
'litigating'	,
'litigation'	,
'litigations'	,
'litigious'	,
'merge'	,
'merged'	,
'merger'	,
'mergers'	,
'merges'	,
'merging'	,
'nationalization'	,
'nationalizations'	,
'nationalize'	,
'nationalized'	,
'nationalizing'	,
'nonmarketable'	,
'outsource'	,
'outsourced'	,
'outsourcer'	,
'outsourcers'	,
'outsources'	,
'outsourcing'	,
'partner'	,
'partnered'	,
'partnering'	,
'partners'	,
'partnership'	,
'partnerships'	,
'patent'	,
'patentability'	,
'patentable'	,
'patented'	,
'patentee'	,
'patenting'	,
'patents'	,
'reacquire'	,
'reacquired'	,
'reacquires'	,
'reacquiring'	,
'reacquisition'	,
'reacquisitions'	,
'recapitalization'	,
'recapitalizations'	,
'recapitalize'	,
'recapitalized'	,
'recapitalizes'	,
'recapitalizing'	,
'reclassification'	,
'reclassifications'	,
'reclassified'	,
'reclassifies'	,
'reclassify'	,
'reclassifying'	,
'reissuance'	,
'reissuances'	,
'reissue'	,
'reissued'	,
'reissues'	,
'reissuing'	,
'reorganisation'	,
'reorganization'	,
'reorganizational'	,
'reorganizations'	,
'reorganize'	,
'reorganized'	,
'reorganizes'	,
'reorganizing'	,
'repatriate'	,
'repatriated'	,
'repatriates'	,
'repatriating'	,
'repatriation'	,
'repatriations'	,
'restructure'	,
'restructured'	,
'restructures'	,
'restructuring'	,
'restructurings'	,
'revaluation'	,
'revaluations'	,
'revalue'	,
'revalued'	,
'revalues'	,
'revaluing'	,
'revocability'	,
'revocable'	,
'revocation'	,
'revocations'	,
'revoke'	,
'revoked'	,
'revokes'	,
'revoking'	,
'royalties'	,
'royalty'	,
'securitizable'	,
'securitization'	,
'securitizations'	,
'securitize'	,
'securitized'	,
'securitizer'	,
'securitizers'	,
'securitizes'	,
'securitizing'	,
'segment'	,
'segmental'	,
'segmentation'	,
'segmentations'	,
'segmented'	,
'segmenting'	,
'segments'	,
'sovereign'	,
'sovereigns'	,
'sovereignties'	,
'sovereignty'	,
'subcontract'	,
'subcontracted'	,
'subcontracting'	,
'subcontractor'	,
'subcontractors'	,
'subcontracts'	,
'sublease'	,
'subleased'	,
'subleasee'	,
'subleasehold'	,
'subleases'	,
'subleasing'	,
'sublessee'	,
'sublessees'	,
'sublessor'	,
'sublessors'	,
'sublet'	,
'sublets'	,
'subletting'	,
'sublettings'	,
'sublicensable'	,
'sublicense'	,
'sublicenseable'	,
'sublicensed'	,
'sublicensee'	,
'sublicensees'	,
'sublicenses'	,
'sublicensing'	,
'sublicensor'	,
'subsidiaries'	,
'subsidiary'	,
'subsidies'	,
'subsiding'	,
'subsidization'	,
'subsidize'	,
'subsidized'	,
'subsidizers'	,
'subsidizes'	,
'subsidizing'	,
'subsidy'	,
'subtenancies'	,
'subtenancy'	,
'subtenant'	,
'subtenants'	,
'swap'	,
'swaps'	,
'swaption'	,
'swaptions'	,
'takeover'	,
'takeovers'	,
'trademark'	,
'trademarked'	,
'trademarking'	,
'trademarks'	,
'unexercisable'	,
'unexercised'	,
'unrecognized'	,
'unremitted'	,
'unrepatriated'	,
'venture'	,
'ventures'	,
'warrantees'	,
'warrantied'	,
'warranties'	,
'warranting'	,
'warrantor'	,
'warranty'	,
'worldwide']
