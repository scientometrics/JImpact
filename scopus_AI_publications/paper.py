#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt






class Paper():
    """This class is for preprocessing Scopus Dataset"""
    

    
    def __init__(self, dataframe):
        file = pd.read_csv(dataframe)
        self.dataframe = file

 
        
        
    def show_columns(self):
        print("the number of columns is: {}".format(self.dataframe.shape[1]))
        print(self.dataframe.columns)
    
    def describe_dataframe(self):
        self.dataframe.info()
        
        
    def counter(self, column_name, sep):
        sep_list = []
        for k in self.dataframe[column_name][self.dataframe.loc[:, column_name].notnull()].index.values.tolist():
            if sep in self.dataframe[column_name][self.dataframe.loc[:, column_name].notnull()][k]:
                sep_list.append(k)
            else:
                continue
        return sep_list

        
    def not_int(self, column_name):
        list_of_not_int_rows = []
        list_of_not_int_values = []
        for w in range(self.dataframe.shape[0]):
            if type(self.dataframe.loc[w, column_name]) != np.int64:
                self.list_of_not_int_rows.append(w)
                self.list_of_not_int_values.append(self.dataframe.loc[w, column_name])
        return list_of_not_int_rows, list_of_not_int_values
            
    def convert(self, column_name, deli, sep="\t"):
        """Coverts commas to Tab"""
        for w in range(self.dataframe.shape[0]):
            self.dataframe.loc[w, column_name] = str(self.dataframe.loc[w, column_name]).replace(deli, sep)
    
        
    def str_covert(self, column_name):
        """coverts type to string"""
        for j in range(self.dataframe.loc[:, column_name].shape[0]):
            self.dataframe.loc[j, column_name] = str(self.dataframe.loc[j, column_name])
        
    def merge_columns(self, *args, name_of_the_new_column="merged"):
        """merge columns"""
        t = ""
        k = len(args)
        if k == 1:
            self.dataframe[name_of_the_new_column] = self.dataframe[args[0]]
        elif k == 2:
            self.dataframe[name_of_the_new_column] = self.dataframe[args[0]] + self.dataframe[args[1]]
        elif k == 3:
            self.dataframe[name_of_the_new_column] = self.dataframe[args[0]] + self.dataframe[args[1]] + self.dataframe[args[2]]
        elif k == 4:
            self.dataframe[name_of_the_new_column] = self.dataframe[args[0]] + self.dataframe[args[1]] + self.dataframe[args[2]] + self.dataframe[args[3]]
        else:
            self.dataframe[name_of_the_new_column] = self.dataframe[args[0]] + self.dataframe[args[1]] + self.dataframe[args[2]] + self.dataframe[args[3]] + self.dataframe[args[4]]
        
            
        
    def to_csv(self, name):
        """Create a new csv file without index"""
        self.dataframe.to_csv(name + ".csv", index=False)
        
    
            
        
        
        


# In[ ]:




