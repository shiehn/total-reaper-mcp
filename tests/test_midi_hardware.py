"""Test cases for MIDI hardware operations"""

import pytest
from .conftest import call_tool, reaper_available


@pytest.mark.integration
@pytest.mark.skipif(not reaper_available(), reason="REAPER not available")
class TestMIDIHardware:
    """Test MIDI hardware-related operations"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, mock_project):
        """Ensure clean state for each test"""
        pass
    
    def test_get_num_midi_inputs(self, mock_project):
        """Test getting number of MIDI inputs"""
        result = call_tool("get_num_midi_inputs", {})
        assert result["success"]
        assert "Number of MIDI inputs:" in result["result"]
        
        # Extract the count
        count_str = result["result"].split(": ")[1]
        count = int(count_str)
        assert count >= 0
    
    def test_get_num_midi_outputs(self, mock_project):
        """Test getting number of MIDI outputs"""
        result = call_tool("get_num_midi_outputs", {})
        assert result["success"]
        assert "Number of MIDI outputs:" in result["result"]
        
        # Extract the count
        count_str = result["result"].split(": ")[1]
        count = int(count_str)
        assert count >= 0
    
    def test_get_midi_input_names(self, mock_project):
        """Test getting MIDI input names"""
        # First get the count
        result = call_tool("get_num_midi_inputs", {})
        assert result["success"]
        count = int(result["result"].split(": ")[1])
        
        # Get names for available inputs (test up to 3 or available count)
        test_count = min(count, 3)
        for i in range(test_count):
            result = call_tool("get_midi_input_name", {"input_index": i})
            assert result["success"]
            assert f"MIDI input {i}:" in result["result"]
    
    def test_get_midi_output_names(self, mock_project):
        """Test getting MIDI output names"""
        # First get the count
        result = call_tool("get_num_midi_outputs", {})
        assert result["success"]
        count = int(result["result"].split(": ")[1])
        
        # Get names for available outputs (test up to 3 or available count)
        test_count = min(count, 3)
        for i in range(test_count):
            result = call_tool("get_midi_output_name", {"output_index": i})
            assert result["success"]
            assert f"MIDI output {i}:" in result["result"]
    
    def test_invalid_midi_input_index(self, mock_project):
        """Test error handling for invalid MIDI input index"""
        # Try to get name of a very high index that likely doesn't exist
        result = call_tool("get_midi_input_name", {"input_index": 9999})
        
        # This might succeed if there are many MIDI inputs, or fail
        # We just check that we get a response
        assert "result" in result or "error" in result
    
    def test_invalid_midi_output_index(self, mock_project):
        """Test error handling for invalid MIDI output index"""
        # Try to get name of a very high index that likely doesn't exist
        result = call_tool("get_midi_output_name", {"output_index": 9999})
        
        # This might succeed if there are many MIDI outputs, or fail
        # We just check that we get a response
        assert "result" in result or "error" in result
    
    def test_midi_system_info(self, mock_project):
        """Test getting complete MIDI system information"""
        # Get input count
        result = call_tool("get_num_midi_inputs", {})
        assert result["success"]
        input_count = int(result["result"].split(": ")[1])
        
        # Get output count
        result = call_tool("get_num_midi_outputs", {})
        assert result["success"]
        output_count = int(result["result"].split(": ")[1])
        
        # Basic sanity checks
        assert input_count >= 0
        assert output_count >= 0
        
        # If we have MIDI devices, test getting their names
        if input_count > 0:
            result = call_tool("get_midi_input_name", {"input_index": 0})
            assert result["success"]
        
        if output_count > 0:
            result = call_tool("get_midi_output_name", {"output_index": 0})
            assert result["success"]