#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 11:02:40 2020
@author: theo
"""
import part_1 as p1
import os

def make_bidirectionnal_hit_on_many_proteome(genome_list, directory): #do the blast between many proteome
    while len(genome_list) != 0:
        for i in range(1,len(genome_list)):
            p1.bidirectionnal_hit('subpart/data/fasta/'+genome_list[0],'subpart/data/fasta/'+genome_list[i],directory)
        del genome_list[0]


def create_cluster(directory,nb_proteome):
    dico_species = {}
    dico_hits_bidirectionnelle = {}
    for i in os.listdir(directory+'/hits_bidirectionnelle/'):  #read all the files and make a dict
        file = open(directory+'/hits_bidirectionnelle/'+i,'r')
        for e in file:
            dico_hits_bidirectionnelle[e.split('\t')[1]] = e.split('\t')[3].replace('\n','')
            dico_species[e.split('\t')[1]] = e.split('\t')[0]
            dico_species[e.split('\t')[3].replace('\n','')] = e.split('\t')[2]
    file.close()
    
    list_cluster =  [] #list with all the cluster
    while bool(dico_hits_bidirectionnelle):
        new = True      
        first = True    
        list_del = []  #list to delete the prot already use in a cluster 
        cluster = []    #list who contain 1 cluster
        while new:      #repeat the loop while there is a new entry in cluster
            new=False
            for i in dico_hits_bidirectionnelle:
                if first and dico_hits_bidirectionnelle[i] != 'already in a cluster': #init the cluster
                     cluster.append(i)
                     cluster.append(dico_hits_bidirectionnelle[i])
                     new=True
                     first = False
                     dico_hits_bidirectionnelle[i] = 'already in a cluster'
                     list_del.append(i)
                elif i in cluster and dico_hits_bidirectionnelle[i] not in cluster and dico_hits_bidirectionnelle[i] != 'already in a cluster':
                     cluster.append(dico_hits_bidirectionnelle[i])
                     new=True
                     dico_hits_bidirectionnelle[i] = 'already in a cluster'
                     list_del.append(i)
                elif dico_hits_bidirectionnelle[i] in cluster and i not in cluster and dico_hits_bidirectionnelle[i] != 'already in a cluster':
                     cluster.append(i)
                     new=True
                     dico_hits_bidirectionnelle[i] = 'already in a cluster'
                     list_del.append(i)
        list_cluster.append(cluster) #save the cluster in list_cluster
        for i in list_del:     #delete the key already use
            del dico_hits_bidirectionnelle[i]
    os.system('mkdir -p '+directory+'/cluster/cluster_fasta/')
    file = open(directory+'/cluster/cluster.txt','w')  #save the result in a txt file
    os.system('mkdir -p '+directory+'/cluster/cluster_fasta_for_align/')

    dico_seq = read_seq_fasta(list(set(dico_species.values())))
    for cluster in list_cluster:
        verif = False
        file.write(">cluster "+str(list_cluster.index(cluster))+":\n")
        file_cluster_fasta=open(directory+'/cluster/cluster_fasta/cluster'+str(list_cluster.index(cluster))+'.fasta','w')
        if len(cluster) == nb_proteome:
                    file_cluster_fasta_2=open(directory+'/cluster/cluster_fasta_for_align/cluster'+str(list_cluster.index(cluster))+'.fasta','w')
                    verif = True
        for i in cluster:
            file.write("species : "+dico_species[i]+"\t\tProteine : "+i+"\n")  
            file_cluster_fasta.write('>'+dico_species[i]+'\n'+dico_seq['>'+i])
            if verif:
                file_cluster_fasta_2.write('>'+dico_species[i]+'\n'+dico_seq['>'+i])
        file_cluster_fasta.close
        if verif:
            file_cluster_fasta_2.close            
        
    file.close
    return len(list_cluster)

def read_seq_fasta(list_proteome):
    dico_sequences = {}
    sequences = ""
    ident = ""
    for proteome in list_proteome:
        file_fasta = open('subpart/data/fasta/'+proteome+'.fasta','r')
        for ligne in file_fasta:
            if ligne[0]=='>':
                dico_sequences[ident]=sequences
                sequences=""
                ident= ligne.split(' ')[0].replace('\n','')
            else:
                sequences+=ligne
        dico_sequences[ident]=sequences
    return dico_sequences
