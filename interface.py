#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 10:26:38 2020

@author: thierry
"""
import sys
sys.path.append("subpart/")

from tkinter import *
import PIL
import PIL.Image
from tkinter.filedialog import *
import webbrowser
from tkinter.messagebox import *
import os
from part_1 import *
from part_2 import *
from part_3 import *
from part_web import *
from graph import *
from picture import *


        

#function to create Listboxes
def listbox(liste, liste_element):
    liste_element.delete(0,END)
    for i in range(len(liste)):
        liste_element.insert(END, liste[i])
        
def Nb_clusters(enter_folder):
    file = open(enter_folder.get() + '/cluster/cluster.txt','r')
    nb=0
    for l in file:
        if l[0] == ">":
            nb += 1
    return nb

#radio button function that allows you to go directly to the selection of genomes to launch the blasts
def Skip():
    genome_list= os.listdir('subpart/data/fasta')
    listbox(genome_list, list_item1)
    title_add.grid_forget()
    copy_sequence.grid_forget()
    file_write.grid_forget()
    browse.grid_forget()
    web.grid_forget()
    record.grid_forget()
    arrow1.grid_forget()
    add.grid(column=0, row=0, sticky=E)
    no_add.grid(column=2, row=0, sticky=W)
    study_genomes.grid(column=0, row=1, columnspan=6)
    list_item1.grid(column=0, row=2, columnspan=5, rowspan=5, sticky=W+E)
    scrollbar.grid(column=5, row=2, rowspan=5, sticky=N+S)
    scrollbar2.grid(column=0, row=7, columnspan=5, sticky=W+E)
    folder_name.grid(column=0, row=9, columnspan=5, sticky=W+E)
    enter_folder.grid(column=0, row=10, columnspan=5)
    enter_folder.focus()
    submit.grid(column=0, row=11, columnspan=5)
    quit_program.grid(column=0, row=12, columnspan=5)
    empty.grid_forget()
    arrow2.grid_forget()
    empty2.grid_forget()
    result.grid_forget()
    nb_cluster.grid_forget()
    histogram_label.grid_forget()
    can_histogram.grid_forget()
    histogram_button.grid_forget()
    tree_label.grid_forget()
    can_tree.grid_forget()
    tree_button.grid_forget()
    

#radio button function that allows you to go back to the first step to add a genomes to the database
def Add_fasta():
    title_add.grid(column=0, row=0, columnspan=3)
    add.grid(column=0, row=1)
    no_add.grid(column=1, row=1)
    copy_sequence.grid(column=0, row=2, columnspan=3, rowspan=2)
    copy_sequence.delete("1.0", "end-1c")
    copy_sequence.focus()
    file_write.grid(row=4, column=0, sticky=W+E)
    browse.grid(row=5, column=0, sticky=W+E)
    file_name.grid_forget()
    file_name.configure(text="")
    web.grid(row=6, column=0, columnspan=2, sticky=W+E)
    record.grid(row=7, column=0, columnspan=2, sticky=W+E)
    quit_program.grid(column=3, row=7)
    arrow1.grid_forget()
    study_genomes.grid_forget()
    list_item1.grid_forget()
    scrollbar.grid_forget()
    scrollbar2.grid_forget()
    folder_name.grid_forget()
    enter_folder.grid_forget()
    submit.grid_forget()
    empty.grid_forget()
    arrow2.grid_forget()
    empty2.grid_forget()
    result.grid_forget()
    nb_cluster.grid_forget()
    histogram_label.grid_forget()
    can_histogram.grid_forget()
    histogram_button.grid_forget()
    tree_label.grid_forget()
    can_tree.grid_forget()
    tree_button.grid_forget()

#function allowing to open a window to name the fasta file to create
def Name_fasta():
    if copy_sequence.get(1.0, 1.1) != ">":
        showwarning(title='Error', message="If you want to use this button, please enter a sequence in the dedicated frame")
    else:
        project3.deiconify()
        Labelfile.pack()
        Namefile.pack()
        Namefile.focus()
        Validate_Name.pack()
        
#function to create a fasta file from the copied fasta sequence    
def Confirm():
    if Namefile == "":
       showwarning(title='Error', message="Please indicate the name of the file")
    else:
       with open("subpart/data/fasta/" + Namefile.get() + ".fasta" , 'w') as file:
           file.write(str(copy_sequence.get("1.0", "end-1c")))
       file_name.configure(text= str(Namefile.get())+".fasta")
       file_name.grid(row=4, column=1)
       project3.withdraw()

#function associated with the "save sequence" button to save the new proteomes in the database and create the indexes for the blast
def Record():
    # 1.0 matches the first line and 0th character (1st), end to end, -1c to remove the last character / n (line break)
    if copy_sequence.get("1.0", "end-1c") == "" and file_name.cget("text") == "":
        showwarning(title='Error', message="You have not entered a sequence. Please start over !")
    else:
        if path.get() != "":
            makedb(path.get())
        else:
            makedb("subpart/data/fasta/" + file_name.cget("text"))
        empty5= Label(project, text="")
        empty5.grid(row=0, rowspan=6, column=3)
        arrow1.grid(row=2, column=4, rowspan=3)
        study_genomes.grid(column=5, row=0, columnspan=3)
        genome_list= os.listdir('subpart/data/fasta')
        listbox(genome_list, list_item1)
        #genome selection add default
        for i in genome_list:
            if i == file_name.cget("text"):
                list_item1.selection_set(genome_list.index(i))
        list_item1.grid(column=5, row=2, columnspan=3, rowspan=3, sticky=N+S+W+E)
        scrollbar.grid(column=8, row=2, rowspan=3, sticky=N+S)
        scrollbar2.grid(column=5, row=5, columnspan=3, sticky=W+E)
        folder_name.grid(column=5, row=6, columnspan=3, sticky=W+E)
        enter_folder.grid(column=5, row=7, columnspan=3)
        enter_folder.focus()
        submit.grid(column=5, row=8, columnspan=3)
        quit_program.grid(column=5, row=9, columnspan=3)
   

#function to recover fasta file from user's computer       
def Browse():
    name = askopenfilename(title="Open your document", filetypes=[('txt files','.fasta'),('all files','.fa')])
    file = open(name, "r")
    content = file.read()
    file_name.grid(row=5, column=1)
    file_name.configure(text=name.split('/')[-1])
    path.set(name)

#function to search proteome on Ensembl
def Search():
    project2.deiconify()
    user_selection.grid(column=0, row=0, columnspan=3)
    species.grid(column=0, row=1, columnspan=3)
    species.focus()
    generate_list.grid(column=1, row=2)
    copy_sequence.delete("1.0", "end-1c")
    file_name.configure(text="")   

#function to generate the list of proteomes of the query species
def Generate_list():
    global dico_proteome_available
    if species.get() == "":
         showwarning(title='Error', message="Please enter the species you are looking for")
    else:
        list_item2.grid(column=0, row=3, columnspan=3, rowspan=5)
        scrollbar3.grid(column=3, row=3, rowspan=5, sticky=N+S)
        scrollbar4.grid(column=0, row=8, columnspan=3, sticky=W+E)
        validate.grid(column=1, row=9)
        query = species.get()
        dico_proteome_available=current_proteome(query)	
        species_list= list (dico_proteome_available.keys())
        listbox(species_list, list_item2)

#download function of the fasta sequence of the query species
def Validate():
    Labelle=Label(project, text="")
    query=dico_proteome_available[list_item2.get(list_item2.curselection())]
    fasta = download_fasta(query)
    file_name.configure(text= str(fasta.split("/")[-1]))
    file_name.grid(row=6, column=3)
    path.set(fasta)
    project2.withdraw()
    
#function allowing to launch the analysis   
def Submit():
    directory = enter_folder.get()
    global radio_button_value 
    if len(list_item1.curselection()) < 2 or directory == "" :
        showwarning(title='Erreur', message="Please choose at least two genomes and enter the name of the file of your results")
    else:
        liste_ident = []
        os.system("mkdir -p " + directory)
        for i in list_item1.curselection():
            ident= list_item1.get(i)
            liste_ident.append(ident)   
        nb_proteome = len(liste_ident)
        make_bidirectionnal_hit_on_many_proteome(liste_ident,directory)
        create_cluster(directory,nb_proteome)
        multiple_cluster_align(directory,nb_proteome)
        histo(directory)
        nb = Nb_clusters(enter_folder)
        if radio_button_value.get() == "Skip":
            empty.grid(column=0, row=13, columnspan=4, sticky=W+E)
            arrow2.grid(column=2, row=14, sticky=W+E)
            empty2.grid(column=0, row=15, columnspan=4, sticky=W+E)
            result.grid(column=2, row=16)
            empty4.grid(column=0, row=17, columnspan=5, sticky=W+E)
            nb_cluster.configure(text="Number of clusters formed: " + str(nb))
            nb_cluster.grid(column=0, row=18, columnspan=5)
            histogram_label.grid(column=0, row=19, columnspan=2)
            can_histogram.grid(column=0, row=20, columnspan=2, rowspan=4)
            histogram_button.grid(column=0, row=24, columnspan=2)
            tree_label.grid(column=3, row=19, columnspan=2)
            can_tree.grid(column=3, row=20, columnspan=2, rowspan=4)
            tree_button.grid(column=3, row=24, columnspan=2)
            empty3.grid(column=0, row=24, columnspan=5)
        else:
            empty.grid(column=0, row=10, columnspan=8)
            arrow2.grid(row=11, column=3)
            empty2.grid(column=0, row=12, columnspan=8)
            result.grid(column=3, row=13)
            empty4.grid(column=0, row=14, columnspan=8)
            nb_cluster.configure(text="Number of clusters formed: " + str(nb))
            nb_cluster.grid(column=0, row=15, columnspan=8, sticky=W)
            histogram_label.grid(column=0, columnspan=4, row=16)
            can_histogram.grid(column=1, row=17, columnspan=2, rowspan=4, sticky=W+E)
            histogram_button.grid(column=0, row=21, columnspan=4, sticky=W+E+N+S)
            tree_label.grid(column=4, columnspan=4, row=16)
            can_tree.grid(column=5, row=17, columnspan=2, rowspan=4, sticky=W+E)
            tree_button.grid(column=4, row=21, columnspan=4, sticky=W+E+N+S)
            empty3.grid(column=0, row=22, columnspan=8)


def Histogram():
    Picture(enter_folder, histogram)

def Tree():
    Picture(enter_folder, tree_phylo)

#main window creation
project = Tk()
project.title ("genome analysis")
project.resizable(height = False, width = False)

#fasta file window creation
project3 = Toplevel(project)
project3.withdraw()


#web search window creation
project2 = Toplevel(project)
project2.withdraw()

project.iconphoto(False, PhotoImage(file="subpart/Pictures/icone.png"))

#allows you to change the action of the cross at the top right
project2.protocol('WM_DELETE_WINDOW', lambda:project2.withdraw())
project3.protocol('WM_DELETE_WINDOW', lambda:project3.withdraw())



#First stage window
histogram ="/histogram/my_file.png"
tree_phylo = "/phylo/tree.png"
dico_proteome_available={}
title_add=Label(project, text="Add your genome of interest")
title_add.grid(column=0, row=0, columnspan=3)
radio_button_value= StringVar()
radio_button_value.set("Add")
add=Radiobutton(project, text="Add Fasta", variable=radio_button_value, value="Add", command= Add_fasta)
add.grid(column=0, row=1)
no_add=Radiobutton(project, text="Skip", variable=radio_button_value, value="Skip", command=Skip)
no_add.grid(column=1, row=1)
copy_sequence = Text(project, width=20, height=5)
copy_sequence.grid(column=0, row=2, columnspan=3, rowspan=2)
copy_sequence.focus()
file_write = Button(project, text="File Write", command=Name_fasta)
file_write.grid(row=4, column=0, sticky=W+E)
path=StringVar()
browse = Button(project, text="Browse", command=Browse)
browse.grid(row=5, column=0, sticky=W+E)
file_name = Label(project, text="")
web = Button(project, text="WEB search",width=20, command=Search)
web.grid(row=6, column=0, columnspan=3, sticky=W+E)
record= Button(project, text='Save sequence', width=20, command=Record)
record.grid(row=7, column=0, columnspan=3, sticky=W+E)
quit_program= Button(project, text="quit", command= project.destroy)
quit_program.grid(column=3, row=7)
arrow1 = Canvas(project, width=55, height=70)
arrow1.create_line(0, 35, 53, 35, width=5, fill="black")
arrow1.create_line(30, 17.5, 50, 35, width=6, fill="black")
arrow1.create_line(30, 52.5, 50, 35, width=6, fill="black")


#Genome selection, second stage window
study_genomes=Label(project, text="Select genomes")
scrollbar = Scrollbar(project)
scrollbar2 = Scrollbar(project, orient= HORIZONTAL)
list_item1 = Listbox(project, selectmode=MULTIPLE, exportselection=0, height=5, yscrollcommand = scrollbar.set, xscrollcommand=scrollbar2.set)
scrollbar.config(command = list_item1.yview )
scrollbar2.config(command=list_item1.xview)
folder_name=Label(project, text="Name of your results file")
enter_folder= Entry(project, text="")
submit= Button(project, text="Submit", command=Submit)


#Résults, third stage window
empty=Label(project, text="")
arrow2 = Canvas(project, width=100, height=55)
arrow2.create_line(50, 0, 50, 53, width=5, fill="black")
arrow2.create_line(25, 25, 50, 50, width=6, fill="black")
arrow2.create_line(75, 25, 50, 50, width=6, fill="black")
empty2= Label(project, text="")
result= Label(project, text="Résultat")
empty4= Label(project, text="")
nb_cluster= Label(project, text="Number of clusters formed: ")
histogram_label= Label(project, text="Histogramme : ")
image1 = PIL.Image.open("subpart/Pictures/histo_reduced.png") 
can_histogram=Canvas(project, width = image1.size[0], height = image1.size[1])
filename1 = PhotoImage(file = "subpart/Pictures/histo_reduced.png")
can_histogram.create_image(0,0, anchor = NW, image=filename1)
histogram_button=Button(project, text="View Histogram", command=Histogram)
tree_label=Label(project, text="Arbre phylogénétique")
image2 = PIL.Image.open("subpart/Pictures/tree_reduced.png")
can_tree=Canvas(project, width = image2.size[0], height = image2.size[1])
filename2 = PhotoImage(file = "subpart/Pictures/tree_reduced.png")
can_tree.create_image(0,0, anchor = NW, image=filename2)
tree_button = Button(project, text="Tree View", command=Tree)
empty3 = Label(project, text="")

#Fasta file name
Labelfile= Label(project3, text="Please give the name of the file")
Namefile=Entry(project3, text="")
Validate_Name=Button(project3, text="Confirm", command=Confirm)

#Search web
user_selection=Label(project2, text="desired species")
species = Entry(project2, text="")
generate_list= Button(project2, text="Generate list", command=Generate_list)
scrollbar3 = Scrollbar(project2)
scrollbar4 = Scrollbar(project2, orient= HORIZONTAL)
species_list= os.listdir('subpart/data/fasta/')
list_item2= Listbox(project2, exportselection=0, yscrollcommand = scrollbar3.set, xscrollcommand=scrollbar4.set)
listbox(species_list, list_item2)
scrollbar3.config(command = list_item2.yview )
scrollbar4.config(command=list_item2.xview)
validate=Button(project2, text="Validate", command=Validate)



#Creation of windows
project.mainloop()
project2.mainloop()
project3.mainloop()

