require('dotenv').config();
const readline = require('readline');
const { MemorySaver } = require('@langchain/langgraph/checkpoint/memory');
const { graph } = require('./graph');

// Configuration for the chat session
const config = {
    configurable: {
        thread_id: "2"  // Unique identifier for the user session
    }
};

// Create readline interface for user input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

async function init() {
    try {
        // Create a MemorySaver instance for checkpoints
        const checkpointer = new MemorySaver();
        
        // Create the chat graph with the checkpointer
        const graphWithCheckpointer = graph;
        
        // Function to handle chat input
        const chat = async () => {
            rl.question('>> ', async (userInput) => {
                try {
                    // Process the user input through the graph with the checkpointer
                    const result = await graphWithCheckpointer.invoke(
                        { messages: [{ role: "user", content: userInput }] },
                        { ...config, callbacks: [] }
                    );
                    
                    // Display the response
                    if (result && result.messages && result.messages.length > 0) {
                        const lastMessage = result.messages[result.messages.length - 1];
                        const content = typeof lastMessage === 'string' 
                            ? lastMessage 
                            : lastMessage.content;
                        console.log('AI:', content);
                    }
                    
                    // Continue the chat
                    chat();
                } catch (error) {
                    console.error('Error processing message:', error);
                    rl.close();
                }
            });
        };
        
        // Start the chat
        console.log('Chat started. Type your message and press Enter to send.');
        chat();
        
    } catch (error) {
        console.error('Error initializing chat:', error);
        process.exit(1);
    }
}

// Start the application
init();

// Handle process termination
process.on('SIGINT', () => {
    console.log('\nExiting chat...');
    process.exit(0);
});
