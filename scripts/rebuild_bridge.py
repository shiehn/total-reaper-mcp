#!/usr/bin/env python3
"""
Rebuild the bridge file properly by taking DSL functions and the v2 handlers
"""

print("Rebuilding bridge file...")

# Read the DSL functions from v3
with open('lua/mcp_bridge.lua', 'r') as f:
    v3_lines = f.readlines()

# Extract DSL functions (lines 194-706)
dsl_functions = []
for i in range(193, 706):
    dsl_functions.append(v3_lines[i])

# Read the original v2 file
with open('lua/archive/mcp_bridge_file_v2.lua', 'r') as f:
    v2_content = f.read()

# Find where to insert DSL functions in v2
# They should go before "-- Main processing function"
insert_pos = v2_content.find("-- Main processing function")

# Build the new file
new_content = (
    v2_content[:insert_pos] +
    "\n-- ============================================================================\n" +
    "-- DSL HELPER FUNCTIONS\n" +
    "-- ============================================================================\n" +
    ''.join(dsl_functions) +
    "\n" +
    v2_content[insert_pos:]
)

# Now we need to modify the handler section to check DSL functions first
# Find the line "-- Handle all API functions"
handler_start = new_content.find("-- Handle all API functions")
handler_line_start = new_content.rfind('\n', 0, handler_start) + 1

# Find where the first function handler starts
first_handler = new_content.find("if fname == \"InsertTrackAtIndex\"", handler_start)

# Insert DSL check before the first handler
dsl_check = """                    if DSL_FUNCTIONS[fname] then
                        local result = DSL_FUNCTIONS[fname](table.unpack(args))
                        -- Copy all fields from result to response
                        for k, v in pairs(result) do
                            response[k] = v
                        end
                    
                    else"""

# Change the first "if" to "elseif"
new_content = (
    new_content[:first_handler] +
    dsl_check + new_content[first_handler:].replace("if fname ==", "elseif fname ==", 1)
)

# Write the result
with open('lua/mcp_bridge.lua', 'w') as f:
    f.write(new_content)

print("Bridge rebuilt successfully!")
print("The file now has the correct structure with DSL functions integrated.")