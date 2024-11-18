import socket
import logging
import sys
import time
from message import Message, MessageType

class Client:
    def __init__(self, server_host: str, server_port: int):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        try:
            self.socket.connect((self.server_host, self.server_port))
            logging.info(f"Connected to load balancer at {self.server_host}:{self.server_port}")
        except ConnectionRefusedError:
            logging.error("Failed to connect to load balancer")
            raise
            
    def send_request(self, msg_id: str, source: str, destination: str):
        message = Message(msg_id, MessageType.GET, source, destination)
        try:
            self.socket.send(message.serialize())
            logging.info(f"Sent message: {message}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            raise
            
    def close(self):
        self.socket.close()

def test_request():
    client = Client('localhost', 4000)
    
    try:
        client.connect()
        
        test_cases = [
            ("msg1", "client1", "server1"),
            ("msg2", "client1", "server2"),
            ("msg3", "client1", "server3"),
        ]
        
        for msg_id, source, dest in test_cases:
            client.send_request(msg_id, source, dest)
            time.sleep(1)
            
    except Exception as e:
        logging.error(f"Test failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_request()
    else:
        client = Client('localhost', 4000)
        try:
            client.connect()
            
            while True:
                try:
                    msg_id = input("Enter message ID: ")
                    source = input("Enter source: ")
                    dest = input("Enter destination: ")
                    client.send_request(msg_id, source, dest)
                except KeyboardInterrupt:
                    break
                except ValueError:
                    print("Invalid input format")
                    
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            client.close()