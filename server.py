#!/usr/bin/env python

import asyncio
import websockets
import os
import threading
import time
import sys

testing = 0 # repalce by 1 for testing

def control_evets(msg):
	try:
		keys,mouse,pointer = msg.split('|')
		m_events = mouse.split(',')
		
		for event in m_events:
			if event != "":
				x,y,e=event.split(' ')
				os.system("python mouse.py 1 "+x+" "+y+" "+e)
		x,y=pointer.split(',')
		if not testing:
			os.system("python mouse.py 0 "+x+" "+y)
	except ValueError:
		pass

pwd="default"
@asyncio.coroutine
def hello(websocket, path):
	print("New connection established")
	while 1:
		inp = yield from websocket.recv()
		if(inp=="exit"):
			return
		if(inp==pwd):
			break
		yield from websocket.send("error")

	yield from websocket.send("connect")
	while 1:
		inp = yield from websocket.recv()
		if(inp=="exit"):
			break
		control_evets(inp)
		os.system("python testsc.py > out")
		f=open("out",'r')
		greeting=f.read()
		yield from websocket.send(greeting)

arg= sys.argv
if len(arg) > 1:
	testing=1

while 1:
	print("Input server password : " , end="")
	password = input()
	print("Retype server password : ", end="")
	repassword = input()

	if(password==repassword):
		pwd=password
		break;

	print("Password mismatch")

print("Server started...")
start_server = websockets.serve(hello, '', 7861)
i=0

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
