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
	x=random.uniform(0.45,0.7)
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
if_dropped=0
first_frame_check=True

f = open("output.txt", "wb")
endoffile = False

lastpktreceived = time.time()	
starttime = time.time()

while True:
	p=Generate_Probability()
	try:
		pkt = conn.recv(4096)
		rcv_pkt=pickle.loads(pkt)
		recv_check_sum=rcv_pkt['check_sum']
		del rcv_pkt['check_sum']

		byte_rcv_pkt=pickle.dumps(rcv_pkt)
		calc_check_sum=hashlib.sha224(byte_rcv_pkt).hexdigest()
		
		if (p>Acc_Prob or if_dropped==1):
			if(calc_check_sum!=recv_check_sum):
				print("Error in Packet")

			else:
				if(rcv_pkt['sq_no']==Exp_Sn):
					if_dropped=0
					
					if first_frame_check:
						first_frame_time=time.time()
						first_frame_check=False
					
					
					print ("Received Packet inorder", Exp_Sn)
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
					print('New Ack Sent For', repr(Exp_Sn))
		else:
			if_dropped=1
			print ("Packet Dropped", rcv_pkt['sq_no'])
					
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
			print('Ack Sent For Same Packet', repr(Exp_Sn))

	except Exception as e:
		break

endtime = time.time()

f.close()
conn.close()

print ('FILE TRANFER SUCCESSFUL')
print("Server Disconnected")

print("--------------------------")

print("Start Time", starttime)
print("First Frame Received at",first_frame_time)
print("End Time", endtime)

print("--------------------------")


