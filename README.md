# TAMUhack Utility Scripts
This repo contains any scripts that we use regularly.

## Configure AWS CLI
Install the AWS CLI and configure with proper credentials.
```
npm install aws-sdk
aws configure
```

## S3 Resume Download
Install the Python requirements and change bucketName, remote_dir, and local_dir values as needed 
```
pip3 install -r requirements.py
python3 download_resumes_from_bucket.py
```