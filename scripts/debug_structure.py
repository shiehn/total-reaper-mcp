#!/usr/bin/env python3
"""Debug the structure by counting opens and closes"""

with open('lua/mcp_bridge.lua', 'r') as f:
    lines = f.readlines()

# Count structure elements
opens = 0
closes = 0

for i in range(710, 3850):
    line = lines[i].strip()
    
    # Count opens
    if 'function()' in line and 'pcall' in line:
        opens += 1
        print(f"Line {i+1}: PCALL OPEN (total opens: {opens})")
    elif line == 'if file_exists(numbered_request_file) then':
        opens += 1
        print(f"Line {i+1}: IF file_exists OPEN (total opens: {opens})")
    elif line == 'if content then':
        opens += 1
        print(f"Line {i+1}: IF content OPEN (total opens: {opens})")
    elif line == 'if request and request.func and request.args then':
        opens += 1
        print(f"Line {i+1}: IF request OPEN (total opens: {opens})")
    
    # Count closes
    elif line == 'end':
        closes += 1
        print(f"Line {i+1}: END (total closes: {closes}, balance: {opens - closes})")
    elif line == 'end)':
        closes += 1
        print(f"Line {i+1}: END) for pcall (total closes: {closes}, balance: {opens - closes})")

print(f"\nFinal: Opens={opens}, Closes={closes}, Balance={opens - closes}")