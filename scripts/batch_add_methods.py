#!/usr/bin/env python3
"""
Batch add all missing methods to REAPER MCP Server
This directly updates the app.py and mcp_bridge.lua files
"""

import re
import shutil
from datetime import datetime

# Read the generated files
with open('generated_tools.txt', 'r') as f:
    tools_content = f.read()
    # Extract just the tool definitions
    tools_to_add = '\n'.join(tools_content.split('\n')[3:]).strip()

with open('generated_handlers.txt', 'r') as f:
    handlers_content = f.read()
    # Extract just the handlers
    handlers_to_add = '\n'.join(handlers_content.split('\n')[3:]).strip()

with open('generated_lua_handlers.txt', 'r') as f:
    lua_content = f.read()
    # Extract just the Lua handlers
    lua_to_add = '\n'.join(lua_content.split('\n')[3:]).strip()

# Backup files
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy('server/app.py', f'server/app.py.backup_{timestamp}')
shutil.copy('lua/mcp_bridge.lua', f'lua/mcp_bridge.lua.backup_{timestamp}')

print(f"Created backups with timestamp: {timestamp}")

# Update server/app.py
with open('server/app.py', 'r') as f:
    app_content = f.read()

# Find the position to insert tools (after the last Tool definition)
tools_pattern = r'(\s+Tool\(.+?\)\s*\))\s*\]'
tools_match = re.search(tools_pattern, app_content, re.DOTALL)

if tools_match:
    # Insert the new tools before the closing bracket
    insert_pos = tools_match.end(1)
    app_content = app_content[:insert_pos] + ',\n' + tools_to_add + app_content[insert_pos:]
    print("✓ Added tool definitions to app.py")
else:
    print("✗ Could not find tool definitions section in app.py")

# Find the position to insert handlers (before the final else)
handler_pattern = r'(\s+else:\s+return \[TextContent\(\s+type="text",\s+text=f"Unknown tool: \{name\}"\s+\)\])'
handler_match = re.search(handler_pattern, app_content)

if handler_match:
    # Insert the new handlers before the else clause
    insert_pos = handler_match.start()
    app_content = app_content[:insert_pos] + handlers_to_add + '\n' + app_content[insert_pos:]
    print("✓ Added handlers to app.py")
else:
    print("✗ Could not find handler section in app.py")

# Write updated app.py
with open('server/app.py', 'w') as f:
    f.write(app_content)

# Update lua/mcp_bridge.lua
with open('lua/mcp_bridge.lua', 'r') as f:
    lua_content_file = f.read()

# Find the position to insert Lua handlers (before the final else)
lua_pattern = r'(\s+else\s+response\.error = "Unknown function: " \.\. fname\s+end)'
lua_match = re.search(lua_pattern, lua_content_file)

if lua_match:
    # Insert the new handlers before the else clause
    insert_pos = lua_match.start()
    lua_content_file = lua_content_file[:insert_pos] + lua_to_add + '\n' + lua_content_file[insert_pos:]
    print("✓ Added Lua handlers to mcp_bridge.lua")
else:
    print("✗ Could not find Lua handler section in mcp_bridge.lua")

# Write updated mcp_bridge.lua
with open('lua/mcp_bridge.lua', 'w') as f:
    f.write(lua_content_file)

print("\n✅ All methods have been added!")
print("\nNext steps:")
print("1. Review the changes in server/app.py and lua/mcp_bridge.lua")
print("2. Test the new methods")
print("3. Update IMPLEMENTATION_STATUS.md")
print("\nBackup files created:")
print(f"  - server/app.py.backup_{timestamp}")
print(f"  - lua/mcp_bridge.lua.backup_{timestamp}")