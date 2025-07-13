#!/usr/bin/env python3
"""
Script to help migrate from legacy MCP pattern to modern @mcp.tool() pattern
This analyzes the existing implementation and generates modern pattern code
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def extract_tool_definitions(file_path: Path) -> List[Dict]:
    """Extract tool definitions from @app.list_tools()"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the list_tools function
    list_tools_match = re.search(r'@app\.list_tools\(\)\s*async def list_tools\(\):\s*return \[(.*?)\]', 
                                content, re.DOTALL)
    if not list_tools_match:
        return []
    
    tools_text = list_tools_match.group(1)
    
    # Extract individual Tool definitions
    tool_pattern = r'Tool\(\s*name="([^"]+)",\s*description="([^"]+)",\s*inputSchema=(\{[^}]+\})\s*\)'
    tools = []
    
    for match in re.finditer(tool_pattern, tools_text, re.DOTALL):
        name = match.group(1)
        description = match.group(2)
        schema_text = match.group(3)
        
        # Try to parse the schema
        try:
            # Simple JSON-like parsing (would need more robust parsing for production)
            schema = eval(schema_text)  # Note: eval is dangerous, only use on trusted code
        except:
            schema = {"type": "object", "properties": {}, "required": []}
        
        tools.append({
            "name": name,
            "description": description,
            "schema": schema
        })
    
    return tools

def extract_tool_implementations(file_path: Path) -> Dict[str, str]:
    """Extract tool implementations from @app.call_tool()"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the call_tool function
    call_tool_match = re.search(r'@app\.call_tool\(\)\s*async def call_tool\(name: str, arguments: dict\):(.*?)(?=async def|\Z)', 
                               content, re.DOTALL)
    if not call_tool_match:
        return {}
    
    implementations = {}
    call_tool_body = call_tool_match.group(1)
    
    # Extract individual tool implementations
    impl_pattern = r'(?:el)?if name == "([^"]+)":\s*(.*?)(?=(?:el)?if name ==|else:|$)'
    
    for match in re.finditer(impl_pattern, call_tool_body, re.DOTALL):
        name = match.group(1)
        implementation = match.group(2).strip()
        implementations[name] = implementation
    
    return implementations

def schema_to_parameters(schema: Dict) -> Tuple[List[str], List[str]]:
    """Convert JSON schema to function parameters"""
    params = []
    param_docs = []
    
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    
    for prop_name, prop_schema in properties.items():
        param_type = "Any"
        if prop_schema.get("type") == "integer":
            param_type = "int"
        elif prop_schema.get("type") == "number":
            param_type = "float"
        elif prop_schema.get("type") == "boolean":
            param_type = "bool"
        elif prop_schema.get("type") == "string":
            param_type = "str"
        elif prop_schema.get("type") == "array":
            param_type = "List[Any]"
        
        default = prop_schema.get("default")
        if prop_name in required:
            params.append(f"{prop_name}: {param_type}")
        else:
            if default is not None:
                params.append(f"{prop_name}: {param_type} = {repr(default)}")
            else:
                params.append(f"{prop_name}: Optional[{param_type}] = None")
        
        desc = prop_schema.get("description", "")
        param_docs.append(f"        {prop_name}: {desc}")
    
    return params, param_docs

def convert_implementation(impl: str, tool_name: str) -> str:
    """Convert implementation from if/else pattern to direct function"""
    # Remove argument extraction (we'll have real parameters)
    impl = re.sub(r'(\w+) = arguments\["(\w+)"\]', '', impl)
    impl = re.sub(r'(\w+) = arguments\.get\("(\w+)"(?:, [^)]+)?\)', '', impl)
    
    # Convert return statements
    impl = re.sub(r'return \[TextContent\(\s*type="text",\s*text=([^)]+)\)\]', 
                  r'return \1', impl)
    
    # Convert error returns to exceptions
    impl = re.sub(r'return \[TextContent\(\s*type="text",\s*text=f?"Failed[^"]*"\)\]',
                  r'raise Exception("Failed")', impl)
    
    return impl.strip()

def generate_modern_tool(tool_def: Dict, implementation: str) -> str:
    """Generate modern @mcp.tool() function"""
    name = tool_def["name"]
    description = tool_def["description"]
    schema = tool_def["schema"]
    
    params, param_docs = schema_to_parameters(schema)
    param_str = ", ".join(params)
    param_docs_str = "\n".join(param_docs) if param_docs else "        None"
    
    # Clean up implementation
    impl_lines = convert_implementation(implementation, name).split('\n')
    impl_str = "\n    ".join(impl_lines)
    
    return f'''@mcp.tool()
async def {name}({param_str}) -> str:
    """{description}
    
    Args:
{param_docs_str}
        
    Returns:
        Success or error message
    """
    {impl_str}
'''

def analyze_legacy_file(file_path: Path) -> None:
    """Analyze legacy file and show migration examples"""
    print(f"Analyzing {file_path}...")
    
    tools = extract_tool_definitions(file_path)
    implementations = extract_tool_implementations(file_path)
    
    print(f"\nFound {len(tools)} tool definitions")
    print(f"Found {len(implementations)} tool implementations")
    
    # Show examples of conversion
    print("\n" + "="*80)
    print("MIGRATION EXAMPLES")
    print("="*80)
    
    # Convert first 3 tools as examples
    for i, tool in enumerate(tools[:3]):
        if tool["name"] in implementations:
            print(f"\n### Tool: {tool['name']} ###")
            print("\nModern pattern:")
            print("-"*40)
            modern_code = generate_modern_tool(tool, implementations[tool["name"]])
            print(modern_code)

def main():
    """Main entry point"""
    legacy_file = Path("server/app_file_bridge_full.py")
    
    if not legacy_file.exists():
        print(f"Error: {legacy_file} not found")
        return
    
    analyze_legacy_file(legacy_file)
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Create modular structure:")
    print("   server/tools/tracks.py")
    print("   server/tools/midi.py")
    print("   server/tools/fx.py")
    print("   etc.")
    print("\n2. Move related tools to their modules")
    print("\n3. Update imports in main server file")
    print("\n4. Test each module independently")

if __name__ == "__main__":
    main()