# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 15:23:00 2022

@author: BLK
"""

#import requests package to make requests to the google geocoder API
import requests 
#import pandas for obvious reasons
import pandas as pd 
from time import sleep
from random import randint

#importing the excel file as a DataFrame
df = pd.read_excel(r'C:/Users/blk/OneDrive/Studie/CBS/Visual Analytics/Final Project/smileystatus.xlsx')

#this is the API key from the google geocoder API
API_KEY = 'AIzaSyBHUP5CqtTKaDVfYor39zpSb2vmMns3zR4' 
#this is the link used to push addresses to the geocoder API
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?' 

#this iterates over all the rows in the DataFrame
count = 0
total_count = 0
if count <= 49:
    for i, row in df.iterrows():
        # this combines the address columns together in one variable
        # to push to the geocoder API.
        apiAddress = str(df.at[i, 'adresse1']) + ',' + str(df.at[i, 'postnr']) + ',' + str(df.at[i, 'By']) 
        
        # this creates a dictionary with the API key and the address info
        # to push to the Geocoder API on each iteration
        parameters = {
            'key' : API_KEY,
            'address' : apiAddress
            }
        
        try:
            response = requests.get(base_url, params = parameters).json() 
            geometry = response['results'][0]['geometry']
            # response from the API, based on the input url + the dictionary above.
            # when looked at the response, it is given as a dictionary. 
            # with this command the geometry part of the dictionary is accessed.
            
            lat = geometry['location']['lat'] 
            lng = geometry['location']['lng']
            #within the geometry party of the dictionary given by the API
            # The lat and lng are accessed respectively.
            
            df.at[i, 'Geo_Lat_New'] = lat
            df.at[i, 'Geo_Lng_New'] = lng
            # here the lat / lng are appended to two a new columns
            # in the dataframe for each iteration
            count += 1
            total_count += 1
            if count == 49:
                print('Taking a break, total count is:', total_count)
                sleep(randint(1,3))
                count = 0
        except IndexError:
            print('There was an error at iteration:', total_count)
            continue
        except requests.exceptions.ConnectionError:
            sleep(randint(10,20))
            print('There has been a connection error, trying again soon.')
            continue
        
#printing the first 10 rows.
print(df.tail(10))
# exporting the final result to a new excel file.
df.to_excel('Smiley_data_with_lon_lng.xlsx')
 




    
    