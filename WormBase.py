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
geneIDs = ["WBGene00001187", "WBGene00000529", "WBGene00004830", "WBGene00004831", "WBGene00006772", "WBGene00022106", "WBGene00022240", "WBGene00006318"]


# Gene class

class Gene:
    def __init__(self,*args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Testing connection with the WormBase API


baseURL = "http://api.wormbase.org/rest/widget/gene/"
headers = {'content-type': 'application/json'}
r = requests.get(baseURL + "WBGene00001187/description", headers=headers) 
print(r.json())


#columns = ["Gene WB ID","Protein ShortName", "Gene Public Name", "Description", "PMID for evidence", "Protein Name", "Gene Class", "Expression Pattern in Adults", "PMID for expression evidence", "Expressed in neurons", "Expression Info" ]

def getGene(wbid):
    r = requests.get(baseURL + wbid + "/overview", headers=headers) 
    j = r.json()



    geneID = wbid 
    proteinName = j['fields']['name']['data']['label']
    description = j['fields']['concise_description']['data']['text']
    descriptionEvidence = [] 
    
    for ev in j['fields']['concise_description']['data']['evidence']['Paper_evidence']:
        descriptionEvidence.append(ev['id'].encode('utf8'))
        
    geneClass = j['fields']['gene_class']['data']['description']
    
    # Different URI for expression
    r = requests.get(baseURL + wbid + "/expression", headers=headers) 
    j = r.json()

    expPattern = []
    for pattern in j['fields']['expression_patterns']['data']:
        expPattern.append(pattern['expression_pattern']['id'].encode('utf8'))
# Different code to be assigned later, dictionary is temp, may replace with a gene class
    gene = {}
    gene["Gene WB ID"] = geneID
    gene["Protein Name"] = proteinName 
    gene["Description"] = description
    gene["Description Evidence"] = descriptionEvidence    
    gene["Gene Class"] = geneClass
    gene["Expression Pattern in Adults"] = expPattern
    return gene 


for wbid in geneIDs:
    gene = getGene(wbid)
    genes.append(gene)

# Create the dataframe table
df = pd.DataFrame(genes)

print(df)


# Save to file

df.to_csv(path_or_buf = "./table.csv")
