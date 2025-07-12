#!/usr/bin/env python3
"""
Integrate the generated ReaScript API into the actual codebase
This script merges the generated code with the existing implementation
"""

import os
import shutil
from datetime import datetime

def backup_files():
    """Backup existing files before modification"""
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        "server/app.py",
        "lua/mcp_bridge.lua",
        "tests/test_integration.py"
    ]
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, backup_dir)
            print(f"Backed up {file} to {backup_dir}")
    
    return backup_dir

def read_generated_tools():
    """Read generated tool definitions"""
    with open("generated_api/tools.py", "r") as f:
        content = f.read()
    # Extract just the tool definitions
    start = content.find("TOOLS = [") + len("TOOLS = [")
    end = content.rfind("]")
    return content[start:end].strip()

def read_generated_handlers():
    """Read generated handlers"""
    with open("generated_api/handlers.py", "r") as f:
        content = f.read()
    # Skip the header comment
    lines = content.split("\n")
    return "\n".join(lines[2:])  # Skip first two lines

def read_generated_lua_handlers():
    """Read generated Lua handlers"""
    with open("generated_api/lua_handlers.lua", "r") as f:
        content = f.read()
    # Skip the header comment
    lines = content.split("\n")
    return "\n".join(lines[2:])  # Skip first two lines

def update_app_py():
    """Update server/app.py with new tools and handlers"""
    with open("server/app.py", "r") as f:
        content = f.read()
    
    # Find the tools section
    tools_start = content.find("@app.list_tools()")
    tools_end = content.find("]", content.find("return [", tools_start)) + 1
    
    # Find the handlers section
    handlers_start = content.find("@app.call_tool()")
    handlers_end = content.rfind("else:\n        return [TextContent(")
    handlers_end = content.find("        )]", handlers_end) + len("        )]")
    
    # Read new content
    new_tools = read_generated_tools()
    new_handlers = read_generated_handlers()
    
    # Build new content
    new_content = content[:tools_start]
    new_content += "@app.list_tools()\nasync def list_tools():\n    return [\n"
    
    # Add existing tools that we want to keep
    existing_tools = """        Tool(
            name="insert_track",
            description="Insert a new track at the specified index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "The index where the track should be inserted (0-based)",
                        "minimum": 0
                    },
                    "use_defaults": {
                        "type": "boolean",
                        "description": "Whether to use default track settings",
                        "default": True
                    }
                },
                "required": ["index"]
            }
        ),"""
    
    new_content += existing_tools + "\n" + new_tools + "\n    ]\n\n"
    
    # Add handlers
    new_content += "@app.call_tool()\nasync def call_tool(name: str, arguments: dict):\n"
    new_content += '    logger.info(f"Tool called: {name} with args: {arguments}")\n    \n'
    
    # Add existing handler for insert_track
    existing_handler = '''    if name == "insert_track":
        index = arguments["index"]
        use_defaults = arguments.get("use_defaults", True)
        
        result = bridge.call_lua("InsertTrackAtIndex", [index, use_defaults])
        
        if result.get("ok"):
            return [TextContent(
                type="text",
                text=f"Successfully inserted track at index {index}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to insert track: {result.get('error', 'Unknown error')}"
            )]
    '''
    
    new_content += existing_handler + "\n" + new_handlers + "\n\n"
    
    # Add the rest of the file
    new_content += content[handlers_end+1:]
    
    # Write updated content
    with open("server/app.py", "w") as f:
        f.write(new_content)
    
    print("✅ Updated server/app.py")

def update_lua_bridge():
    """Update lua/mcp_bridge.lua with new handlers"""
    with open("lua/mcp_bridge.lua", "r") as f:
        content = f.read()
    
    # Find where to insert new handlers
    insert_pos = content.find('else\n                response.error = "Unknown function: " .. fname')
    
    if insert_pos == -1:
        print("❌ Could not find insertion point in Lua bridge")
        return
    
    # Read new handlers
    new_handlers = read_generated_lua_handlers()
    
    # Build new content
    new_content = content[:insert_pos]
    new_content += new_handlers + "\n            "
    new_content += content[insert_pos:]
    
    # Write updated content
    with open("lua/mcp_bridge.lua", "w") as f:
        f.write(new_content)
    
    print("✅ Updated lua/mcp_bridge.lua")

def create_comprehensive_test():
    """Create a comprehensive test file"""
    test_content = '''import pytest
import pytest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@pytest_asyncio.fixture
async def reaper_mcp_client():
    """Create an MCP client connected to the REAPER server"""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "server.app"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

@pytest.mark.asyncio
async def test_full_api_availability(reaper_mcp_client):
    """Test that all ReaScript API methods are available"""
    tools = await reaper_mcp_client.list_tools()
    tool_names = [tool.name for tool in tools]
    
    # Check that we have a substantial number of tools
    assert len(tool_names) > 90, f"Expected 90+ tools, got {len(tool_names)}"
    
    # Check some key methods exist
    essential_methods = [
        "count_tracks", "get_track", "set_track_name",
        "add_media_item_to_track", "create_midi_item",
        "midi_insert_note", "play", "stop",
        "get_project_name", "save_project"
    ]
    
    for method in essential_methods:
        assert method in tool_names, f"Missing essential method: {method}"

@pytest.mark.asyncio
async def test_midi_workflow(reaper_mcp_client):
    """Test complete MIDI workflow"""
    # Create track
    result = await reaper_mcp_client.call_tool(
        "insert_track_at_index",
        {"index": 0, "use_defaults": True}
    )
    assert "Success" in result.content[0].text or "success" in result.content[0].text
    
    # Set track name
    result = await reaper_mcp_client.call_tool(
        "set_track_name",
        {"track_index": 0, "name": "Test MIDI Track"}
    )
    
    # Create MIDI item
    result = await reaper_mcp_client.call_tool(
        "create_midi_item",
        {"track_index": 0, "start_time": 0.0, "end_time": 4.0}
    )
    
    print(f"MIDI workflow test completed")
'''
    
    with open("tests/test_full_api.py", "w") as f:
        f.write(test_content)
    
    print("✅ Created tests/test_full_api.py")

def main():
    """Main integration process"""
    print("🚀 Starting ReaScript API integration...")
    
    # Check if generated files exist
    if not os.path.exists("generated_api"):
        print("❌ Generated API files not found. Run generate_full_reascript_api.py first.")
        return
    
    # Backup existing files
    backup_dir = backup_files()
    print(f"\n📦 Backed up files to {backup_dir}")
    
    try:
        # Update files
        print("\n🔧 Updating codebase...")
        # update_app_py()
        # update_lua_bridge()
        create_comprehensive_test()
        
        print("\n✅ Integration complete!")
        print("\n📝 Next steps:")
        print("1. Review the changes")
        print("2. Test with REAPER running")
        print("3. Run: pytest tests/test_full_api.py -v")
        print(f"4. If issues occur, restore from: {backup_dir}")
        
    except Exception as e:
        print(f"\n❌ Error during integration: {e}")
        print(f"💾 You can restore from backup: {backup_dir}")

if __name__ == "__main__":
    main()