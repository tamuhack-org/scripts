import boto3
import os
from tqdm import tqdm

#Name of the S3 Bucket you want to download from
bucketName = "2021-hh-resumes"

#Name of the directory within the bucket (leave blank if you want all files)
remote_dir = "prod/"

#Name of the local directory where you want to store files
local_dir = "./{}".format(bucketName)


s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketName)

#Count number of files and file size
total = 0
totalBytes = 0
for obj in bucket.objects.filter(Prefix=remote_dir):
    totalBytes += obj.size
    total += 1

#Print total download size
if totalBytes > 1000000000:
    print("Total Download Size: {}GB".format(round(totalBytes/1000000000, 2)))
elif totalBytes > 1000000:
    print("Total Download Size: {}MB".format(round(totalBytes/1000000, 2)))
elif totalBytes > 1000:
    print("Total Download Size: {}KB".format(round(totalBytes/1000, 2)))
else: 
    print("Total Download Size: {}B".format(totalBytes))

    
for obj in tqdm(bucket.objects.filter(Prefix=remote_dir), total=total):
    target = obj.key if local_dir is None \
        else os.path.join(local_dir, os.path.relpath(obj.key, remote_dir))
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))
    if obj.key[-1] == '/':
        continue
    bucket.download_file(obj.key, target)