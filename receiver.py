from socket import *
from time import sleep
import util
import time

portNumber = 13918

# creating socket by specifying the ip address family and transport service
# AF_INET = IPV4, SOCK_DGRAM = UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', int(portNumber)))

# Variable declaration
expected_seq_num = 0
expected_ack_num = 1
packetNumber = 1

print("Receiver ready to serve...")

# Stimulating timeout event
def timeOutEvent():
    time.sleep(3)
    print("simulating packet loss: sleep a while to trigger timeout event on the send side...")
    pass

# Stimulating packet corruption event
def bitErrorsEvent():
    time.sleep(3)
    print("simulating packet bit errors/corrupted: ACK the previous packet!")
    packet = util.make_packet('', int((expected_seq_num + 1) % 2), int((expected_seq_num + 1) % 2))
    serverSocket.sendto(packet, address)

# extracting data, length, seq, ack information from the sender packet
def extractFromPacket(packet):
    L = [packet[i:i + 1] for i in range(len(packet))]
    data = b''.join(L[12:])
    length = b''.join(L[10:12]).hex()
    seq = bin(int(length, 16))[2:].zfill(16)[-1]
    ack = bin(int(length, 16))[2:].zfill(16)[-2]

    return data, length, seq, ack

# waiting to receive data
while True:
    # receiving data from sender packet
    packet, address = serverSocket.recvfrom(1024)
    print("packet num.", packetNumber, " received: ", packet)

    # check whether checksum is true or not and storing in flag variable
    flag = util.verify_checksum(packet)

    if packetNumber % 6 == 0:
        timeOutEvent()

    elif packetNumber % 3 == 0:
        bitErrorsEvent()

    else:
        data, length, seq, ack = extractFromPacket(packet)

        if int(seq) == expected_seq_num and flag:
            print("packet is expected, message string delivered:", data.decode())
            print("packet is delivered, now creating and sending the ACK packet...")

            packet = util.make_packet('', int(seq), int(seq))
            serverSocket.sendto(packet, address)

        expected_seq_num = (expected_seq_num + 1) % 2
        expected_ack_num = (expected_ack_num + 1) % 2

    packetNumber += 1
    print("all done for this packet!" + "\n")
serverSocket.close()
