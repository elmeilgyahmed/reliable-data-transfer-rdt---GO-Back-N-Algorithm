#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[4]:


# I am the Reciver
import socket
import sys
import random 


# Define Global parametrs used 
drop_packet_probability = 7

#    reciver parameter

receiver_ip_port = ('192.168.1.7', 8080)



# define send function 
def receiver_file(receiverSocket,filename):
    # step one open the file
    try:
        file = open(filename, 'wb')
    except IOError:
        print('Unable to open', filename)
        return
    # step
    tmmam_ack_num = 0 
    while True:
        packet, addr = receiverSocket.recvfrom(1024)
        if not packet:
            break
        ####################################
        ## --packet_num--+--packet_data-- ##
        ####################################
        # note , first we should convert packet num to string as packet_data is in byte
        packet_num = int.from_bytes(packet[0:4], byteorder = 'little', signed = True)
        packet_data=packet[4:]
        print('Recived Packet',packet_num)
        ## Here i assumed that i sent all ACKs 
        
        # it will be implmented in the next phase 
        
        
        ######################################
        #                                    #
        #                                    #
        #         ACKs sent                  #
        #                                    #
        #                                    #
        ######################################
        # phase two begins send acks backs to sender 
        if packet_num == tmmam_ack_num :
            print('Sending ACK', tmmam_ack_num)
            ack=tmmam_ack_num.to_bytes(4, byteorder = 'little', signed = True)
            if random.randint(0, drop_packet_probability) > 0:
                receiverSocket.sendto(ack, addr)
            tmmam_ack_num += 1
            file.write(packet_data)
        else:
            print('Sending ACK', tmmam_ack_num - 1)
            updated_ack=tmmam_ack_num-1
            ack = updated_ack.to_bytes(4, byteorder = 'little', signed = True)
            if random.randint(0, drop_packet_probability) > 0:
                receiverSocket.sendto(ack, addr)

    file.close()
if __name__=='__main__':
    # open the socket and bind it
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiverSocket.bind(receiver_ip_port)
    # read the file name and pass it to send function with the intilized socket 
    myHostName = socket.gethostname()
    print("Name of the localhost is {}".format(myHostName))
    ip = socket.gethostbyname(myHostName)
    print("IP address of the localhost is {}".format(ip))
    filename = sys.argv[1]
    receiver_file(receiverSocket, filename)
    # close the socket 
    receiverSocket.close()


# In[ ]:




