import csv
import math
import pickle
import collections, functools, operator
import pandas as pd
from pathlib import Path
from glob import glob
import errno
import zipfile

def Conversions(file1, file2):
    '''
    file, file --> dict, dict

    This function reads a file in order to convert a zone to the appropriate planning 
    district. It then reads the second file to convert the planning districts to spatial
    categories. The function returns two dictionaries, the first one having the keys as
    zones and the values as the appropriate planning districts. The second dictionary has
    the planning districts as keys and spatial categories as values.

    '''
    zone_to_pd = {}
    pd_to_sp = {}    
    
    with open(file1, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for conversion_row1 in csv_reader:   
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1 
                zone_to_pd[conversion_row1[0]] = conversion_row1[1]
                
            
    with open(file2, 'r') as csv_file1:
        csv_reader1 = csv.reader(csv_file1, delimiter=',')
        line_count1 = 0
        for conversion_row2 in csv_reader1:
            if line_count1 == 0:
                line_count1 += 1
            else:
                line_count1 += 1
                pd_to_sp[conversion_row2[0]] = conversion_row2[1]
                   
    return (zone_to_pd, pd_to_sp)

def Get_Archive(my_zipfile, suffix_string):
        for file in my_zipfile.namelist():
            if (file.endswith(suffix_string)):
                return file

        raise Exception('Unable to find archive name with suffix suffix_string')

def Auto_Ownership(): 
    '''
    file --> dictionary

    This function calculates the average amount of households who have a certain amount of cars
    (0, 1, 2, 3, or 4) in each spatial category. It returns a dictionary with the keys being
    the spatial category and the values being a dictionary where the keys are the number of cars 
    and the values are the amount of households who own that amount of cars.

    '''   
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    spatial_category_list = []
    cars_list = []
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    ownerships_dict = {}
   
    with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\0-49\0.zip') as myzip:
        files = myzip.namelist()
        with myzip.open(Get_Archive(myzip, 'households.csv')) as myfile:   

            for row in myfile:                  
            
                if (is_first_row == True): #Checks if the row is the first row
                    is_first_row = False #Changes flag to false since there is only 1 first row    
            
                else: #If the row is not the first row
                    cars_list.append(int(row[5]))
                    home_zone = row[1] 
                    home_pd = variables[0][home_zone]
                    home_sc = variables[1][home_pd]
                    spatial_category_list.append(home_sc)
                
            for i in range (0, len(spatial_category_list), 1): 
        
                if spatial_category_list[i] in ownerships_dict:
                    if cars_list[i] in ownerships_dict[spatial_category_list[i]]:
                        value = ownerships_dict[spatial_category_list[i]][cars_list[i]] + 1
                        ownerships_dict[spatial_category_list[i]][cars_list[i]] = value          
                
                    else:
                        ownerships_dict[spatial_category_list[i]][cars_list[i]] = 1
                
                else:
                    ownerships_dict[spatial_category_list[i]] = {cars_list[i] : 1}
        
    return ownerships_dict 

print(Auto_Ownership())