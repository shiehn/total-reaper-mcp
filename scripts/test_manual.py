#!/usr/bin/env python3
"""
Manual test script to verify REAPER communication without MCP
"""
import socket
import json
import time

def test_reaper_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)
    sock.bind(('127.0.0.1', 9001))
    
    tests = [
        ("GetAppVersion", []),
        ("CountTracks", [0]),
        ("InsertTrackAtIndex", [0, True]),
        ("CountTracks", [0]),
    ]
    
    for fname, args in tests:
        message = json.dumps({'call': fname, 'args': args})
        print(f"\nSending: {message}")
        
        try:
            sock.sendto(message.encode(), ('127.0.0.1', 9000))
            data, addr = sock.recvfrom(65536)
            response = json.loads(data.decode())
            print(f"Received: {response}")
        except socket.timeout:
            print("Timeout - is REAPER running with mcp_bridge.lua?")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    print("Testing REAPER connection...")
    print("Make sure REAPER is running with mcp_bridge.lua loaded!")
    test_reaper_connection()