const fs = require('fs');
const WebSocket = require('ws');

/**
 * NLP Test with Response Evaluation
 * 
 * This tests through the actual running Reaper Chat app
 * and evaluates the quality of responses
 */

class NLPResponseEvaluator {
  constructor() {
    this.apiKey = process.env.OPENAI_API_KEY;
    this.results = [];
    this.ws = null;
  }

  /**
   * Connect to the MCP relay WebSocket
   */
  async connectToMCPRelay() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket('ws://localhost:8765/mcp');
      
      this.ws.on('open', () => {
        console.log('Connected to MCP relay');
        resolve();
      });

      this.ws.on('error', (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      });

      this.ws.on('message', (data) => {
        try {
          const message = JSON.parse(data);
          console.log('MCP message:', message);
        } catch (e) {
          // Ignore non-JSON messages
        }
      });
    });
  }

  /**
   * Simulate the full conversation flow
   */
  async simulateConversation(userInput) {
    // 1. Get improved system prompt
    const systemPrompt = fs.readFileSync('improved-system-prompt.md', 'utf8')
      .split('```')[1];

    // 2. Get LLM response with tools
    const llmResponse = await this.getLLMResponse(userInput, systemPrompt);
    
    // 3. Execute tools if any
    let toolResults = [];
    if (llmResponse.tool_calls && llmResponse.tool_calls.length > 0) {
      for (const toolCall of llmResponse.tool_calls) {
        const result = await this.executeTool(
          toolCall.function.name, 
          JSON.parse(toolCall.function.arguments)
        );
        toolResults.push({
          tool: toolCall.function.name,
          result: result
        });
      }
    }

    // 4. Get final LLM response with tool results
    let finalResponse = llmResponse.content;
    if (toolResults.length > 0 && !llmResponse.content) {
      // If no content but tools were called, get follow-up response
      finalResponse = await this.getLLMFollowUp(userInput, toolResults);
    }

    return {
      userInput,
      llmResponse,
      toolResults,
      finalResponse
    };
  }

  /**
   * Get LLM response
   */
  async getLLMResponse(userInput, systemPrompt) {
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
        tools: this.getToolDefinitions(),
        tool_choice: 'auto',
        temperature: 0.1
      })
    });

    const data = await response.json();
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
      messages.push({
        role: 'assistant',
        content: `Executed ${tr.tool}: ${JSON.stringify(tr.result)}`
      });
    });

    messages.push({
      role: 'user',
      content: 'Please provide a user-friendly response based on the tool results.'
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
   * Execute tool (mock for now)
   */
  async executeTool(toolName, args) {
    // In a real implementation, this would call the MCP server
    // For now, return mock responses
    const mockResponses = {
      'dsl_list_tracks': {
        success: true,
        result: [{ 
          type: 'text', 
          text: 'Found 2 tracks:\nTrack 1: Bass (MIDI, 2 FX)\nTrack 2: Drums (Audio)' 
        }]
      },
      'dsl_track_create': {
        success: true,
        result: [{ 
          type: 'text', 
          text: 'Created track "' + (args.name || 'New Track') + '" at position ' + (args.position || 3) 
        }]
      },
      'dsl_track_volume': {
        success: true,
        result: [{ 
          type: 'text', 
          text: 'Set track ' + args.track + ' volume to ' + args.volume 
        }]
      }
    };

    return mockResponses[toolName] || { 
      success: false, 
      error: 'Unknown tool' 
    };
  }

  /**
   * Evaluate conversation quality
   */
  async evaluateConversation(conversation) {
    const evaluationPrompt = `
Evaluate this DAW assistant conversation:

User: "${conversation.userInput}"
Assistant response: "${conversation.finalResponse}"
Tools used: ${conversation.toolResults.map(t => t.tool).join(', ') || 'none'}

Rate on these criteria (0-10):
1. Answered Question: Did the response directly answer what was asked?
2. Completeness: Was all necessary information provided?
3. Clarity: Was the response clear and easy to understand?
4. Helpfulness: Would this help a non-technical user?
5. Accuracy: Was the information correct?

Also identify:
- What worked well
- What could be improved
- Any missing information

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
            content: 'You are evaluating a conversation. Respond with valid JSON only, no markdown.' 
          },
          { role: 'user', content: evaluationPrompt }
        ],
        temperature: 0.1
      })
    });

    const data = await response.json();
    const content = data.choices[0].message.content;
    
    try {
      // Remove markdown if present
      const jsonStr = content.replace(/```json\n?/g, '').replace(/```\n?/g, '');
      return JSON.parse(jsonStr);
    } catch (e) {
      console.error('Failed to parse evaluation:', content);
      return {
        answered_question: 0,
        completeness: 0,
        clarity: 0,
        helpfulness: 0,
        accuracy: 0,
        worked_well: ['Failed to evaluate'],
        improvements: ['Evaluation parsing failed'],
        missing_info: []
      };
    }
  }

  /**
   * Run test suite
   */
  async runTests(testCases) {
    console.log('Starting NLP Response Evaluation Tests\n');

    for (const testCase of testCases) {
      console.log(`\nTesting: "${testCase.input}"`);
      console.log(`Expected: ${testCase.expectedInfo}`);

      try {
        // Simulate conversation
        const conversation = await this.simulateConversation(testCase.input);
        
        console.log(`Tools called: ${conversation.toolResults.map(t => t.tool).join(', ') || 'none'}`);
        console.log(`Response: ${conversation.finalResponse?.substring(0, 200)}...`);

        // Evaluate quality
        const evaluation = await this.evaluateConversation(conversation);
        
        const avgScore = (
          evaluation.answered_question +
          evaluation.completeness +
          evaluation.clarity +
          evaluation.helpfulness +
          evaluation.accuracy
        ) / 5;

        console.log(`Average score: ${avgScore.toFixed(1)}/10`);
        
        if (evaluation.improvements && evaluation.improvements.length > 0) {
          console.log(`Improvements needed: ${evaluation.improvements.join(', ')}`);
        }

        this.results.push({
          testCase,
          conversation,
          evaluation,
          avgScore,
          success: avgScore >= 7
        });

      } catch (error) {
        console.error(`Test failed: ${error.message}`);
        this.results.push({
          testCase,
          error: error.message,
          success: false,
          avgScore: 0
        });
      }

      // Rate limiting
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    this.generateReport();
  }

  /**
   * Generate report
   */
  generateReport() {
    const totalTests = this.results.length;
    const successfulTests = this.results.filter(r => r.success).length;
    const avgScore = this.results.reduce((sum, r) => sum + (r.avgScore || 0), 0) / totalTests;

    console.log('\n\n=== Response Quality Evaluation Report ===');
    console.log(`Total Tests: ${totalTests}`);
    console.log(`Successful (≥7/10): ${successfulTests} (${(successfulTests/totalTests*100).toFixed(1)}%)`);
    console.log(`Average Score: ${avgScore.toFixed(1)}/10`);

    // Category scores
    const categoryScores = {
      answered_question: 0,
      completeness: 0,
      clarity: 0,
      helpfulness: 0,
      accuracy: 0
    };

    this.results.forEach(r => {
      if (r.evaluation) {
        Object.keys(categoryScores).forEach(key => {
          categoryScores[key] += r.evaluation[key] || 0;
        });
      }
    });

    console.log('\n=== Category Breakdown ===');
    Object.entries(categoryScores).forEach(([category, total]) => {
      const avg = total / totalTests;
      console.log(`${category}: ${avg.toFixed(1)}/10`);
    });

    // Common improvements needed
    const improvements = {};
    this.results.forEach(r => {
      if (r.evaluation && r.evaluation.improvements) {
        r.evaluation.improvements.forEach(imp => {
          improvements[imp] = (improvements[imp] || 0) + 1;
        });
      }
    });

    console.log('\n=== Common Improvements Needed ===');
    Object.entries(improvements)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .forEach(([imp, count]) => {
        console.log(`- ${imp} (${count} times)`);
      });

    // Save results
    fs.writeFileSync(
      'nlp-response-evaluation-results.json',
      JSON.stringify(this.results, null, 2)
    );
    console.log('\nDetailed results saved to nlp-response-evaluation-results.json');
  }

  /**
   * Get tool definitions
   */
  getToolDefinitions() {
    const toolDefs = JSON.parse(
      fs.readFileSync('improved-tool-descriptions.json', 'utf8')
    );

    // Convert to OpenAI format
    return Object.entries(toolDefs.tool_descriptions).map(([name, info]) => ({
      type: 'function',
      function: {
        name: name,
        description: info.improved,
        parameters: {
          type: 'object',
          properties: this.getToolParameters(name)
        }
      }
    }));
  }

  /**
   * Get tool parameters (simplified)
   */
  getToolParameters(toolName) {
    const params = {
      dsl_track_create: {
        name: { type: 'string', description: 'Track name' },
        role: { type: 'string', description: 'Track type (bass, drums, etc)' },
        position: { type: 'integer', description: 'Track position' }
      },
      dsl_track_volume: {
        track: { type: ['string', 'integer'], description: 'Track identifier' },
        volume: { type: ['string', 'number'], description: 'Volume level' }
      },
      dsl_track_pan: {
        track: { type: ['string', 'integer'], description: 'Track identifier' },
        pan: { type: ['string', 'number'], description: 'Pan position' }
      },
      dsl_list_tracks: {}
    };

    return params[toolName] || {};
  }
}

// Enhanced test cases
const testCases = [
  {
    input: "what are the names of the tracks?",
    expectedInfo: "List of track names with details"
  },
  {
    input: "I need something for the bass",
    expectedInfo: "Bass track creation"
  },
  {
    input: "make the drums louder",
    expectedInfo: "Drum track volume increase"
  },
  {
    input: "show me what I'm working with",
    expectedInfo: "Project overview with all tracks"
  },
  {
    input: "the vocals are too quiet",
    expectedInfo: "Vocal track volume adjustment"
  },
  {
    input: "create a rhythm section",
    expectedInfo: "Multiple track creation or guidance"
  },
  {
    input: "how many tracks do I have?",
    expectedInfo: "Track count and list"
  },
  {
    input: "set up for recording guitar",
    expectedInfo: "Guitar track creation with recording tips"
  },
  {
    input: "everything sounds centered",
    expectedInfo: "Panning suggestions or adjustments"
  },
  {
    input: "I can't hear anything",
    expectedInfo: "Troubleshooting help (volume, mute, solo)"
  }
];

// Main
async function main() {
  const evaluator = new NLPResponseEvaluator();
  
  if (!evaluator.apiKey) {
    console.error('Error: OPENAI_API_KEY not set');
    process.exit(1);
  }

  try {
    await evaluator.runTests(testCases);
  } catch (error) {
    console.error('Test error:', error);
  }
}

if (require.main === module) {
  main();
}

module.exports = { NLPResponseEvaluator };