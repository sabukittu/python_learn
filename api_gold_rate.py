#!/usr/bin/env python

import mysql.connector
import requests
import json


def get_api_req():
	URL = 'http://goldpricez.com/api/rates/currency/inr/measure/gram'
	api_key = {'X-API-KEY': '9ee965c9c260543dfdd055e3718789019ee965c9'}
	x = requests.get(url = URL, params = api_key)
	y = x.json()
	details = json.loads(y)
	return details

def db_init(lis):
	mydb_connect = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="redhat",
	  database="gold_rate"
	)
	mycursor = mydb_connect.cursor()
	add = ("INSERT INTO RateINR "
             		 "(USDtoINR, GraminINR, UpdateTime) "
             		 "VALUES (%s, %s, %s)")

	mycursor.execute(add, lis)
	mydb_connect.commit()


def add_data(data):
	z = []
	z.append(data["usd_to_inr"])
	z.append(data["gram_in_inr"])
	z.append(data["gmt_inr_updated"])
	lis = (tuple(z))
	resp = db_init(lis)
	return resp

data = get_api_req()
add_data(data)


