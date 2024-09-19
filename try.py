import pydivert
import time

filter_rule = "ip and ip.SrcAddr == 141.95.98.181"

try:
    with pydivert.WinDivert(filter_rule) as w:
        print("WinDivert is capturing packets...")

        for packet in w:
            print(f"Packet from {packet.src_addr} intercepted.")

            if packet.src_addr == "141.95.98.181":
                # Simulate delay
                print(f"Delaying packet from {packet.src_addr} by 1 seconds...")
                time.sleep(1)

            # Reinject the delayed packet back into the network stack
            w.send(packet)
            print(f"Packet from {packet.src_addr} reinjected after delay.")

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("\nScript stopped. Exiting...")
