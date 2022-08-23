#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 09:00:03 2020

@author: theo
"""
import os
from Bio import SeqIO
from collections import defaultdict
from Bio import Phylo
import matplotlib.pyplot as plt


def align(file,directory,nb_proteome):  #make the alignement and the curation of the cluster
    nb_seq = os.popen("grep -c '>' "+directory+'/cluster/cluster_fasta_for_align/'+file).readlines()[0].replace('\n','')
    nb_proteome_in_file = os.popen("grep '>' "+directory+"/cluster/cluster_fasta_for_align/"+file+" | sort | uniq | wc -l").readlines()[0].replace('\n','')
    nb_proteome = str(nb_proteome)
    if os.popen('grep ">" '+directory+'/cluster/cluster_fasta_for_align/'+file+'|sort|uniq|wc -l').readlines()[0].replace('\n','') == nb_proteome:
        os.system("./subpart/muscle/muscle3.8.31_i86linux64 -in "+directory+'/cluster/cluster_fasta_for_align/'+file+" -out "+directory+"/phylo/"+file+".muscle")
        os.system("./subpart/Gblocks_0.91b/Gblocks "+directory+'/phylo/'+file+".muscle g")
        os.system('rm '+directory+'/phylo/'+file+'.muscle')
        os.system('rm '+directory+'/phylo/'+file+'.muscle-gb.htm')



def phylo(file,directory):  #do the phylogénie with phyML
    records = SeqIO.parse(directory+'/phylo/'+file, "fasta")
    count = SeqIO.write(records, directory+'/phylo/'+file+".phylip", "phylip")
    os.system('./subpart/PhyML-3.1/PhyML-3.1_linux64 -i '+directory+'/phylo/'+file+'.phylip -d aa')
    create_tree(directory)
    
def make_super_alignement (directory):  #concat all alignement result in a super-alignement
    dico_super_alignement = defaultdict(lambda: '')
    super_alignement = ''
    num_id = ''
    for alignement in os.listdir(directory+'/phylo/'):
        file_alignement = open(directory+'/phylo/'+alignement)
        for ligne in file_alignement:     
            if ligne[0] == '>':
                dico_super_alignement[num_id] += super_alignement.replace('\n','').replace(' ','')
                super_alignement = ''
                num_id = ligne
            else :
                super_alignement += ligne
        dico_super_alignement[num_id] += super_alignement.replace('\n','').replace(' ','')
        super_alignement = ''
        num_id = ''
        file_alignement.close

    file_super_alignement = open(directory+'/phylo/super_alignement.fasta','w')
    for key in dico_super_alignement:
        seq = dico_super_alignement[key]
        corrector = 0
        for i in range(10,len(dico_super_alignement[key]),10):
            if i%60 == 0:
                seq = seq[:i+corrector]+'\n'+seq[i+corrector:]
                corrector += 1
            else:
                seq = seq[:i+corrector]+' '+seq[i+corrector:]
                corrector += 1
        file_super_alignement.write(key+seq+'\n')
    file_super_alignement.close
        
def multiple_cluster_align (directory,nb_proteome): #do the alignmement for all the cluster and the phylogeny of the super alignement
    if nb_proteome >= 3:
        os.system('mkdir -p '+directory+'/phylo/')
        if len(os.listdir(directory+'/cluster/cluster_fasta_for_align/')) != 0:
            n=0
            for file in os.listdir(directory+'/cluster/cluster_fasta_for_align/'):
                n+=1
                align(file,directory,nb_proteome)
            make_super_alignement(directory)
            phylo('super_alignement.fasta',directory)
        else:
            print('0 cluster')
        
def create_tree(directory):
    tree = Phylo.read(directory+'/phylo/super_alignement.fasta.phylip_phyml_tree.txt', "newick")
    Phylo.draw(tree, do_show=False)
    plt.savefig(directory+'/phylo/tree.png')

