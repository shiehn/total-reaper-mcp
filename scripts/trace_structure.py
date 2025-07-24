#!/usr/bin/env python3
"""Trace the structure around the problem area"""

with open('lua/mcp_bridge.lua', 'r') as f:
    lines = f.readlines()

# Focus on lines 710-750 and 3830-3850
print("=== Structure from line 710-750 ===")
indent = 0
for i in range(709, 750):
    line = lines[i].rstrip()
    
    # Detect dedent before printing
    if line.strip() == 'end' or line.strip() == 'end)':
        indent -= 1
    
    if line.strip():  # Skip empty lines
        print(f"{i+1:4d}: {'  ' * indent}{line.strip()}")
    
    # Detect indent after printing
    if 'then' in line and not line.strip().startswith('--'):
        indent += 1
    elif 'function' in line and not line.strip().startswith('--'):
        indent += 1

print("\n=== Structure from line 3830-3850 ===")
# Reset indent and try to figure it out from context
indent = 6  # Guessing based on nesting level
for i in range(3829, 3850):
    line = lines[i].rstrip()
    
    # Detect dedent before printing
    if line.strip() == 'end' or line.strip() == 'end)':
        indent -= 1
    
    if line.strip():  # Skip empty lines
        print(f"{i+1:4d}: {'  ' * indent}{line.strip()}")
    
    # Don't change indent after 'end'