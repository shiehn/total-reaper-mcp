const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * Full Execution NLP Test Framework
 * 
 * This framework tests the complete pipeline:
 * 1. Natural language input
 * 2. LLM tool selection
 * 3. MCP tool execution
 * 4. REAPER command execution
 * 5. Response quality evaluation
 */

class FullExecutionNLPTester {
  constructor() {
    this.mcpProcess = null;
    this.results = [];
    this.mcpServerPath = process.env.VITE_MCP_SERVER_PATH || '/Users/stevehiehn/total-reaper-mcp';
    this.apiKey = process.env.OPENAI_API_KEY;
  }

  /**
   * Start MCP server
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
        if (output.includes('Server started')) {
          console.log('MCP server started successfully');
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
   * Call MCP tool directly
   */
  async callMCPTool(toolName, params = {}) {
    return new Promise((resolve, reject) => {
      const request = {
        jsonrpc: '2.0',
        method: 'tools/call',
        params: {
          name: toolName,
          arguments: params
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

      // Timeout after 5 seconds
      setTimeout(() => {
        this.mcpProcess.stdout.removeListener('data', responseHandler);
        reject(new Error('MCP tool call timeout'));
      }, 5000);
    });
  }

  /**
   * Get LLM to select tool and parameters
   */
  async getLLMToolSelection(userInput, tools) {
    const systemPrompt = fs.readFileSync(
      path.join(__dirname, 'improved-system-prompt.md'), 
      'utf8'
    ).split('```')[1];

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

    const message = data.choices[0].message;
    return {
      content: message.content,
      tool_calls: message.tool_calls || []
    };
  }

  /**
   * Evaluate response quality
   */
  async evaluateResponse(userInput, toolCalled, toolResult, llmResponse) {
    const evaluationPrompt = `
You are evaluating a DAW assistant's response quality.

User asked: "${userInput}"
Tool called: ${toolCalled}
Tool result: ${JSON.stringify(toolResult)}
Assistant's response: ${llmResponse}

Evaluate on these criteria (0-10 scale):
1. Answered Question: Did it directly answer what the user asked?
2. Correct Tool: Was the right tool selected for the task?
3. Complete Response: Was all necessary information provided?
4. User Friendly: Was the response clear and non-technical?

Respond with JSON only:
{
  "answered_question": 0-10,
  "correct_tool": 0-10,
  "complete_response": 0-10,
  "user_friendly": 0-10,
  "issues": ["list of specific issues"],
  "suggestions": ["list of improvements"]
}`;

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: 'gpt-4-turbo-preview',
        messages: [
          { role: 'system', content: 'You are a quality evaluator. Respond with JSON only.' },
          { role: 'user', content: evaluationPrompt }
        ],
        temperature: 0.1
      })
    });

    const data = await response.json();
    try {
      return JSON.parse(data.choices[0].message.content);
    } catch (e) {
      console.error('Failed to parse evaluation:', data.choices[0].message.content);
      return null;
    }
  }

  /**
   * Run a single test
   */
  async runTest(testCase) {
    console.log(`\nTesting: "${testCase.input}"`);
    
    try {
      // Step 1: Get LLM tool selection
      const llmResponse = await this.getLLMToolSelection(
        testCase.input,
        this.getToolDefinitions()
      );

      let toolResult = null;
      let toolCalled = 'none';
      
      if (llmResponse.tool_calls && llmResponse.tool_calls.length > 0) {
        const toolCall = llmResponse.tool_calls[0];
        toolCalled = toolCall.function.name;
        const args = JSON.parse(toolCall.function.arguments);
        
        console.log(`  Tool selected: ${toolCalled}`);
        console.log(`  Parameters: ${JSON.stringify(args)}`);
        
        // Step 2: Execute MCP tool
        try {
          toolResult = await this.callMCPTool(toolCalled, args);
          console.log(`  Tool result: ${JSON.stringify(toolResult).substring(0, 100)}...`);
        } catch (error) {
          console.error(`  Tool execution failed: ${error.message}`);
          toolResult = { error: error.message };
        }
      }

      // Step 3: Evaluate response quality
      const evaluation = await this.evaluateResponse(
        testCase.input,
        toolCalled,
        toolResult,
        llmResponse.content || 'No response content'
      );

      // Calculate overall score
      const scores = evaluation ? [
        evaluation.answered_question,
        evaluation.correct_tool,
        evaluation.complete_response,
        evaluation.user_friendly
      ] : [0, 0, 0, 0];
      
      const overallScore = scores.reduce((a, b) => a + b, 0) / scores.length;

      const result = {
        testCase,
        toolCalled,
        toolResult,
        llmResponse: llmResponse.content,
        evaluation,
        overallScore,
        success: overallScore >= 7
      };

      this.results.push(result);
      
      console.log(`  Overall score: ${overallScore.toFixed(1)}/10`);
      if (evaluation && evaluation.issues.length > 0) {
        console.log(`  Issues: ${evaluation.issues.join(', ')}`);
      }

      return result;

    } catch (error) {
      console.error(`  Test failed: ${error.message}`);
      const result = {
        testCase,
        error: error.message,
        success: false,
        overallScore: 0
      };
      this.results.push(result);
      return result;
    }
  }

  /**
   * Run all tests
   */
  async runTests(testCases) {
    await this.startMCPServer();
    
    console.log('Running full execution tests...\n');

    for (const testCase of testCases) {
      await this.runTest(testCase);
      // Rate limiting
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    return this.generateReport();
  }

  /**
   * Generate detailed report
   */
  generateReport() {
    const totalTests = this.results.length;
    const successfulTests = this.results.filter(r => r.success).length;
    const averageScore = this.results.reduce((sum, r) => sum + r.overallScore, 0) / totalTests;

    console.log('\n=== Full Execution Test Report ===');
    console.log(`Total Tests: ${totalTests}`);
    console.log(`Successful: ${successfulTests} (${(successfulTests/totalTests*100).toFixed(1)}%)`);
    console.log(`Average Score: ${averageScore.toFixed(1)}/10`);

    // Group by issue type
    const issueFrequency = {};
    this.results.forEach(r => {
      if (r.evaluation && r.evaluation.issues) {
        r.evaluation.issues.forEach(issue => {
          issueFrequency[issue] = (issueFrequency[issue] || 0) + 1;
        });
      }
    });

    console.log('\n=== Common Issues ===');
    Object.entries(issueFrequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .forEach(([issue, count]) => {
        console.log(`- ${issue}: ${count} occurrences`);
      });

    // Low scoring tests
    console.log('\n=== Tests Needing Improvement ===');
    this.results
      .filter(r => r.overallScore < 7)
      .slice(0, 5)
      .forEach(r => {
        console.log(`\n"${r.testCase.input}" (Score: ${r.overallScore.toFixed(1)})`);
        if (r.evaluation) {
          console.log(`  Issues: ${r.evaluation.issues.join(', ')}`);
          console.log(`  Suggestions: ${r.evaluation.suggestions.join(', ')}`);
        }
      });

    // Save detailed results
    fs.writeFileSync(
      'nlp-full-execution-results.json',
      JSON.stringify(this.results, null, 2)
    );
    console.log('\nDetailed results saved to nlp-full-execution-results.json');

    return {
      summary: {
        totalTests,
        successfulTests,
        successRate: successfulTests / totalTests,
        averageScore
      },
      results: this.results
    };
  }

  /**
   * Get tool definitions
   */
  getToolDefinitions() {
    // Simplified for testing - in production, fetch from MCP
    return [
      {
        type: 'function',
        function: {
          name: 'dsl_list_tracks',
          description: 'Show what\'s in your project. Use when users ask what tracks exist or want an overview.',
          parameters: { type: 'object', properties: {} }
        }
      },
      {
        type: 'function',
        function: {
          name: 'dsl_track_create',
          description: 'Add a new instrument, voice, or sound to your project.',
          parameters: {
            type: 'object',
            properties: {
              name: { type: 'string', description: 'Track name' },
              role: { type: 'string', description: 'Track role (bass, drums, etc)' }
            }
          }
        }
      },
      {
        type: 'function',
        function: {
          name: 'dsl_track_volume',
          description: 'Make sounds louder or quieter.',
          parameters: {
            type: 'object',
            properties: {
              track: { type: ['string', 'integer'], description: 'Track reference' },
              volume: { type: ['number', 'string'], description: 'Volume value' }
            },
            required: ['track', 'volume']
          }
        }
      }
      // Add more tools as needed
    ];
  }

  /**
   * Cleanup
   */
  cleanup() {
    if (this.mcpProcess) {
      console.log('\nStopping MCP server...');
      this.mcpProcess.kill();
    }
  }
}

// Test cases focusing on response quality
const testCases = [
  {
    input: "what are the names of the tracks?",
    expectedInfo: "track names"
  },
  {
    input: "create a bass track",
    expectedInfo: "confirmation of track creation"
  },
  {
    input: "make track 1 louder",
    expectedInfo: "volume adjustment confirmation"
  },
  {
    input: "I need something for the drums",
    expectedInfo: "drum track creation"
  },
  {
    input: "show me what I have",
    expectedInfo: "project overview with track details"
  }
];

// Main execution
async function main() {
  const tester = new FullExecutionNLPTester();
  
  if (!tester.apiKey) {
    console.error('Error: OPENAI_API_KEY environment variable not set');
    process.exit(1);
  }

  try {
    await tester.runTests(testCases);
  } catch (error) {
    console.error('Test runner error:', error);
  } finally {
    tester.cleanup();
  }
}

// Handle cleanup on exit
process.on('SIGINT', () => {
  console.log('\nInterrupted, cleaning up...');
  process.exit(0);
});

if (require.main === module) {
  main();
}

module.exports = { FullExecutionNLPTester };