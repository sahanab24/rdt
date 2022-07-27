import socket
from socket import *
import util


class Sender:
    def __init__(self):

        self.serverIp = '0.0.0.0'
        self.portNumber = 13918


    """
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
            
        Please check the main.py for a reference of how your function will be called.
    """

    """
    realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)
    Args:
        app_msg_str: the message string (to be put in the data field of the packet)
    """
    def rdt_send(self, app_msg_str):
        print("original message string: ", app_msg_str)

        clientSocket = socket(AF_INET, SOCK_DGRAM)

        seqNumber = util.getSequenceNumber()

        packet = util.make_packet(app_msg_str, 0, seqNumber)
        print("packet created: ", packet)

        while True:
            flag = self.send_packet(clientSocket, packet, seqNumber)

            if flag == 0:
                break
            elif flag == 1:
                print("receiver acked the previous pkt, resend!" + "\n")
                print("[ACK-Previous retransmission]:", app_msg_str)
            elif flag == 2:
                print("Socket timeout! Resend!" + "\n")
                print("[timeout retransmission]:", app_msg_str)
        clientSocket.close()

    """
      Args:  connection, packet and sequence number as input 

      Returns: return flag as output
   
         flag = 0 means no bit loss and timeout everything perfect
         flag = 1 means bit errors
         flag = 2 means timeout 
    """
    def send_packet(self, clientSocket, packet, seq):
        flag = 0
        clientSocket.sendto(packet, (self.serverIp, self.portNumber))
        clientSocket.settimeout(5)
        packetNumber = util.getPacketNumber()
        print("packet num.", packetNumber, " is successfully sent to the receiver.")

        try:
            modified_msg = clientSocket.recv(2048)
            L = [modified_msg[i:i + 1] for i in range(len(modified_msg))]
            length = b''.join(L[10:12]).hex()
            recvSeq = bin(int(length, 16))[2:].zfill(16)[-1]
            recvAck = bin(int(length, 16))[2:].zfill(16)[-2]
            if seq == int(recvSeq):
                print("packet is received correctly: seq. num ", int(seq), " = ACK num ", int(recvAck), ". all done!",
                      sep='')
                print()
                flag = 0
            else:
                flag = 1
        except timeout:
            flag = 2
        except socket.error:
            print("socket error occurred: ")
        return flag

    ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
    ####### function, which will be called by an application to                 #######
    ####### send a message. DO NOT Change the function name.                    #######
    ####### You can have other functions as needed.                             #######

    # write code for resending packet
