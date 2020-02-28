#!/usr/local/bin/python3

import boto3
import datetime
from datetime import datetime
from datetime import timedelta


account_name = 'AWS-Production'
profile = boto3.Session(region_name='us-east-1',profile_name=account_name)
events = profile.client('health')
response = events.describe_events() #filter={'eventStatusCodes':['upcoming']}

#print(response)

print((datetime.now() - timedelta(1)).date())

#current_date = datetime.now()
# #print((datetime.now()).date())

for x in response['events']:
    a = 2019-10-14
    if x['statusCode'] == 'open' and (x['startTime']).date() == (datetime.now() - timedelta(1)).date() :#(datetime.now()).date() :
        print("Account Name\t"+"Event\t"+"Service\t"+"\t\t\tDate"+"\t\tRegion")
        print(account_name+'\t'+x['service']+'\t'+str(x['eventTypeCode'])+'\t'+str((x['startTime']).date())+'\t'+str(x['region']))









        #a = ['service','eventTypeCode','region']
        #c = (' '.join(a))
        #print(a)
       # b = []
        #for x in a:
            #print(x)
            #b.append(x[a])
        #y = x['startTime']
        
        
        
        # print(y.date())
        # print(x['service'])
        # print(x['eventTypeCode'])
        # print(x['region'])
           
#print(c)
