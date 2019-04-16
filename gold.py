#!/usr/bin/env python

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import mysql.connector
import requests
import json


def get_api_req():
   URL = 'http://goldpricez.com/api/rates/currency/inr/measure/gram'
   api_key = {'X-API-KEY': '9ee965c9c260543dfdd055e3718789019ee965c9'}
   x = requests.get(url = URL, params = api_key)
   y = x.json()
   data = json.loads(y)
   return data

data = get_api_req()
mydb = mysql.connector.connect(host='localhost', database='gold_rate', user='root', password='redhat')
cursor = mydb.cursor()


def db_query(cursor):
   ii = ("SELECT GraminINR FROM RateINR ORDER BY CurrentDate DESC LIMIT 0,2")
   cursor.execute(ii)
   fetch = cursor.fetchall()
   prev = (list(fetch[1]))
   last = (list(fetch[0]))
   d = (float(last[0]))
   e = (float(prev[0]))
   previous_rate = (8 * e)
   latest_rate = (8 * d)
   diff = (latest_rate - previous_rate)
   if diff > 0:
     stats = 'HIGH'
   else:
     stats = 'LOW'
   calc = [latest_rate, previous_rate, diff, stats]

   oo = ("SELECT * FROM RateINR ORDER BY CurrentDate DESC LIMIT 0,2")
   cursor.execute(oo)
   fetch = cursor.fetchall()
   d = {}
   l = (list(fetch[0]))
   p = (list(fetch[1]))
   d['latest'] = l
   d['prev'] = p
   d['calc'] = calc
   return d

a = db_query(cursor)
cu_dt = (a['latest'][3])
up_dt = (a['latest'][2])
gm_lr = (round((float(a['latest'][1])),2))
gm_pr = (round((float(a['prev'][1])),2))
pv_lr = (round((float(a['calc'][0])),2))
pv_pr = (round((float(a['calc'][1])),2))
diff = (round((float(a['calc'][2])),2))
stat = (a['calc'][3])


def db_insert(mydb, cursor, lis):
	add = ("INSERT INTO RateINR "
         		"(USDtoINR, GraminINR, UpdateTime, CurrentDate, CurrentTime) "
             	"VALUES (%s, %s, %s, CURDATE(), CURTIME())")
	cursor.execute(add, lis)
	mydb.commit()


def add_data(mydb, cursor, data):
	z = []
	z.append(data["usd_to_inr"])
	z.append(data["gram_in_inr"])
	z.append(data["gmt_inr_updated"])
	lis = (tuple(z))
	try:
	    resp = db_insert(mydb, cursor, lis)
	except Exception as e:
		resp = print('Database is upto Date')
	return resp


def mail_sender(up_dt, gm_lr, gm_pr, pv_lr, pv_pr, diff, stat):
	sender_email = "esskayrengan@gmail.com"
	receiver_email = "sabukittu@gmail.com"
#	password = getpass.getpass()
	password = 'redhat123'

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
	    server.login(sender_email, password)
	    server.sendmail(
	        sender_email, receiver_email, message.as_string()
	    )



add_data(mydb, cursor, data)
mail_sender(up_dt, gm_lr, gm_pr, pv_lr, pv_pr, diff, stat)







