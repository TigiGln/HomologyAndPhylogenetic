#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 09:38:16 2020
@author: theo
"""
#import
import os
from collections import defaultdict
import time


def makedb (seq):   #make the indexed files for blast
    if (os.path.isfile('subpart/data/'+seq.split('/')[-1].replace('.fasta','.dmnd'))==False):
        os.system("cp "+seq+" subpart/data/fasta/"+seq.split('/')[-1])
        #os.system("makeblastdb -dbtype prot -in "+seq+" -out data/"+seq.split('/')[-1])
        os.system('./subpart/Diamond/diamond makedb  --in '+seq+' -d subpart/data/'+seq.split('/')[-1].replace('.fasta',''))

                          
def Blastp (seq,data_base,nom_result,directory): #fait un blastp entre une db blast et un fichier fasta
    os.system('mkdir -p '+directory+"/result_blastp/")
    #os.system("blastp -query "+seq.split('\t')[-1]+" -db data/"+data_base+".fasta  -num_threads "+str(cpu)+" -max_target_seqs 1 -outfmt 6 -evalue 1E-10 >"+directory+"/result_blastp/"+nom_result)
    os.system("./subpart/Diamond/diamond blastp -k 1 -d subpart/data/"+data_base+" -q "+seq.split('\t')[-1]+" -o "+directory+"/result_blastp/"+nom_result)
    print('done')
    time.sleep(0.1)

def read_best_hit (file_name,directory): #read blast result and return the best hit
    file = open(directory+'/result_blastp/'+file_name,'r')
    num_id = ""
    best_hit = defaultdict(lambda: 0)
    for ligne in file:
        if num_id != ligne.split('\t')[0]:
            best_hit[ligne.split('\t')[0]] = ligne.split("\t")[1]
        num_id = ligne.split('\t')[1]
    file.close()
    return best_hit

def compare_best_hit(dico_un,dico_deux,name_genome_1,name_genome_2,directory): #compare the best hit and save the bidirectionnal hit in a file
    os.system('mkdir -p '+directory+"/hits_bidirectionnelle/")
    resultat_bi = open(directory+'/hits_bidirectionnelle/resultat_bidirectionnelle_'+name_genome_1+'_VS_'+name_genome_2+'.tsv','w')
    for key, value in dico_un.items():
        if key == dico_deux[value]:
            resultat_bi.write(name_genome_1+'\t'+key+'\t'+name_genome_2+'\t'+value+'\n')
    resultat_bi.close()
        
    
    
def bidirectionnal_hit(genome_1,genome_2,directory): #take two proteome in input and use the other fonction to male the bidirectionnal hits
    name_genome_1 = genome_1.split('/')[-1].split('.')[0]
    name_genome_2 = genome_2.split('/')[-1].split('.')[0]
    Blastp(genome_1,name_genome_2,'result_blast_'+name_genome_1+'_VS_'+name_genome_2+'.blast',directory)
    Blastp(genome_2,name_genome_1,'result_blast_'+name_genome_2+'_VS_'+name_genome_1+'.blast',directory)
    best_hit_genome_un = read_best_hit('result_blast_'+name_genome_1+'_VS_'+name_genome_2+'.blast',directory)
    best_hit_genome_deux = read_best_hit('result_blast_'+name_genome_2+'_VS_'+name_genome_1+'.blast',directory)
    compare_best_hit(best_hit_genome_un,best_hit_genome_deux,name_genome_1,name_genome_2,directory)

