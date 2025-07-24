const { ConversationTracker } = require('./conversation-tracker');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * Enhanced NLP Test Framework with Conversation Tracking
 * 
 * This framework combines:
 * 1. Natural language input testing
 * 2. Actual REAPER command execution via MCP
 * 3. Response quality evaluation
 * 4. Conversation tracking for continuous improvement
 */

class TrackedNLPTester {
  constructor() {
    this.tracker = new ConversationTracker('nlp-execution-tests');
    this.mcpProcess = null;
    this.chatProcess = null;
    this.apiKey = process.env.OPENAI_API_KEY;
    this.mcpServerPath = process.env.VITE_MCP_SERVER_PATH || '/Users/stevehiehn/total-reaper-mcp';
  }

  /**
   * Start the MCP server
   */
  async startMCPServer() {
    console.log('Starting MCP server...');
    
    return new Promise((resolve, reject) => {
      this.mcpProcess = spawn('python', [
        '-m', 'server.app',
        '--transport', 'stdio'
      ], {
        cwd: this.mcpServerPath,
        env: { ...process.env, PYTHONPATH: this.mcpServerPath }
      });

      this.mcpProcess.stdout.on('data', (data) => {
        const output = data.toString();
        if (output.includes('Server started') || output.includes('initialize')) {
          console.log('MCP server ready');
          resolve();
        }
      });

      this.mcpProcess.stderr.on('data', (data) => {
        console.error('MCP stderr:', data.toString());
      });

      this.mcpProcess.on('error', (error) => {
        console.error('Failed to start MCP server:', error);
        reject(error);
      });

      // Give it time to start
      setTimeout(() => resolve(), 3000);
    });
  }

  /**
   * Start the Reaper Chat app
   */
  async startReaperChat() {
    console.log('Starting Reaper Chat...');
    
    return new Promise((resolve, reject) => {
      this.chatProcess = spawn('npm', ['start'], {
        cwd: path.join(__dirname, '..'),
        env: { 
          ...process.env,
          NODE_ENV: 'test',
          ELECTRON_DISABLE_SECURITY_WARNINGS: 'true'
        }
      });

      this.chatProcess.stdout.on('data', (data) => {
        const output = data.toString();
        if (output.includes('main window created') || output.includes('webpack compiled')) {
          console.log('Reaper Chat ready');
          resolve();
        }
      });

      this.chatProcess.stderr.on('data', (data) => {
        // Log but don't fail on stderr (webpack warnings are common)
        console.log('Chat stderr:', data.toString());
      });

      this.chatProcess.on('error', (error) => {
        console.error('Failed to start Reaper Chat:', error);
        reject(error);
      });

      // Give it time to start
      setTimeout(() => resolve(), 10000);
    });
  }

  /**
   * Simulate a full conversation through the system
   */
  async testConversation(userInput, expectedIntent) {
    console.log(`\nTesting: "${userInput}"`);
    console.log(`Expected: ${expectedIntent}`);

    const conversationData = {
      userInput,
      expectedIntent,
      timestamp: new Date().toISOString()
    };

    try {
      // Get system prompt and tool definitions
      const systemPrompt = this.getSystemPrompt();
      const tools = await this.getAvailableTools();

      // Step 1: Get LLM tool selection
      const llmResponse = await this.getLLMResponse(userInput, systemPrompt, tools);
      conversationData.llmResponse = llmResponse;

      // Step 2: Execute tools if selected
      let toolResults = [];
      if (llmResponse.tool_calls && llmResponse.tool_calls.length > 0) {
        for (const toolCall of llmResponse.tool_calls) {
          console.log(`  Tool called: ${toolCall.function.name}`);
          
          try {
            const args = JSON.parse(toolCall.function.arguments);
            const result = await this.executeMCPTool(toolCall.function.name, args);
            
            toolResults.push({
              tool: toolCall.function.name,
              args: args,
              result: result,
              success: true
            });

            console.log(`  Result: ${JSON.stringify(result).substring(0, 100)}...`);
          } catch (error) {
            console.error(`  Tool failed: ${error.message}`);
            toolResults.push({
              tool: toolCall.function.name,
              error: error.message,
              success: false
            });
          }
        }
      }
      conversationData.toolResults = toolResults;

      // Step 3: Get final response
      let finalResponse = llmResponse.content;
      if (toolResults.length > 0 && !finalResponse) {
        // Get a follow-up response based on tool results
        finalResponse = await this.getLLMFollowUp(userInput, toolResults);
      }
      conversationData.finalResponse = finalResponse;

      console.log(`  Response: ${finalResponse?.substring(0, 150)}...`);

      // Step 4: Evaluate quality
      const evaluation = await this.evaluateQuality(
        userInput,
        expectedIntent,
        toolResults,
        finalResponse
      );
      conversationData.evaluation = evaluation;

      const avgScore = (
        evaluation.correctness +
        evaluation.completeness +
        evaluation.helpfulness +
        evaluation.clarity
      ) / 4;

      conversationData.avgScore = avgScore;
      conversationData.success = avgScore >= 7;

      console.log(`  Quality score: ${avgScore.toFixed(1)}/10`);
      if (evaluation.issues && evaluation.issues.length > 0) {
        console.log(`  Issues: ${evaluation.issues.join(', ')}`);
      }

      // Track the conversation
      this.tracker.trackConversation(conversationData);

      return conversationData;

    } catch (error) {
      console.error(`Test error: ${error.message}`);
      conversationData.error = error.message;
      conversationData.success = false;
      conversationData.avgScore = 0;
      
      this.tracker.trackConversation(conversationData);
      return conversationData;
    }
  }

