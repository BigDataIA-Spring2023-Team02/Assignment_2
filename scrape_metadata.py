import os
import re
import requests
import time
import boto3
import pandas as pd
from dotenv import load_dotenv

class Scrape_Data:
    def __init__(self):
        load_dotenv()
        
        self.s3client = boto3.client('s3',
                            region_name='us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                            )
        
        self.clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOGS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOGS_SECRET_KEY')
                        )
        
        self.geos_bucket_name = "noaa-goes18"
        self.geos18_data_dict = {'ID': [], 'Product_Name': [], 'Year': [], 'Day': [], 'Hour': []}
        self.nexrad_bucket_name = "noaa-nexrad-level2"
        self.nexrad_data_dict = {'ID': [], 'Year': [], 'Month': [], 'Day': [], 'NexRad Station Code': []}
        self.nexrad_map_data_url = "https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt"
        self.nexradmap_data_dict = {'ID': [], 'Station_Code': [], 'State': [], 'County': [],'latitude': [], 'longitude': [],'elevation': []}

    def write_logs(self, message: str):
        self.clientLogs.put_log_events(
            logGroupName = "Assignment02-logs",
            logStreamName = "Scrape-Logs",
            logEvents = [
                {
                    'timestamp' : int(time.time() * 1e3),
                    'message' : message
                }
            ]
        )
    
    def geos18_data(self):
        id = 1
        prefix = "ABI-L1b-RadC/"
        result = self.s3client.list_objects(Bucket = self.geos_bucket_name, Prefix = prefix, Delimiter = '/')
        self.write_logs(f"Returning list of objects in GEOS18 Bucket for selected prefix {prefix}: {result}")

        for i in result.get('CommonPrefixes'):
            path = i.get('Prefix').split('/')
            prefix_2 = prefix + path[-2] + "/"
            sub_folder = self.s3client.list_objects(Bucket = self.geos_bucket_name, Prefix = prefix_2, Delimiter = '/')
            
            for j in sub_folder.get('CommonPrefixes'):
                sub_path = j.get('Prefix').split('/')
                prefix_3 = prefix_2 + sub_path[-2] + "/"
                sub_sub_folder = self.s3client.list_objects(Bucket = self.geos_bucket_name, Prefix = prefix_3, Delimiter = '/')
                
                for k in sub_sub_folder.get('CommonPrefixes'):
                    sub_sub_path = k.get('Prefix').split('/')
                    sub_sub_path = sub_sub_path[:-1]
                    self.geos18_data_dict['ID'].append(id)
                    self.geos18_data_dict['Product_Name'].append(sub_sub_path[0])
                    self.geos18_data_dict['Year'].append(sub_sub_path[1])
                    self.geos18_data_dict['Day'].append(sub_sub_path[2])
                    self.geos18_data_dict['Hour'].append(sub_sub_path[3])
                    id += 1
        
        geos18_data = pd.DataFrame(self.geos18_data_dict)
        self.write_logs(f"Returning metadata from GEOS18 Bucket: {geos18_data}")
        return geos18_data

    def nexrad_data(self):
        id = 1
        years = ['2022','2023']
        for year in years:
            prefix = year + '/'
            result = self.s3client.list_objects(Bucket = self.nexrad_bucket_name, Prefix = prefix, Delimiter = '/')
            self.write_logs(f"Returning list of objects in NEXRAD Bucket for selected prefix {prefix}: {result}")

            for i in result.get('CommonPrefixes'):
                path = i.get('Prefix').split('/')
                prefix_2 = prefix + path[-2] + "/"
                sub_folder = self.s3client.list_objects(Bucket = self.nexrad_bucket_name, Prefix = prefix_2, Delimiter = '/')
                
                for j in sub_folder.get('CommonPrefixes'):
                    sub_path = j.get('Prefix').split('/')
                    prefix_3 = prefix_2 + sub_path[-2] + "/"
                    sub_sub_folder = self.s3client.list_objects(Bucket = self.nexrad_bucket_name, Prefix = prefix_3, Delimiter = '/')

                    for k in sub_sub_folder.get('CommonPrefixes'):
                        sub_sub_path = k.get('Prefix').split('/')
                        sub_sub_path = sub_sub_path[:-1]
                        self.nexrad_data_dict['ID'].append(id)
                        self.nexrad_data_dict['Year'].append(sub_sub_path[0])
                        self.nexrad_data_dict['Month'].append(sub_sub_path[1])
                        self.nexrad_data_dict['Day'].append(sub_sub_path[2])
                        self.nexrad_data_dict['NexRad Station Code'].append(sub_sub_path[3])
                        id += 1
        
        nexrad_data = pd.DataFrame(self.nexrad_data_dict)
        self.write_logs(f"Returning metadata from NEXRAD Bucket: {nexrad_data}")
        return nexrad_data

    def nexradmap_data(self):
        response = requests.get(self.nexrad_map_data_url)
        lines = response.text.split('\n')
        
        id = 0
        nexradmap = []
        for line in lines:
            line = line.strip()
            word_list = line.split(" ")
            if (word_list[-1].upper() == 'NEXRAD'):
                nexradmap.append(line)
        nexradmap = [i for i in nexradmap if 'UNITED STATES' in i]
        
        for station in nexradmap:
            id += 1
            station1 = station.split("  ")
            station1 =  [i.strip() for i in station1 if i != ""]
            station2 = station.split(" ")
            station2 =  [i.strip() for i in station2 if i != ""]
            self.nexradmap_data_dict['ID'].append(id)
            self.nexradmap_data_dict['Station_Code'].append(station1[0].split(" ")[1])
            for i in range(len(station1)):
                if (re.match(r'\b[A-Z][A-Z]\b',station1[i].strip())):
                    self.nexradmap_data_dict['State'].append(station1[i][:2])
                    self.nexradmap_data_dict['County'].append(station1[i][2:])
            for i in range(len(station2)):
                if (re.match(r'^-?[0-9]\d(\.\d+)?$',station2[i])):
                    self.nexradmap_data_dict['latitude'].append(float(station2[i]))
                    self.nexradmap_data_dict['longitude'].append(float(station2[i+1]))
                    self.nexradmap_data_dict['elevation'].append(int(station2[i+2]))
                    break
        
        nexradmap_data = pd.DataFrame(self.nexradmap_data_dict)
        self.write_logs(f"Returning metadata for NEXRAD Map Locations: {nexradmap_data}")
        return nexradmap_data