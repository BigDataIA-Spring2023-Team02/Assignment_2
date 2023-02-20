import os
import time
import boto3
from dotenv import load_dotenv
import streamlit as st

class AWS_Main:
    def __init__(self):
        load_dotenv ()

        self.s3client = boto3.client('s3',
                                region_name = 'us-east-1',
                                aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                                aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                                )
        
        self.s3resource = boto3.resource('s3',
                                region_name = 'us-east-1',
                                aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                                aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                                )
        
        self.clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOGS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOGS_SECRET_KEY')
                        )
        
        self.geos_bucket_name = "noaa-goes18"
        self.nexrad_bucket_name = "noaa-nexrad-level2"
    
    def write_logs(self, message: str):
        self.clientLogs.put_log_events(
            logGroupName = "Assignment02-logs",
            logStreamName = "AWS-Logs",
            logEvents = [
                {
                    'timestamp' : int(time.time() * 1e3),
                    'message' : message
                }
            ]
        )
    
    def list_files_in_user_bucket(self):
        my_bucket = self.s3client.list_objects_v2(Bucket = os.environ.get('USER_BUCKET_NAME')).get('Contents')
        file_list = []
        for file in my_bucket:
            file_list.append(file['Key'])
        self.write_logs(f"Returning list of files in User Bucket: {file_list}")
        return file_list

    def list_files_in_noaa_goes18_bucket(self, product, year, day, hour):
        prefix = product + '/' + year + '/' + day + '/' + hour + '/'
        geos_bucket = self.s3client.list_objects(Bucket = self.geos_bucket_name, Prefix = prefix).get('Contents')
        file_list = []
        for objects in geos_bucket:
            file_path = objects['Key']
            file_path = file_path.split('/')
            file_list.append(file_path[-1])
        self.write_logs(f"Returning list of files in GOES18 Bucket for Selected prefix {prefix}: {file_list}")
        return file_list

    def list_files_in_noaa_nexrad_bucket(self, year, month, day, station):
        prefix = year + '/' + month + '/' + day + '/' + station + '/'
        nexrad_bucket = self.s3client.list_objects(Bucket = self.nexrad_bucket_name, Prefix = prefix).get('Contents')
        file_list = []
        for objects in nexrad_bucket:
            file_path = objects['Key']
            file_path = file_path.split('/')
            file_list.append(file_path[-1])
        self.write_logs(f"Returning list of files in NEXRAD Bucket for Selected prefix {prefix}: {file_list}")
        return file_list

    def copy_file_to_user_bucket(self, selected_file, file_input, satellite_input):
        user_bucket = self.s3resource.Bucket(os.environ.get('USER_BUCKET_NAME'))
        
        if satellite_input == 'geos18':
            user_folder = 'GOES18/'
            file_key = user_folder + file_input
            url_s3 = 'https://damg-7245-projects.s3.amazonaws.com/' + file_key
            url_noaa = 'https://noaa-goes18.s3.amazonaws.com/' + selected_file
            copy_source = {
                'Bucket': self.geos_bucket_name,
                'Key': selected_file
                }
        
        elif satellite_input == 'nexrad':
            user_folder = 'NEXRAD/'
            file_key = user_folder + file_input
            url_s3 = 'https://damg-7245-projects.s3.amazonaws.com/' + file_key
            url_noaa = 'https://noaa-nexrad-level2.s3.amazonaws.com/' + selected_file
            copy_source = {
                'Bucket': self.nexrad_bucket_name,
                'Key': selected_file
                }
        
        for file in user_bucket.objects.all():
            if(file.key == file_key):
                self.write_logs(f"Sorry !!! Cannot copy a file that is already present in the user bucket")
                st.warning('File already available in user bucket, so cannot copy the file')
                st.write('DOWNLOAD the file from the below link using URL to already existing file on local S3 bucket: ')
                self.write_logs(f"Returning file link available in user bucket for selected file {file_input}: {url_s3}")
                st.write('File Link in S3 Bucket !!!\n', url_s3)
                return url_s3, url_noaa

        user_bucket.copy(copy_source, file_key)
        self.write_logs(f"Returning file link available in user bucket for selected file {file_input}: {url_s3}")
        st.success('File Copied Succesfully in the user bucket')
        st.write('File Link in S3 Bucket !!!\n', url_s3)
        self.write_logs(f"Returning file link from NOAA bucket for selected file {file_input}: {url_noaa}")
        st.write('File Link in NOAA Bucket !!!\n', url_noaa)
        return url_s3, url_noaa