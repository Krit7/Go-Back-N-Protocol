# Go-Back-N-Protocol
1. Go-Back-N is implemented in such a way that the sender sends the frame again if he receives the ACK of the same frame he has sent previously.

2. Frame Consists :
Frame={
	'sq_no' : ,
	'data' : ,
	'chck_sum' : ,
}
sq_no : Sequence number of the frame to be sent
data : The data to be sent
chck_sum : Hashed value of the packet to be sent


3. The frames are dropeed with probability P which is randomly generated.Also, the protocol is designed such that when a packet is dropped 1 time, it is assigned a priority value such that it can’t be dropped another time. This is to ensure that a packet is not dropped an infinite number of times and hence all the data reaches the server. 

4. Results:-
First Frame Sent Time
Frist Frame Received Time
Avg. Number of Frames Sent
Start-Time and End-Time

5. You can use the same code to run the application (server and client) on the same machine by running both of them on differnet terminal using command :- python server.py/client.py

6. The "file.txt" contains the content that is being sent by the client to the server for and the "output.txt" contains the received text received by the server from client.


