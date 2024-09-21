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
import random
import pydivert
import time

filter_rule = "ip and ip.SrcAddr == 192.168.0.180 and ip.DstAddr == 141.95.98.181"
packet_buffer = []  # Tároljuk az elhalasztott packeteket
batch_size = 3  # Együtt küldjük el a packeteket minden 3. iteráció után

try:
    with pydivert.WinDivert(filter_rule) as w:
        print("Packet capturing started...")

        for packet in w:
            # Ellenőrizzük, hogy a forrás 192.168.0.180 és a cél 141.95.98.181
            if packet.src_addr == "192.168.0.180" and packet.dst_addr == "141.95.98.181":
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
