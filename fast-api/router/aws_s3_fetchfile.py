import re
import os
import boto3
import requests
from pathlib import Path
from dotenv import load_dotenv
from jwt_api import get_current_user
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, status, HTTPException, Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

dotenv_path = Path('./.env')
load_dotenv(dotenv_path)

router = APIRouter(
    prefix="/aws-s3-fetchfile",
    tags=['aws-s3-fetchfile']
)

@router.post('/goes18', status_code=status.HTTP_200_OK)
async def generate_goes_url(file_input : str, token: str = Depends(oauth2_scheme)):
    user_id = get_current_user(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )
    
    input_url = "https://noaa-goes18.s3.amazonaws.com/"
    file_name = file_input.strip()
    if (re.match(r'[O][R][_][A-Z]{3}[-][A-Za-z0-9]{2,3}[-][A-Za-z0-9]{4,6}[-][A-Z0-9]{2,5}[_][G][1][8][_][s][0-9]{14}[_][e][0-9]{14}[_][c][0-9]{14}\b', file_name)):
        file_name = file_name.split("_")
        file_split = file_name[1].split('-')
        
        no_digits = []
        for i in file_split[2]:
            if not i.isdigit():
                no_digits.append(i)
        
        str_2 = ''.join(no_digits)
        
        year = file_name[3][1:5]
        day = file_name[3][5:8]
        hour = file_name[3][8:10]
        final_url = input_url + file_split[0] + '-' + file_split[1] + '-' + str_2 + '/' + year + '/' + day + '/' + hour + '/' + file_input
        response = requests.get(final_url)
        if(response.status_code == 404):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail= "No such file exists at GOES18 location")
        return final_url
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail= "Invalid filename format for GOES18")

@router.post('/nexrad', status_code=status.HTTP_200_OK)
async def generate_nexrad_url(file_input : str, token: str = Depends(oauth2_scheme)):
    user_id = get_current_user(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )

    input_url = "https://noaa-nexrad-level2.s3.amazonaws.com/"
    file_name = file_input.strip()
    if (re.match(r'[A-Z]{3}[A-Z0-9][0-9]{8}[_][0-9]{6}[_]{0,1}[A-Z]{0,1}[0-9]{0,2}[_]{0,1}[A-Z]{0,3}\b', file_name)):
        final_url = input_url+file_name[4:8]+"/"+file_name[8:10]+"/"+file_name[10:12]+"/"+file_name[:4]+"/"+file_input
        response = requests.get(final_url)
        if(response.status_code == 404):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail= "No such file exists at NEXRAD location")
        return final_url

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail= "Invalid filename format for NEXRAD")