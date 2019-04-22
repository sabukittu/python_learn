#!/usr/bin/env python

## This script is used to get data from goldpricez.com using an API 
## request and store the data to database 'gold_rate' 
## Then fetch the data from database and will send a mail with 
## 'GramPrice', 'PavanPrice', 'Status'.

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import mysql.connector
import requests
import json


## get_api_req() function is used to get api request from goldpricez.com
## its in JSON format
def get_api_req():

	URL = 'http://goldpricez.com/api/rates/currency/inr/measure/gram'
	api_key = {'X-API-KEY': '9ee965c9c260543dfdd055e3718789019ee965c9'}

	x = requests.get(url = URL, params = api_key)
	y = x.json()
	data = json.loads(y)

	return data


## These 2 line of code is using to establish a connection 
## with the database.
try:
	mydb = mysql.connector.connect(host='localhost', database='gold_rate', user='root', password='redhat')
	cursor = mydb.cursor()
except Exception as e:
	print("\n\033[1;31;40m"+(str(e))+"\033[1;0;40m\n")
	exit(1)


## add_data() function is using to insert the data to database gold_rate
## the values are fetched from api_get_req()
def add_data(mydb, cursor, data):

	z = []
	z.append(data["usd_to_inr"])
	z.append(data["gram_in_inr"])
	z.append(data["gmt_inr_updated"])
	lis = (tuple(z))

	try:
		add = ("INSERT INTO RateINR "
				"(USDtoINR, GraminINR, UpdateTime, CurrentDate, CurrentTime) "
				"VALUES (%s, %s, %s, CURDATE(), CURTIME())")
		cursor.execute(add, lis)
		resp = mydb.commit() 
	except Exception as e:
		resp = 'Database is upto Date'

	return resp

## Main Execution of the script, adding data to DB.
data = get_api_req()
add_data(mydb, cursor, data)

## db_query() function is used to query the details from database gold_rate
## the return 'd' value will be dict contain list
def db_query(cursor):

	ii = ("SELECT * FROM RateINR ORDER BY CurrentDate DESC LIMIT 0,2")
	cursor.execute(ii)
	fetch = cursor.fetchall()

	prev = (list(fetch[1]))
	pr = (prev[1])
	last = (list(fetch[0]))
	la = (last[1])

	f = (float(la))
	e = (float(pr))

	previous_rate = (8 * e)
	latest_rate = (8 * f)
	diff = (latest_rate - previous_rate)
	
	if diff > 0:
		stats = 'HIGH'
	else:
		stats = 'LOW'
	
	calc = [latest_rate, previous_rate, diff, stats]
	d = {}
	d['latest'] = last
	d['prev'] = prev
	d['calc'] = calc

	return d


## These are the values of rates fetched from
## db_query() function 
a = db_query(cursor)

cu_dt = (a['latest'][3])
up_dt = (a['latest'][2])
gm_lr = (round((float(a['latest'][1])),2))
gm_pr = (round((float(a['prev'][1])),2))
pv_lr = (round((float(a['calc'][0])),2))
pv_pr = (round((float(a['calc'][1])),2))

diff = (round((float(a['calc'][2])),2))
stat = (a['calc'][3])


## mail_sender() function is using to send a mail with the current 
## gold rate with comparison with previous date
def mail_sender(up_dt, gm_lr, gm_pr, pv_lr, pv_pr, diff, stat):

	sender_email = "esskayrengan@gmail.com"
	print('\n    Sender Email : "esskayrengan@gmail.com"')
	password = getpass.getpass()
#	password = 'redhat123'
	receiver_email = input("\n    Receiver Email : ")


	message = MIMEMultipart("alternative")
	message["Subject"] = "Gold Rate"
	message["From"] = sender_email
	message["To"] = receiver_email

# Create the plain-text and HTML version of your message
	html = """\
	<html>
	   <head>
	      <style>
	         table, th, td {
	            border: 1px  solid black;
	         }
	      </style>
	   </head>
	   <body>
	      <h1>Gold Rate</h1>

	      <table>
	         <tr>
	            <th>Commodity</th>
	            <th>UpdatedDate</th>
	            <th>GramRate(Yesterday)</th>
	            <th>PavanRate(Yesterday)</th>
	            <th>GramRate(Today)</th>
	            <th>PavanRate(Today)</th>
	            <th>Difference</th>
	            <th>Status</th>
	         </tr>
	         <tr>
	            <td> GOLD </td>
	            <td> %s </td>
	            <td> Rs. %s </td>
	            <td> Rs. %s </td>
	            <td> Rs. %s </td>
	            <td> Rs. %s </td>
	            <td> %s </td>
	            <td> %s </td>
	         </tr>
	      </table>
	   </body>
	</html>
	""" % (up_dt, gm_pr, pv_pr, gm_lr, pv_lr, diff, stat)

# Turn these into plain/html MIMEText objects
	part1 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
	message.attach(part1)

# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		try:
			server.login(sender_email, password)
			server.sendmail(
	        	sender_email, receiver_email, message.as_string()
			)
			resp = print('\n\033[1;32;40m    Mail sent ...!\033[1;0;40m\n')
		except Exception as e:
			resp = print('\n\033[1;31;40m    Something went wrong ...!\033[1;0;40m\n')
	return resp 


## Sending the composed mail
mail_sender(up_dt, gm_lr, gm_pr, pv_lr, pv_pr, diff, stat)