  /**
   * Get LLM response with tools
   */
  async getLLMResponse(userInput, systemPrompt, tools) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: 'gpt-4-turbo-preview',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userInput }
        ],
        tools: tools,
        tool_choice: 'auto',
        temperature: 0.1
      })
    });

    const data = await response.json();
    if (data.error) {
      throw new Error(data.error.message);
    }

    return data.choices[0].message;
  }

  /**
   * Get follow-up response after tool execution
   */
  async getLLMFollowUp(userInput, toolResults) {
    const messages = [
      { role: 'user', content: userInput }
    ];

    // Add tool results
    toolResults.forEach(tr => {
      const content = tr.success 
        ? `Tool ${tr.tool} executed successfully: ${JSON.stringify(tr.result)}`
        : `Tool ${tr.tool} failed: ${tr.error}`;
      
      messages.push({
        role: 'assistant',
        content: content
      });
    });

    messages.push({
      role: 'user',
      content: 'Based on these results, provide a clear, user-friendly response.'
    });

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: 'gpt-4-turbo-preview',
        messages: messages,
        temperature: 0.3
      })
    });

    const data = await response.json();
    return data.choices[0].message.content;
  }

  /**
   * Execute MCP tool
   */
  async executeMCPTool(toolName, args) {
    return new Promise((resolve, reject) => {
      const request = {
        jsonrpc: '2.0',
        method: 'tools/call',
        params: {
          name: toolName,
          arguments: args
        },
        id: Date.now()
      };

      this.mcpProcess.stdin.write(JSON.stringify(request) + '\n');

      const responseHandler = (data) => {
        const lines = data.toString().split('\n');
        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const response = JSON.parse(line);
            if (response.id === request.id) {
              this.mcpProcess.stdout.removeListener('data', responseHandler);
              if (response.error) {
                reject(new Error(response.error.message));
              } else {
                resolve(response.result);
              }
            }
          } catch (e) {
            // Not JSON, ignore
          }
        }
      };

      this.mcpProcess.stdout.on('data', responseHandler);

      // Timeout
      setTimeout(() => {
        this.mcpProcess.stdout.removeListener('data', responseHandler);
        reject(new Error('MCP tool call timeout'));
      }, 5000);
    });
  }

  /**
   * Evaluate conversation quality
   */
  async evaluateQuality(userInput, expectedIntent, toolResults, finalResponse) {
    const evaluationPrompt = `
Evaluate this REAPER assistant conversation:

User asked: "${userInput}"
Expected intent: ${expectedIntent}
Tools executed: ${toolResults.map(tr => `${tr.tool} (${tr.success ? 'success' : 'failed'})`).join(', ') || 'none'}
Assistant response: "${finalResponse || 'No response'}"

Rate on a 0-10 scale:
1. Correctness: Did it understand and execute the right action?
2. Completeness: Was all necessary information provided?
3. Helpfulness: Does this help the user achieve their goal?
4. Clarity: Is the response clear and easy to understand?

Also identify:
- Issues (if any)
- Improvements needed (if any)

Respond with JSON only.`;

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: 'gpt-4-turbo-preview',
        messages: [
          { 
            role: 'system', 
            content: 'You are evaluating a DAW assistant conversation. Respond with valid JSON only.' 
          },
          { role: 'user', content: evaluationPrompt }
        ],
        temperature: 0.1
      })
    });

    const data = await response.json();
    try {
      const content = data.choices[0].message.content;
      const jsonStr = content.replace(/```json\n?/g, '').replace(/```\n?/g, '');
      return JSON.parse(jsonStr);
    } catch (e) {
      return {
        correctness: 0,
        completeness: 0,
        helpfulness: 0,
        clarity: 0,
        issues: ['Failed to evaluate'],
        improvements: ['Evaluation error']
      };
    }
  }

  /**
   * Get system prompt
   */
  getSystemPrompt() {
    return fs.readFileSync(
      path.join(__dirname, 'src/renderer/pages/ChatPage.tsx'),
      'utf8'
    ).match(/const systemPrompt = `([^`]+)`/)[1];
  }

  /**
   * Get available tools (simplified for testing)
   */
  async getAvailableTools() {
    // In production, this would query the MCP server
    // For testing, we'll use a subset of tools
    const toolDefs = JSON.parse(
      fs.readFileSync(path.join(__dirname, 'improved-tool-descriptions.json'), 'utf8')
    );

    return Object.entries(toolDefs.tool_descriptions).slice(0, 10).map(([name, info]) => ({
      type: 'function',
      function: {
        name: name,
        description: info.improved,
        parameters: {
          type: 'object',
          properties: this.getToolParams(name)
        }
      }
    }));
  }

  /**
   * Get tool parameters (simplified)
   */
  getToolParams(toolName) {
    const params = {
      dsl_list_tracks: {},
      dsl_track_create: {
        name: { type: 'string' },
        role: { type: 'string' }
      },
      dsl_track_volume: {
        track: { type: ['string', 'integer'] },
        volume: { type: ['string', 'number'] }
      },
      dsl_track_pan: {
        track: { type: ['string', 'integer'] },
        pan: { type: ['string', 'number'] }
      },
      dsl_track_mute: {
        track: { type: ['string', 'integer'] }
      },
      dsl_track_solo: {
        track: { type: ['string', 'integer'] }
      },
      dsl_play: {},
      dsl_stop: {},
      dsl_set_tempo: {
        bpm: { type: 'number' }
      }
    };

    return params[toolName] || {};
  }

  /**
   * Run test suite
   */
  async runTests(testCases) {
    console.log('Starting Enhanced NLP Tests with Conversation Tracking\n');

    // Start services
    await this.startMCPServer();
    
    // Run tests
    for (const testCase of testCases) {
      await this.testConversation(testCase.input, testCase.expectedIntent);
      
      // Rate limiting
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Generate reports
    this.tracker.generateActionableReport();

    // Find previous session for comparison
    const trackingDir = path.join(__dirname, 'conversation-tracking');
    if (fs.existsSync(trackingDir)) {
      const files = fs.readdirSync(trackingDir)
        .filter(f => f.startsWith('session-') && f.endsWith('.json'))
        .sort();
      
      if (files.length > 1) {
        const previousFile = files[files.length - 2];
        console.log(`\nComparing with previous session: ${previousFile}`);
        this.tracker.compareWithPrevious(path.join(trackingDir, previousFile));
      }
    }

    return this.tracker.conversations;
  }

  /**
   * Cleanup
   */
  cleanup() {
    if (this.mcpProcess) {
      console.log('\nStopping MCP server...');
      this.mcpProcess.kill();
    }
    if (this.chatProcess) {
      console.log('Stopping Reaper Chat...');
      this.chatProcess.kill();
    }
  }
}

// Comprehensive test cases
const testCases = [
  // Information requests
  {
    input: "what are the names of the tracks?",
    expectedIntent: "list track names and details"
  },
  {
    input: "how many tracks do I have?",
    expectedIntent: "count and list tracks"
  },
  {
    input: "show me what I'm working with",
    expectedIntent: "project overview"
  },
  
  // Volume adjustments
  {
    input: "make the drums louder",
    expectedIntent: "increase drum track volume"
  },
  {
    input: "the bass is too loud",
    expectedIntent: "decrease bass track volume"
  },
  {
    input: "I can't hear the vocals",
    expectedIntent: "increase vocal track volume or solo"
  },
  
  // Track creation
  {
    input: "I need a bass track",
    expectedIntent: "create bass track"
  },
  {
    input: "add something for the rhythm",
    expectedIntent: "create rhythm/drum track"
  },
  {
    input: "create a new instrument",
    expectedIntent: "create new track"
  },
  
  // Playback control
  {
    input: "play it",
    expectedIntent: "start playback"
  },
  {
    input: "stop the music",
    expectedIntent: "stop playback"
  },
  {
    input: "make it faster",
    expectedIntent: "increase tempo"
  },
  
  // Mixing
  {
    input: "put the guitar on the left",
    expectedIntent: "pan guitar left"
  },
  {
    input: "everything sounds centered",
    expectedIntent: "adjust panning"
  },
  {
    input: "make it wider",
    expectedIntent: "stereo width adjustment"
  },
  
  // Troubleshooting
  {
    input: "I can't hear anything",
    expectedIntent: "check mute/solo/volume"
  },
  {
    input: "something's wrong with track 2",
    expectedIntent: "diagnose track 2 issue"
  },
  
  // Natural variations
  {
    input: "turn it up",
    expectedIntent: "increase volume"
  },
  {
    input: "too quiet",
    expectedIntent: "increase volume"
  },
  {
    input: "shut it off",
    expectedIntent: "mute or stop"
  },
  {
    input: "give me a beat",
    expectedIntent: "create drum track or pattern"
  }
];

// Main execution
async function main() {
  const tester = new TrackedNLPTester();
  
  if (!tester.apiKey) {
    console.error('Error: OPENAI_API_KEY environment variable not set');
    console.error('Please set it with: export OPENAI_API_KEY=your-api-key');
    process.exit(1);
  }

  try {
    const results = await tester.runTests(testCases);
    
    console.log('\n=== FINAL SUMMARY ===');
    console.log(`Total conversations tracked: ${results.length}`);
    console.log(`Check conversation-tracking/ directory for detailed reports`);
    
  } catch (error) {
    console.error('Test runner error:', error);
  } finally {
    tester.cleanup();
  }
}

// Handle cleanup
process.on('SIGINT', () => {
  console.log('\nInterrupted, cleaning up...');
  process.exit(0);
});

if (require.main === module) {
  main();
}

module.exports = { TrackedNLPTester };