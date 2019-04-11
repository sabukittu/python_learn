#!/usr/bin/env python


import mysql.connector
import requests
import json


def get_api_req():
	URL = 'https://jsonplaceholder.typicode.com/users/'
	x = requests.get(url = URL)
	data = x.json()
	return data


def db_init(lis):
	mydb_connect = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="redhat",
	  database="api_get_req_data"
	)
	mycursor = mydb_connect.cursor()
	add = ("INSERT INTO API_REQ_DETAILS "
             		 "(Name, UserName, Email, Phone, WebSite) "
             		 "VALUES (%s, %s, %s, %s, %s)")

	mycursor.execute(add, lis)
	mydb_connect.commit()


def add_data(data):
	for name in data:
		z = []
		z.append(name["name"])
		z.append(name["username"])
		z.append(name["email"])
		z.append(name["phone"])
		z.append(name["website"])
		lis = (tuple(z))
		resp = db_init(lis)
	return resp

data = get_api_req()
add_data(data)

