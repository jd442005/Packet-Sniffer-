import matplotlib.pyplot as plt
from collections import Counter
from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP, ICMP
import csv

traffic_data = []

# Packet handler function
def packet_handler(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = "Other"
        
        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"
        elif ICMP in packet:
            protocol = "ICMP"
        
        traffic_data.append((src_ip, dst_ip, protocol))
        print(f"Source: {src_ip} -> Destination: {dst_ip}, Protocol: {protocol}")

# Function to plot data
def plot_traffic_data():
    # Extract source and destination IPs
    src_ips = [src for src, dst, proto in traffic_data]
    dst_ips = [dst for src, dst, proto in traffic_data]
    protocols = [proto for src, dst, proto in traffic_data]

    # Count occurrences
    src_ip_counts = Counter(src_ips)
    dst_ip_counts = Counter(dst_ips)
    protocol_counts = Counter(protocols)

    # Plot source IP addresses
    plt.figure(figsize=(10, 5))
    plt.bar(src_ip_counts.keys(), src_ip_counts.values())
    plt.xlabel('Source IP Addresses')
    plt.ylabel('Number of Packets')
    plt.title('Source IP Address Traffic')
    plt.xticks(rotation=90)
    plt.show()

    # Plot destination IP addresses
    plt.figure(figsize=(10, 5))
    plt.bar(dst_ip_counts.keys(), dst_ip_counts.values())
    plt.xlabel('Destination IP Addresses')
    plt.ylabel('Number of Packets')
    plt.title('Destination IP Address Traffic')
    plt.xticks(rotation=90)
    plt.show()

    # Plot protocol distribution
    plt.figure(figsize=(10, 5))
    plt.bar(protocol_counts.keys(), protocol_counts.values())
    plt.xlabel('Protocol')
    plt.ylabel('Number of Packets')
    plt.title('Protocol Distribution')
    plt.show()

# Function to save traffic data to a CSV file
def save_traffic_data(filename="traffic_data.csv"):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Source IP', 'Destination IP', 'Protocol']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for src_ip, dst_ip, protocol in traffic_data:
            writer.writerow({'Source IP': src_ip, 'Destination IP': dst_ip, 'Protocol': protocol})
    
    print(f"Traffic data saved to {filename}")

# Function to prompt user for protocol filter
def get_protocol_filter():
    global protocol_filter
    while True:
        protocol_filter = input("Enter protocol to filter (TCP/UDP/ICMP or leave blank for all): ").strip().upper()
        if protocol_filter in ["TCP", "UDP", "ICMP", ""]:
            break
        print("Invalid input. Please enter 'TCP', 'UDP', 'ICMP', or leave blank.")

# Main function
def main():
    get_protocol_filter()  # Prompt user for protocol filter
    print("Starting packet capture. Press Ctrl+C to stop.")
    sniff(prn=packet_handler, count=100)  # Adjust count or other parameters as needed
    plot_traffic_data()
    save_traffic_data()

if __name__ == "__main__":
    main()
