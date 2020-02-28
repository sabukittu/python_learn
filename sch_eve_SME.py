#!/usr/bin/python3
import MySQLdb
import csv
import sys
from datetime import timedelta
from datetime import datetime
from aws_conf import *
import boto3
from pprint import pprint
mydb = MySQLdb.connect(host=host, user=user,passwd=password,db=db)
cursor = mydb.cursor()
reg=['us-east-1']
def db():
    class event_det:
        def delete(self):
            cursor.execute("truncate table scheduled_events;")
            mydb.commit()
        def list_desc(self):
            sql ="INSERT INTO scheduled_events(EntityValue,Service,StartTime,EventTypeCode,AccountName,RegionName) VALUES(%s,%s,%s,%s,%s,%s);"
            try:
                res=client.describe_events( filter={'eventStatusCodes': ['upcoming','open' ] },)
                for i in res['events']:
                    arn=i['arn']
                    service=i['service']
                    startTime=i['startTime']
                    eventTypeCode=i['eventTypeCode']
                    region=i['region']
                    res1=client.describe_affected_entities(filter={ 'eventArns': [arn,],})
                    for j in res1['entities']:
                        entityValue=j['entityValue']
                       # print(entityValue,service,startTime,eventTypeCode,profn,region)
                        cursor.execute(sql,(entityValue,service,startTime,eventTypeCode,profn,region))
                        mydb.commit()
            except:
                pass
    event =event_det()
    event.delete()
    for profn in pro:
        for regn in reg:
            session = boto3.Session(profile_name=profn)
            client = session.client('health',region_name=regn)
            event.list_desc()
    cursor.close()
    mydb.close()
db()
print("Schedule Event - Success")
