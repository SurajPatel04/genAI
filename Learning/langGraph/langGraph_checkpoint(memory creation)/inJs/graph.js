require('dotenv').config();
const { StateGraph, END, START } = require('@langchain/langgraph');
const { ChatGoogleGenerativeAI } = require('@langchain/google-genai');

// Initialize the chat model
const model = new ChatGoogleGenerativeAI({
    modelName: 'gemini-1.5-pro', // Updated to a more commonly available model
    apiKey: process.env.GOOGLE_API_KEY,
    temperature: 0.7,
});

// Define the state type using annotations
const { Annotation } = require('@langchain/langgraph');

const GraphState = Annotation.Root({
    messages: {
        value: (x, y) => x.concat(y),
        default: () => []
    }
});

// Chat function that processes the state and returns a new state
async function chat(state) {
    try {
        const response = await model.invoke([state.messages[state.messages.length - 1]]);
        return { messages: [response] };
    } catch (error) {
        console.error('Error in chat function:', error);
        throw error;
    }
}

// Create the graph builder
const workflow = new StateGraph(GraphState);

// Add nodes and edges
workflow.addNode('chat', chat);
workflow.addEdge(START, 'chat');
workflow.addEdge('chat', END);

// Compile the graph
const graph = workflow.compile();

module.exports = {
    graph
};
