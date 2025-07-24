#!/usr/bin/env python3
"""
Check Lua syntax by analyzing structure
"""

def check_lua_syntax(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Track nesting
    stack = []
    function_count = 0
    if_count = 0
    for_count = 0
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Skip comments and empty lines
        if not stripped or stripped.startswith('--'):
            continue
        
        # Track opening structures
        if 'function' in line and '(' in line:
            function_count += 1
            stack.append(('function', i))
        
        if stripped.startswith('if ') or ' if ' in stripped:
            if_count += 1
            stack.append(('if', i))
            
        if stripped.startswith('for '):
            for_count += 1
            stack.append(('for', i))
            
        # Track pcall
        if 'pcall(function()' in line:
            stack.append(('pcall', i))
            
        # Track closing
        if stripped == 'end':
            if stack:
                structure, start_line = stack.pop()
                print(f"Line {i}: 'end' closes {structure} from line {start_line}")
            else:
                print(f"⚠️  Line {i}: Unexpected 'end' - no matching opening")
                
        if stripped == 'end)':
            if stack and stack[-1][0] == 'pcall':
                structure, start_line = stack.pop()
                print(f"Line {i}: 'end)' closes {structure} from line {start_line}")
            else:
                print(f"❌ Line {i}: 'end)' without matching pcall")
    
    print(f"\nSummary:")
    print(f"Functions: {function_count}")
    print(f"If statements: {if_count}")
    print(f"For loops: {for_count}")
    print(f"Unclosed structures: {len(stack)}")
    
    if stack:
        print("\nUnclosed structures:")
        for structure, line in stack:
            print(f"  - {structure} at line {line}")

if __name__ == "__main__":
    check_lua_syntax("lua/mcp_bridge.lua")