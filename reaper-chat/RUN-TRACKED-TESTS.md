# Running Enhanced NLP Tests with Conversation Tracking

## Overview
The enhanced NLP test framework combines:
- Natural language understanding evaluation
- Actual REAPER command execution via MCP
- Response quality assessment
- Conversation tracking for continuous improvement

## Prerequisites
1. REAPER must be running
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```
3. Ensure MCP server path is correct:
   ```bash
   export VITE_MCP_SERVER_PATH=/Users/stevehiehn/total-reaper-mcp
   ```

## Running the Tests

### Basic Test Run
```bash
# From the reaper-chat directory
node test-nlp-with-tracking.js
```

### What the Tests Do
1. Start the MCP server
2. For each test case:
   - Send natural language input to LLM
   - Execute selected MCP tools in REAPER
   - Evaluate response quality
   - Track conversation for analysis
3. Generate actionable improvement reports

### Understanding the Output

#### Console Output
- Real-time test progress
- Tool selections and execution results
- Quality scores (0-10 scale)
- Issue identification

#### Tracking Reports
Check the `conversation-tracking/` directory for:
- `session-*.json` - Raw conversation data
- `report-*.md` - Detailed analysis reports

### Report Contents
1. **Summary Statistics**
   - Success rate
   - Average quality score
   - Total conversations

2. **Failure Patterns**
   - Common failure types
   - Example queries that failed
   - Suggested improvements

3. **Actionable Improvements**
   - Specific changes to make
   - Impact assessment
   - Priority ordering

4. **Conversations Needing Review**
   - Low-scoring interactions
   - Detailed analysis of issues

## Using Results for Improvement

### 1. Review Failure Patterns
Look for patterns in the report:
```
=== TOP FAILURE PATTERNS ===
1. information_request-none (5 failures, avg score: 4.2)
   Example failures:
   - "what tracks are playing?"
     Issues: no_tool_called, missing_concrete_info
```

### 2. Implement Improvements
Based on suggestions:
```
=== ACTIONABLE IMPROVEMENTS ===
1. Add tool mapping for information_request queries
   Problem: 5 information_request queries didn't trigger any tool
   Solution: Update system prompt to better handle these query types
```

### 3. Track Progress
Compare sessions over time:
```
=== PROGRESS COMPARISON ===
Success Rate: 61.5% → 85.2%
Average Score: 6.8 → 8.4
```

## Continuous Improvement Workflow

1. **Run Tests Regularly**
   ```bash
   # Add to your testing routine
   npm run test:nlp-tracked
   ```

2. **Review Reports**
   - Check `conversation-tracking/` after each run
   - Focus on high-impact improvements

3. **Update System**
   - Modify system prompts
   - Enhance tool descriptions
   - Fix identified issues

4. **Measure Progress**
   - Compare session reports
   - Track success rate trends
   - Monitor quality scores

## Troubleshooting

### MCP Server Won't Start
- Ensure Python environment is activated
- Check server path is correct
- Look for port conflicts

### No Tool Execution
- Verify REAPER is running
- Check MCP connection in REAPER console
- Review tool availability

### Low Quality Scores
- Review specific failure examples
- Check if tools return expected data
- Verify response generation logic

## Next Steps
After running tests and reviewing reports:
1. Prioritize high-impact improvements
2. Update system prompts or tool descriptions
3. Re-run tests to verify improvements
4. Commit successful changes