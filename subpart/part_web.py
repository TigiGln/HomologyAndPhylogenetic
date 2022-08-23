#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:25:53 2020

@author: theo
"""

import os

def current_proteome(query):
    reg="[^a-z0-9]"
    dico_proteome_available = {}
    os.system('wget -O subpart/web/current_readme.txt ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README')
    os.system("grep -i '^UP.*" + reg + query + reg + "' subpart/web/current_readme.txt > subpart/web/file.txt")
    file=open('subpart/web/file.txt', 'r')
    for i in file:
        i=i.split('\t')
        dico_proteome_available[i[7].replace('\n','')] = i[3] + '\t' + i[0]+'_'+i[1]+'.fasta.gz'
    file.close()
    return dico_proteome_available


def download_fasta(query): #the query is the value of the dictionary (reign\tproteomeid_taxid.fasta.gz)
    query = query.split('\t')
    os.system('wget -O subpart/data/fasta/'+ query[1]+' ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/'+query[0][0].upper()+query[0][1:]+'/'+query[1])
    os.system("gunzip subpart/data/fasta/" + query[1])
    fasta = "subpart/data/fasta/"+ query[1].replace(".gz","")
    os.system("rm -f subpart/data/fasta/"+ query[1])
    return fasta

