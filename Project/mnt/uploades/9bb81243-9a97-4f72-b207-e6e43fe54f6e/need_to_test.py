import os
import json
import openai

# Set your OpenAI API key (you can also set it as an environment variable).
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# Define a simple function that simulates fetching weather data.
def get_weather(location: str) -> dict:
    """
    Simulated function to get weather data.
    In a real-world scenario, you would replace this with an API call to a weather service.
    """
    # For demonstration, we return a fixed response.
    return {
        "location": location,
        "temperature": 68,  # Temperature in Fahrenheit
        "condition": "partly cloudy"
    }

# Define function metadata used by the model to know when/how to call our function.
functions = [
    {
        "name": "get_weather",
        "description": "Fetches the current weather for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or region for which to fetch the weather."
                }
            },
            "required": ["location"],
        },
    }
]

# Start the conversation with an initial system and user message.
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather in London?"}
]

# First, call the ChatCompletion with function definitions.
response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=messages,
    functions=functions,
    function_call="auto"  # Let the assistant decide if a function should be called.
)

message = response["choices"][0]["message"]

# Check if the model decided to call a function.
if message.get("function_call"):
    # Parse the function call's arguments from the model.
    function_name = message["function_call"]["name"]
    arguments = json.loads(message["function_call"]["arguments"])
    
    # For this example, we only have one function: get_weather.
    if function_name == "get_weather":
        location = arguments.get("location")
        weather_data = get_weather(location)  # Call our simulated function.
        
        # Now, add the function call and its result to our message history.
        messages.append(message)  # The assistant's message with the function call.
        messages.append({
            "role": "function",
            "name": function_name,
            "content": json.dumps(weather_data)
        })
        
        # Continue the conversation by passing the updated message history.
        second_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
        )
        
        final_reply = second_response["choices"][0]["message"]["content"]
        print("Assistant:", final_reply)
else:
    # If no function was called, simply output the assistant's message.
    print("Assistant:", message["content"])

