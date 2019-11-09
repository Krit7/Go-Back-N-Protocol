import socket
import pickle
import hashlib
import sys
import os
import math
import time
import random

def seqNo(x):
	return x%8

def Generate_Probability():
	x=random.uniform(0.4,0.7)
	return round(x,2)

host = ''
port = 3000

s = socket.socket()
print ("Socket successfully created")

s.bind((host, port))
print ("Socket binded to %s" %(port))

s.listen(1)
print ("Server is listening")

conn, addr = s.accept()
print('Connected by', addr)

N  = 7							#transmit-window size
Exp_Sn = seqNo(0)

ACK = 1
acks = []

Acc_Prob = 0.5

f = open("output.txt", "wb")
endoffile = False
lastpktreceived = time.time()	
starttime = time.time()

while True:
	try:
		pkt = conn.recv(4096)
		rcv_pkt=pickle.loads(pkt)
		recv_check_sum=rcv_pkt['check_sum']
		del rcv_pkt['check_sum']

		byte_rcv_pkt=pickle.dumps(rcv_pkt)
		calc_check_sum=hashlib.sha224(byte_rcv_pkt).hexdigest()
		
		p=Generate_Probability()
		print(p)
	
		if(calc_check_sum!=recv_check_sum):
			print("Error in Packet")
		else:
			if(rcv_pkt['sq_no']!=Exp_Sn):
				print ("Received out of order", rcv_pkt['sq_no'])
				ack_pkt={
				'sq_no': Exp_Sn
				}
				# Convert The Packet Into Byte Format
				byte_pkt=pickle.dumps(ack_pkt)

				# Create Checksum 
				check_sum=hashlib.sha224(byte_pkt).hexdigest()

				# Add Checksum to Pakect
				ack_pkt['check_sum']=check_sum

				# Send Packet
				conn.sendall(pickle.dumps(ack_pkt))
				print('Ack Of Same Packet', repr(Exp_Sn))
			else:
				print ("Received inorder", Exp_Sn)
				
				if rcv_pkt['data']:
					f.write(rcv_pkt['data'])
				else:
					endoffile = True
				
				Exp_Sn=seqNo(Exp_Sn+1)
				
				ack_pkt={
				'sq_no': Exp_Sn
				}
				# Convert The Packet Into Byte Format
				byte_pkt=pickle.dumps(ack_pkt)

				# Create Checksum 
				check_sum=hashlib.sha224(byte_pkt).hexdigest()

				# Add Checksum to Pakect
				ack_pkt['check_sum']=check_sum
				# Send Packet
				conn.sendall(pickle.dumps(ack_pkt))
				print('New Ack', repr(Exp_Sn))

	except Exception as e:
		if endoffile:
			if(time.time()-lastpktreceived>1):
				break
	

endtime = time.time()

f.close()
print ('FILE TRANFER SUCCESSFUL')
print ("TIME TAKEN " , str(endtime - starttime))

conn.close()
print("Server Disconnected")

