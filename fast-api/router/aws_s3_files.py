import os
import boto3
from fastapi import APIRouter, status, HTTPException
from dotenv import load_dotenv

#load env variables
load_dotenv()
router = APIRouter(
    prefix="/aws-s3-files",
    tags=['aws-s3-files']
)

@router.get('/goes18', status_code=status.HTTP_200_OK)
async def list_files_in_goes18_bucket(year : str, day : str, hour : str, product : str = "ABI-L1b-RadC"):
    geos_bucket_name = "noaa-goes18"
    s3client = boto3.client('s3',
                            region_name = 'us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                            )
    s3resource = boto3.resource('s3',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )
    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )
    file_list = []
    prefix = product+'/'+year+'/'+day+'/'+hour+'/'
    geos_bucket = s3client.list_objects(Bucket = geos_bucket_name, Prefix = prefix).get('Contents')
    for objects in geos_bucket:
        file_path = objects['Key']
        file_path = file_path.split('/')
        file_list.append(file_path[-1])
    if (len(file_list)!=0):
        return file_list
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "Unable to fetch filenames from S3 bucket")

@router.get('/nexrad', status_code=status.HTTP_200_OK)
async def list_files_in_nexrad_bucket(year : str, month : str, day : str, nexrad_station : str):
    nexrad_bucket_name = "noaa-nexrad-level2"
    s3client = boto3.client('s3',
                            region_name = 'us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                            )
    s3resource = boto3.resource('s3',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )
    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )
    file_list = []
    prefix = year+'/'+month+'/'+day+'/'+nexrad_station+'/'
    nexrad_bucket = s3client.list_objects(Bucket = nexrad_bucket_name, Prefix = prefix).get('Contents')
    for objects in nexrad_bucket:
        file_path = objects['Key']
        file_path = file_path.split('/')
        file_list.append(file_path[-1])
    if (len(file_list)!=0):
        return file_list
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "Unable to fetch filenames from S3 bucket")

@router.post('/goes18/copyfile', status_code=status.HTTP_200_OK)
async def copy_goes_file_to_user_bucket(file_name : str, product : str, year : str, day : str, hour : str):
    geos_bucket_name = "noaa-goes18"
    s3client = boto3.client('s3',
                            region_name = 'us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                            )
    s3resource = boto3.resource('s3',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )
    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )
    try:
        destination_bucket = s3resource.Bucket(os.environ.get('USER_BUCKET_NAME'))
        all_selections_string = product+'/'+year+'/'+day+'/'+hour+'/'+file_name
        destination_folder = 'GOES18/'
        destination_key = destination_folder + file_name
        url_to_mys3 = 'https://damg-7245-projects.s3.amazonaws.com/' + destination_key
        copy_source = {
            'Bucket': geos_bucket_name,
            'Key': all_selections_string
            }
        for file in destination_bucket.objects.all():
            if(file.key == destination_key):
                return url_to_mys3
        destination_bucket.copy(copy_source, destination_key)
        return url_to_mys3
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "Unable to copy file")

@router.post('/nexrad/copyfile', status_code=status.HTTP_200_OK)
def copy_nexrad_file_to_user_bucket(file_name : str, year : str, month : str, day : str, ground_station : str):
    nexrad_bucket_name = "noaa-nexrad-level2"
    s3client = boto3.client('s3',
                            region_name = 'us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                            )
    s3resource = boto3.resource('s3',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )
    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )
    try:
        destination_bucket = s3resource.Bucket(os.environ.get('USER_BUCKET_NAME'))
        all_selections_string = year+'/'+month+'/'+day+'/'+ground_station+'/'+file_name
        destination_folder = 'NEXRAD/'
        destination_key = destination_folder + file_name
        url_to_mys3 = 'https://damg-7245-projects.s3.amazonaws.com/' + destination_key
        copy_source = {     #define the copy source bucket as NEXRAD bucket
            'Bucket': nexrad_bucket_name,
            'Key': all_selections_string
            }
        for file in destination_bucket.objects.all():
            if(file.key == destination_key):    #if selected file already exists at destination bucket
                return url_to_mys3
        destination_bucket.copy(copy_source, destination_key)   #copy file to destination bucket
        return url_to_mys3
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "Unable to copy file")