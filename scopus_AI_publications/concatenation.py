#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Improting the necessary packages (paper is a package I created for data preprocessing)
from paper import Paper
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 
import glob

# list of directories in this file
list_files = os.listdir()


# list of files with .csv 
list_files_csv = []
for i in list_files:
    if i.endswith(".csv"):
        list_files_csv.append(i)

# list_files_csv

# len(list_files_csv)

# test = Paper("scopus-2010.csv")

# test.str_covert(column_name="Conference code")
# test.counter(column_name="Conference code", sep=";")


# test.dataframe.loc[3, "Conference code"]

#the number of columns is: 47
# Index(['Authors', 'Author(s) ID', 'Title', 'Year', 'Source title', 'Volume',
#        'Issue', 'Art. No.', 'Page start', 'Page end', 'Page count', 'Cited by',
#        'DOI', 'Link', 'Affiliations', 'Authors with affiliations', 'Abstract',
#        'Author Keywords', 'Index Keywords', 'Molecular Sequence Numbers',
#        'Chemicals/CAS', 'Tradenames', 'Manufacturers', 'Funding Details',
#        'Funding Text 1', 'Funding Text 2', 'Funding Text 3', 'References',
#        'Correspondence Address', 'Editors', 'Sponsors', 'Publisher',
#        'Conference name', 'Conference date', 'Conference location',
#        'Conference code', 'ISSN', 'ISBN', 'CODEN', 'PubMed ID',
#        'Language of Original Document', 'Abbreviated Source Title',
#        'Document Type', 'Publication Stage', 'Access Type', 'Source', 'EID'],
#       dtype='object')

i = 0
for dataframe in list_files_csv:
    paper = Paper(dataframe)
    
    #Authors
    paper.str_covert(column_name="Authors")
    paper.convert(column_name="Authors", deli=",")
    
    #Author(s) ID
    paper.str_covert(column_name="Author(s) ID")
    paper.convert(column_name="Author(s) ID", deli=";")
    
    #Title
    paper.str_covert(column_name="Title")
    paper.convert(column_name="Title", deli=",")
    
    #Year
    pass
    
    #Source title
    paper.str_covert(column_name="Source title")

    #Volume
    paper.str_covert(column_name="Volume")
    
    #Issue
    paper.str_covert(column_name="Issue")
    
    #Art. No.
    paper.str_covert(column_name="Art. No.")
    
    #Page start
    paper.str_covert(column_name="Page start")
    
    #Page end
    paper.str_covert(column_name="Page end")
    
    #Page count
    paper.str_covert(column_name="Page count")
    
    #Cited by
    paper.str_covert(column_name="Cited by")
    
    #DOI
    paper.str_covert(column_name="DOI")
    
    #Link
    paper.str_covert(column_name="Link")
    
    #Affiliations
    paper.str_covert(column_name="Affiliations")
    paper.convert(column_name="Affiliations", deli=";")
    
    #Authors with affiliations
    paper.str_covert(column_name="Authors with affiliations")
    paper.convert(column_name="Authors with affiliations", deli=";")
    
    #Abstract
    paper.str_covert(column_name="Abstract")
    
    #Author Keywords
    paper.str_covert(column_name="Author Keywords")
    paper.convert(column_name="Author Keywords", deli=";")
    
    #Index Keywords
    paper.str_covert(column_name="Index Keywords")
    paper.convert(column_name="Index Keywords", deli=";")
    
    #Molecular Sequence Numbers
    paper.str_covert(column_name="Molecular Sequence Numbers")
    
    #Chemicals/CAS
    paper.str_covert(column_name="Chemicals/CAS")
    paper.convert(column_name="Chemicals/CAS", deli=";")
    
    #Tradenames
    paper.str_covert(column_name="Tradenames")
    paper.convert(column_name="Tradenames", deli=";")
    
    #Manufacturers
    paper.str_covert(column_name="Manufacturers")
    paper.convert(column_name="Manufacturers", deli=";")
    
    if "Funding Text 4" not in paper.dataframe.columns.values.tolist():
        paper.dataframe["Funding Text 4"] = " "
    if "Funding Text 3" not in paper.dataframe.columns.values.tolist():
        paper.dataframe["Funding Text 3"] = " "
    if "Funding Text 2" not in paper.dataframe.columns.values.tolist():
        paper.dataframe["Funding Text 2"] = " "
    if "Funding Text 1" not in paper.dataframe.columns.values.tolist():
        paper.dataframe["Funding Text 1"] = " "
    
    
    
    #Funding Details, Funding Text 1, Funding Text 2, Funding Text 3, Funding Text 4
    paper.merge_columns("Funding Details", "Funding Text 1", "Funding Text 2", "Funding Text 3", "Funding Text 4")
    
    
    #References
    paper.str_covert(column_name="References")
    paper.convert(column_name="References", deli=";")
    
    #Correspondence Address
    paper.str_covert(column_name="Correspondence Address")
    
    #Editors
    paper.str_covert(column_name="Editors")
    
    #Sponsors
    paper.str_covert(column_name="Sponsors")
    
    #Publisher
    paper.str_covert(column_name="Publisher")
    
    #Conference name
    paper.str_covert(column_name="Conference name")
    
    #Conference date
    paper.str_covert(column_name="Conference date")
    
    #Conference location
    paper.str_covert(column_name="Conference location")

    #Conference code
    paper.str_covert(column_name="Conference code")

    
    
    #ISSN
    paper.str_covert(column_name="ISSN")
    
    
    #ISBN
    paper.str_covert(column_name="ISBN")
    paper.convert(column_name="ISBN", deli=";")
    
    #CODEN
    paper.str_covert(column_name="CODEN")
    
    #PubMed ID
    paper.str_covert(column_name="PubMed ID")
    
    #Language of Original Document
    paper.str_covert(column_name="Language of Original Document")
    
    
    #Abbreviated Source Title
    paper.str_covert(column_name="Abbreviated Source Title")
    
    #Document Type
    paper.str_covert(column_name="Document Type")
    
    #Publication Stage
    paper.str_covert(column_name="Publication Stage")
    
    #Access Type
    paper.str_covert(column_name="Access Type")
    
    #Source
    paper.str_covert(column_name="Source")
    
    #EID
    paper.str_covert(column_name="EID")

    

    
    paper.dataframe[sorted(paper.dataframe.columns)]
    
    print("done!!!")
    globals()["df_" + str(i)] = paper.dataframe
    i += 1
    


    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#concatenation
df_all = pd.concat([df_0, df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10, df_11, df_12, df_13, df_14], ignore_index=False)

df_all.loc[:, "merged"].nunique() # we have 92 unique values for merged field (Funding details)

# CSV file
df_all.to_csv("df_all.csv")

