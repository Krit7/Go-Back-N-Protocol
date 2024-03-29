import socket
import pickle
import hashlib
import sys
import os
import math
import time

def seqNo(x):
	return x%8

def Check_Window_Size(Sb,Sn,N):
	if(Sb+Sn<N):
		return True
	return False

host = socket.gethostbyname('')    
port = 3000					#ILOVEYOU3000

s = socket.socket()
s.connect((host, port))

window=[]
N = 7
Sn=seqNo(0)
Sb=seqNo(0)

first_frame_check=True
read_count=1
frame_sent_count=0

#SENDS DATA
fileOpen= open('data.txt', 'rb') 
data = fileOpen.read(50)
done = False

lastackreceived = time.time()
starttime = time.time()

while not done:
	if (Check_Window_Size) :
		# Create a new packet packet(sq_no,data,check_sum)
		if(Sb==Sn):
			pkt={
			'sq_no' : Sn ,
			'data' : data,
			}

			# Convert The Packet Into Byte Format
			byte_pkt=pickle.dumps(pkt)
			
			# Create Checksum 
			check_sum=hashlib.sha224(byte_pkt).hexdigest()
			
			# Add Checksum to Pakect
			pkt['check_sum']=check_sum
			
			# Send Packet
			s.sendall(pickle.dumps(pkt))
			print('Sent Packet', repr(Sn))
			
			if first_frame_check:
				first_frame_time=time.time()
				first_frame_check=False

			frame_sent_count=frame_sent_count+1

			# Increment Sn for sending next packet
			Sn=seqNo(Sn+1)

			#check if EOF has reached
			if(not data):
				done = True
			
			#append packet to window
			window.append(pkt)

			#read more data
			data = fileOpen.read(50)
			read_count=read_count+1
		else:

			s.sendall(pickle.dumps(window[0]))
			
			if first_frame_check:
				first_frame_time=time.time()
				first_frame_check=False
			
			del window[0]
			print('Sent Packet After Drop', repr(Sb))
			Sb = seqNo(Sb + 1)
			frame_sent_count=frame_sent_count+1


	try:
		pkt = s.recv(4096)
		rcv_pkt=pickle.loads(pkt)

		recv_check_sum=rcv_pkt['check_sum']
		del rcv_pkt['check_sum']

		byte_rcv_pkt=pickle.dumps(rcv_pkt)
		calc_check_sum=hashlib.sha224(byte_rcv_pkt).hexdigest()

		if(calc_check_sum!=recv_check_sum):
			print("Error in Ack")
		else:
			print('Received Ack for Packet', repr(rcv_pkt['sq_no']))
			if rcv_pkt['sq_no']>Sb or (rcv_pkt['sq_no']==0 and Sb==7):
				lastackreceived = time.time()
				del window[0]
				Sb = seqNo(Sb + 1)
			
				
	except Exception as e:
		curr_time=time.time()
		transmisiom_time=curr_time-lastackreceived
		if(transmisiom_time>0.01):
			for i in window:
				s.sendall(pickle.dumps(i))

endtime = time.time()

fileOpen.close()  
s.close()

print ('FILE TRANFER SUCCESSFUL')
print("Client Disconnected")

print("--------------------------")

print("Start Time", starttime)
print("First Frame Sent at",first_frame_time)
print("End Time", endtime)

avg_frame_sent=frame_sent_count/read_count
print("Average Number of Frame Sent",avg_frame_sent)

print("--------------------------")



