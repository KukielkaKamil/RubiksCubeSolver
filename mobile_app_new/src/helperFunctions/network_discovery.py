import socket
import json
import threading
import time

class ServerDiscovery:
    DISCOVERY_PORT = 5001  # Port for UDP discovery
    BROADCAST_IP = '255.255.255.255'
    
    def __init__(self, http_port=5000):
        self.http_port = http_port
        self.server_ip = None
        self.discovery_running = False
        
    def start_discovery_server(self):
        """Starts UDP server for discovery (run on API server)"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.DISCOVERY_PORT))
        
        while True:
            data, addr = sock.recvfrom(1024)
            if data == b'DISCOVER_RUBIKS_SERVER':
                response = json.dumps({
                    'service': 'rubiks_server',
                    'http_port': self.http_port
                }).encode()
                sock.sendto(response, addr)

    def discover_server(self, timeout=5):
        """Discovers server IP using UDP broadcast (run on client)"""
        self.discovery_running = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1)
        
        start_time = time.time()
        
        while time.time() - start_time < timeout and self.discovery_running:
            try:
                # Broadcast discovery message
                sock.sendto(b'DISCOVER_RUBIKS_SERVER', 
                          (self.BROADCAST_IP, self.DISCOVERY_PORT))
                
                # Wait for response
                data, addr = sock.recvfrom(1024)
                response = json.loads(data.decode())
                
                if response.get('service') == 'rubiks_server':
                    self.server_ip = addr[0]
                    return f'http://{addr[0]}:{response["http_port"]}'
                    
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Discovery error: {e}")
                
        return None

    def stop_discovery(self):
        """Stops the discovery process"""
        self.discovery_running = False