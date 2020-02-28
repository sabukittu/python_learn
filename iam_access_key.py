#!/usr/local/bin/python3

import boto3
import json
import datetime
import sys
import csv

if len (sys.argv) == 2: 
    acc_name = sys.argv[1]
    profile = boto3.Session(profile_name=acc_name)
    iam = profile.client('iam')
    user_list = iam.list_users()
    current = datetime.datetime.now(datetime.timezone.utc)
else:
    print("\n"+'   Usage:-   iam_access_key.py "AWS Profile Name"'+"\n")
    exit(1)

def FILE_CSV():
    row = ['Username','Access Keys','Days']
    with open('/Users/kittusabu/Desktop/access.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

def IAM_ACCESS_KEY(lists,identity,date):
    for user in lists['Users']:
        row = []
        user_name = user['UserName']
        access_keys = identity.list_access_keys(UserName=user_name)
        for l in access_keys['AccessKeyMetadata']:
            dt = l['CreateDate']
            key = l['AccessKeyId']
            num_days = date-dt
            if l['Status'] == 'Active':
                row = [user_name,key,str(num_days.days)]
                with open('/Users/kittusabu/Desktop/access.csv', 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                    csvFile.close()
    print("\n"+"  List Generated:-"+'  "/Users/kittusabu/Desktop/access.csv"'+"\n")

FILE_CSV()
IAM_ACCESS_KEY(lists=user_list,identity=iam,date=current)
        