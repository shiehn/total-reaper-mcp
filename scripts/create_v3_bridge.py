#!/usr/bin/env python3
"""
Script to create the v3 bridge file by combining DSL functions with v2 handlers
"""

import re

# Read the partial v3 file
with open('lua/mcp_bridge_file_v3_with_dsl.lua', 'r') as f:
    v3_content = f.read()

# Read the v2 file
with open('lua/mcp_bridge_file_v2.lua', 'r') as f:
    v2_content = f.read()

# Find the handlers section in v2 (from "if fname ==" to the generic handler)
# We need everything from the first handler to the end of the generic handler
handlers_match = re.search(
    r'(if fname == "InsertTrackAtIndex".*?else\s+-- Try generic function call.*?end\s+end)', 
    v2_content, 
    re.DOTALL
)

if not handlers_match:
    print("Could not find handlers section in v2 file!")
    exit(1)

handlers_section = handlers_match.group(1)

# Find where to insert in v3 (replace the placeholder comment)
v3_updated = v3_content.replace(
    """elseif fname == "CountTracks" then
                            local count = reaper.CountTracks(0)
                            response.ok = true
                            response.ret = count
                        
                        -- [REST OF THE ORIGINAL BRIDGE FILE CONTINUES HERE]
                        -- [Due to length, I'll create a note that the rest should be copied from v2]
                        else
                            response.error = "Unknown function: " .. fname
                        end""",
    handlers_section
)

# Write the complete v3 file
with open('lua/mcp_bridge_file_v3_with_dsl.lua', 'w') as f:
    f.write(v3_updated)

print("Created complete v3 bridge file with DSL functions!")
print("The file is ready at: lua/mcp_bridge_file_v3_with_dsl.lua")