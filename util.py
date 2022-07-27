# Variable declaration
seqNumber = 1
global packetNumber
packetNumber = 0

"""
create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

Args:
  packet_wo_checksum: the packet byte data (including headers except for checksum field)

Returns:
  the checksum in bytes
"""
def create_checksum(packet_wo_checksum):
    data = [packet_wo_checksum[i:i + 2] for i in range(0, len(packet_wo_checksum), 2)]

    checksum = bin(0)
    for i in range(0, len(data)):
        a = bin(int.from_bytes(data[i], 'big'))
        checksum = bin(int(checksum, 2) + int(a, 2))

    k = 16

    # overflow of bits that is if bit count is greater than 16
    if len(checksum) > k:
        x = len(checksum) - k
        checksum = bin(int(checksum[0:x], 2) + int(checksum[x:], 2))[2:]

    # IF bit count is less than 16
    if len(checksum) < k:
        checksum = '0' * (k - len(checksum)) + checksum

    return checksum


"""
verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

Args:
  packet: the whole (including original checksum) packet byte data

Returns:
  True if the packet checksum is the same as specified in the checksum field
  False otherwise
"""
# this is one approach to verify checksum
def verify_checksum(packet):
    L = [packet[i:i + 1] for i in range(len(packet))]

    senderChecksum = b''.join(L[8:10])

    withoutChecksum = b''.join(L[0:8] + L[10:])

    receiverChecksum = create_checksum(withoutChecksum)
    receiverChecksum = complementData(receiverChecksum)

    firstByte = int(receiverChecksum[0:8], 2)
    secondByte = int(receiverChecksum[8:], 2)

    receiverChecksum = bytes([firstByte]) + bytes([secondByte])
    return senderChecksum == receiverChecksum

# this is second approach to verify checksum
def verify_checksum(packet):
    checkSum = create_checksum(packet)
    # print("verify_checksum:",checkSum)

    return True == all(c in '1' for c in checkSum)


"""
calculate the length of the current packet

Args:
    data_str: packet data
    ack_num: ack_num bit to add to the packet length
    seq_num: seq_num bit to add to the packet length

Returns:
    The length in 16 bits. The first 14 bits are used to save the length (header + data) of the current packet, 
    the 15th bit is used to indicate if this packet is an ACK packet, and the 16th bit saves the sequence number 
    of this packet.
"""
def make_packet(data_str, ack_num, seq_num):
    header_length = 12
    partialHeader = 'COMPNETW'

    packetLength = calculate_packet_length(data_str, ack_num, seq_num)

    # packet = header+data = "partialHeader"+length+data
    packet = dataToBytes(partialHeader) + packetLength + dataToBytes(data_str)

    checksum = create_checksum(packet)

    compData = complementData(checksum)

    firstByte = int(compData[0:8], 2)
    secondByte = int(compData[8:], 2)

    checksum = bytes([firstByte]) + bytes([secondByte])

    complete_packet = bytes(partialHeader, 'utf-8') + checksum + packetLength + bytes(data_str, 'utf-8')

    return complete_packet

"""
This method will return the packet length for the data.
"""
def calculate_packet_length(data_str, ack_num, seq_num):
    partialHeader = 'COMPNETW'
    partialHeaderLength = 12

    dataLength = byteDataLength(data_str)

    headerAndDataLength = partialHeaderLength + len(data_str)

    # Adding the acknowledgement bit to the headerAndDataLength
    modifiedLength = leftShif(headerAndDataLength, ack_num)

    # Adding the sequence bit to the headerAndDataLength
    modifiedLength = leftShif(modifiedLength, seq_num)

    modifiedLengthBits = format(modifiedLength, '016b')

    firstByte = int(modifiedLengthBits[0:8], 2)
    secondByte = int(modifiedLengthBits[8:], 2)

    return bytes([firstByte]) + bytes([secondByte])


# This method takes data as input and return's the length
def byteDataLength(data):
    return len(bytes(data, 'utf-8'))


# This method takes text as input and returns the byte data
def dataToBytes(data):
    return bytes(data, 'utf-8')


"""
Args: 
   number : integer for which left shift to be done
   flag : either 0 or 1 integer object
Returns:
   left-shift operated 16 bit number
"""
def leftShif(number, flag):
    return ((number << 1) + flag)


# This method returns the sequence number that is to be sent
def getSequenceNumber():
    global seqNumber
    if seqNumber == 0:
        seqNumber = 1
    elif seqNumber == 1:
        seqNumber = 0
    return seqNumber


# This method outputs packet number
def getPacketNumber():
    global packetNumber
    packetNumber = packetNumber + 1
    return packetNumber


# This method takes input as string and inverts  1's to 0's and  0's to 1's  and returns the inverted string as output
def complementData(s):
    Checksum = ''
    for i in s:
        if i == '1':
            Checksum += '0'
        else:
            Checksum += '1'
    return Checksum
