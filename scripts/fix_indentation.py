#!/usr/bin/env python3
"""Fix the indentation issues in the bridge file"""

with open('lua/mcp_bridge.lua', 'r') as f:
    lines = f.readlines()

# Find all elseif lines that are misaligned
for i in range(750, 3850):
    line = lines[i]
    if line.strip().startswith('elseif fname =='):
        # This should be at the same indentation level as the first if
        # Which is 24 spaces (6 levels of 4 spaces)
        lines[i] = ' ' * 24 + line.strip() + '\n'

# Write back
with open('lua/mcp_bridge.lua', 'w') as f:
    f.writelines(lines)

print("Fixed elseif indentation")