#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 15:16:37 2020

@author: thierry
"""

import pandas as p
from plotnine import *
from matplotlib import pyplot as plt
import os


def histo(directory):
    os.system("mkdir -p " + directory + "/histogram/")
    newfile=open(directory + "/histogram/myfile.txt", "w")
    newfile.write("protéine name" + "\t" + "percentage identity" + "\n")
    Notnull=False
    for name in os.listdir(directory + "/result_blastp/"):
        if os.path.getsize(directory +'/result_blastp/'+ name) != 0:
            Notnull = True
            file = open(directory +'/result_blastp/'+ name,'r')
            for line in file:
                newfile.write(str(line.split("\t")[0]) + "\t" + str(line.split("\t")[2]) + "\n")
            file.close()
    newfile.close()

    # Lire le jeu de données
    if Notnull:
        df = p.read_csv(directory + "/histogram/myfile.txt", "\t" )
        g_x = ggplot( data = df, mapping = aes( x = 'percentage identity'))
        histo= geom_histogram(bins=30, fill="red", color="blue")
        graphtitle=  ggtitle("Percent Identity of homologue") 
        name_axe_x= xlab("% identities of each homologue")
        name_axe_y =  ylab("number of proteins")
        figure=  g_x + histo + graphtitle + name_axe_x + name_axe_y
        figure.save(directory + "/histogram/my_file.png")


