#!/usr/bin/env python
# coding: utf-8

# In[4]:


# I am the Sender 
import socket
import sys
import random 
import _thread
import time
from timer_settings import Timer_settings
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('ex.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)






# Define Global parametrs used 

#    sender parameter

sender_ip_port = ('192.168.1.7', 0)
wait_to_receive_ack_interval = 0.05
packet_timeout_time = 0.5

#    reciver parameter


#    packet parameter

packet_size_bytes = 512

drop_packet_probability = 7

#    window parameter

window_size = 7
BASE = 0
MUTEX = _thread.allocate_lock()
time_to_send_packet = Timer_settings(packet_timeout_time)
file2 = open('ex.txt', 'w')

# define send function 
def send_file(senderSocket,filename):
    # step one open the file
    try:
        file = open(filename, 'rb')
    except IOError:
        print('Unable to open', filename)
        return
    # step two read the file make it packets and store it
    all_packets = []
    packet_num = 0
    while True:
        packet_data=file.read(packet_size_bytes)
        if not packet_data:
            break
        ####################################
        ## --packet_num--+--packet_data-- ##
        ####################################
        # note first we should convert packet num to string as packet_data is in byte
        packet=packet_num.to_bytes(4, byteorder = 'little', signed = True) + packet_data
        all_packets.append(packet)
        packet_num += 1
    # step three send the packets 
    # 1- intilize window size 
    global BASE
    global MUTEX
    global time_to_send_packet
    w_size=min(window_size,len(all_packets)-BASE)
    # 2- make the base to zero
    BASE = 0
    packet_turn = 0
    print('number of pakcets are',len(all_packets))
    # strat another thread(task) for the sender to wait for ACKs
    _thread.start_new_thread(ack_waiting_thread, (senderSocket,))
    line1=[]
    while len(all_packets) > BASE:
        MUTEX.acquire()
        while packet_turn < BASE + w_size:
            if random.randint(0, drop_packet_probability) > 0:
                print('Sending packet', packet_turn)
                now=time.time()
                file2.writelines("%s,%s\n"%(now,packet_turn))
                senderSocket.sendto(all_packets[packet_turn], receiver_ip_port)
            packet_turn += 1
        ## here the base should remove depending only reciving ACKs
        ## here i assumed i will recived all acks once -this simple but i will do it right in the next phase 
        
        if not time_to_send_packet.running_timer():
            print('Starting timer')
            time_to_send_packet.start_timer()

        while time_to_send_packet.running_timer() and not time_to_send_packet.timeout_timer():
            MUTEX.release()
            print('Waiting for ACks')
            time.sleep(wait_to_receive_ack_interval)
            MUTEX.acquire()

        if time_to_send_packet.timeout_timer():
            print('the allowed time has ended')
            time_to_send_packet.stop_timer();
            packet_turn = BASE
        else:
            print('Shifting window')
            w_size = min(window_size,len(all_packets)-BASE)
        MUTEX.release()
    if random.randint(0, drop_packet_probability) > 0:
        senderSocket.sendto(b'', receiver_ip_port)
    file.close()
    file2.close()

def ack_waiting_thread(sock):
    global MUTEX
    global BASE
    global time_to_send_packet

    while True:
        packet, addr = sock.recvfrom(1024)
        ack = int.from_bytes(packet[0:4], byteorder = 'little', signed = True)
        if (ack >= BASE):
            MUTEX.acquire()
            BASE = ack + 1
            print('ack received.. Base updated', BASE)
            time_to_send_packet.stop_timer()
            MUTEX.release()
if __name__=='__main__':
    # open the socket and bind it
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    senderSocket.bind(sender_ip_port)
    # read the file name and pass it to send function with the intilized socket 
    filename = sys.argv[1]
    myHostName = socket.gethostname()
    print("Name of the localhost is {}".format(myHostName))
    ip = socket.gethostbyname(myHostName)
    print("IP address of the localhost is {}".format(ip))
    receiver_ip_port = (sys.argv[2],int(sys.argv[3]))
    print(receiver_ip_port)
    start = time.time()
    send_file(senderSocket, filename)
    end = time.time()
    print(f"Runtime of the program is {end - start}")
    # close the socket 
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
    senderSocket.close()


# In[ ]:





