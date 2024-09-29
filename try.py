"""
import pydivert
import time

filter_rule = "ip and ip.SrcAddr == 192.168.0.180"

try:
    with pydivert.WinDivert(filter_rule) as w:
        print("WinDivert is capturing packets...")

        for packet in w:
            print(f"Packet from {packet.src_addr} intercepted.")

            if packet.src_addr == "192.168.0.180": #141.95.98.181
                # Simulate delay
                print(f"Delaying packet from {packet.src_addr} by 1 seconds...")
                time.sleep(0.499)

            # Reinject the delayed packet back into the network stack
            w.send(packet)
            w.send(packet)
            w.send(packet)
            print(f"Packet from {packet.src_addr} reinjected after delay.")

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("\nScript stopped. Exiting...")
"""
"""
import random
import pydivert
import time

filter_rule = "ip and ip.SrcAddr == 192.168.0.180 and ip.DstAddr == 141.95.98.181"
packet_flag = False
current_packet = None
try:
    with pydivert.WinDivert(filter_rule) as w:
        print("Packet capturing started...")
        
        for packet in w:
            if packet_flag:
                time.sleep(0.5)
                w.send(current_packet)
                packet_flag = False
            # Ellenőrizzük, hogy a forrás 192.168.0.180 és a cél 141.95.98.181
            if packet.src_addr == "192.168.0.180" and packet.dst_addr == "141.95.98.181":
                # Random késleltetjük a packetet
                delay = random.uniform(0.2, 1.0)  # Random delay between 200ms to 1s
                print(f"Delaying packet from {packet.src_addr} to {packet.dst_addr} by {delay} seconds...")
                time.sleep(delay)

                # Random dobjuk el néhány packetet (pl. minden 3.-at)
                if random.randint(1, 5) == 3:  # Drop roughly every 3rd packet
                    print(f"Packet from {packet.src_addr} to {packet.dst_addr} dropped.")
                    current_packet = packet
                    packet_flag = True
                    continue

            # Reinject the packet back into the network
            w.send(packet)
            print(f"Packet from {packet.src_addr} to {packet.dst_addr} reinjected.")

except KeyboardInterrupt:
    print("\nScript stopped. Exiting...")
"""
"""
import random
import pydivert
import time

filter_rule = "ip and ip.SrcAddr == 141.95.98.181 and ip.DstAddr == 192.168.0.180" 
packet_buffer = []  # Tároljuk az elhalasztott packeteket
batch_size = 3  # Együtt küldjük el a packeteket minden 3. iteráció után

try:
    with pydivert.WinDivert(filter_rule) as w:
        print("Packet capturing started...")

        for packet in w:
            # Ellenőrizzük, hogy a forrás 192.168.0.180 és a cél 141.95.98.181
            if packet.src_addr == "141.95.98.181" and packet.dst_addr == "192.168.0.180":
                # Random késleltetés
                delay = random.uniform(0.2, 1.0)
                print(f"Delaying packet from {packet.src_addr} to {packet.dst_addr} by {delay} seconds...")
                time.sleep(delay)

                # Packet duplikálás
                if random.randint(1, 5) == 2:
                    print(f"Duplicating packet from {packet.src_addr} to {packet.dst_addr}.")
                    w.send(packet)  # Duplikált packetet azonnal visszaküldjük

                # Batch küldés
                packet_buffer.append(packet)
                if len(packet_buffer) >= batch_size:
                    print(f"Sending {batch_size} packets at once...")
                    for buffered_packet in packet_buffer:
                        w.send(buffered_packet)
                    packet_buffer = []  # Kiürítjük a buffer-t

except KeyboardInterrupt:
    print("\nScript stopped. Exiting...")
"""
"""
from scapy.all import sniff
import time

# Define the IPs you want to monitor
ip1 = "141.95.98.181"
ip2 = "192.168.0.180"

# Define a packet filter function with a timestamp
def packet_callback(packet):
    # Check if packet has an IP layer
    if packet.haslayer("IP"):
        src_ip = packet["IP"].src
        dst_ip = packet["IP"].dst

        # Check if the packet is between the two specified IPs
        if (src_ip == ip1 and dst_ip == ip2) or (src_ip == ip2 and dst_ip == ip1):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f"Time: {timestamp} | Packet: {src_ip} --> {dst_ip}")
            packet.show()  # Display packet details

# Start sniffing the network for packets
print(f"Sniffing traffic between {ip1} and {ip2}...")
sniff(filter=f"ip host {ip1} and {ip2}", prn=packet_callback)

"""
import struct

# Replace this with your actual raw data payload
raw_data = b'\x94&dZb7\x8a\x95\xda\xf5\x11\xa7\xd25\xb1S\xec`\xc3<F\x1c\x1c\x08$\x9ao\r\xd7\x0fF\x8e\xaf:\xa6\xea\x7f\xealMUd\xa2Q\x18\x84/s\x9b3\xca@\x87%XZ\xaaD\x80|\xd4t\xc1r\xf7\xbe\xda1\xc0\xae\xdc\x18\xd3\xf8@\x01\xab\xd4\x03X\xcf\xe3\x91/\x00@\xec>\x0f\xc9\x1f\xa8\x91\x10?\xedx\x92\xfaX\xf89\xec\xbd\xce4\x05\xeb\x92^I\x81\xeb\xe3j\xa0\x01w\xcc\x0b\x08\x9f0\r [\x8b\x9cS\xec\x8d\x03\x95\xb5'

def decode_raw_data(data):
    # Decode based on assumed structure
    action_type = struct.unpack('B', data[0:1])[0]
    item_id = struct.unpack('I', data[1:5])[0]
    quantity = struct.unpack('H', data[5:7])[0]
    success_flag = struct.unpack('B', data[7:8])[0]
    payload_data = data[8:]

    # Print results
    print(f"Action Type: {action_type}")
    print(f"Item ID: {item_id}")
    print(f"Quantity: {quantity}")
    print(f"Success Flag: {success_flag}")
    print(f"Payload Data: {payload_data.hex()}")

# Decode the raw data
decode_raw_data(raw_data)