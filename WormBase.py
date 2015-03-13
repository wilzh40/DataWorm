import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import lxml

import json 
import requests
import grequests
import sys 
import re


# Variables
# A couple of test genes
genes = []
genesIDs = ["WBGene00001187", "WBGene00000529", "WBGene00004830", "WBGene00004831", "WBGene00006772", "WBGene00022106", "WBGene00022240", "WBGene00006318"]


# Gene class

class Gene:
    def __init__(self,*args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Connect with the WormBase API

baseURL = "http://api.wormbase.org/rest/widget/gene/"
headers = {'content-type': 'application/json'}
r = requests.get(baseURL + "WBGene00001187/description", headers=headers) 
print(r.json())


def getGene(wbid):
    r = requests.get(baseURL + wbid + "/overview", headers=headers) 
    j = r.json()





    
    geneID = wbid 
    proteinName = j['fields']['name']['data']['label']
    description = j['fields']['concise_description']['data']['text']
    geneClass = ""

    gene = {}
    gene["Gene WB ID"] = geneID
    gene["proteinName"] = proteinName 
    gene["description"] = description
    
    return gene 


for wbid in geneIDs:
    gene = getGene(wbid)
    genes.append(gene)

print(genes)

# Create the columns based on the Excel Spreadsheet

columns = ["Gene WB ID","Protein ShortName", "Gene Public Name", "Description", "PMID for evidence", "Protein Name", "Gene Class", "Expression Pattern in Adults", "PMID for expression evidence", "Expressed in neurons", "Expression Info" ]

# Create rows based on Protein IDs
# Save to file

