import openai

# Replace with your actual OpenAI API key
api_key = "sk-proj-S1T72cS09PcdYOIgH31ET3BlbkFJiepW8yBG1HyoCoOiOe3J"

# Function to get a response from the API
def get_openai_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" depending on your model
        messages=messages
    )
    return response.choices[0].message['content']

# Initial message history
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# Example user message
user_message = "How can I pass chat history in OpenAI?"

# Append the user message to the message history
messages.append({"role": "user", "content": user_message})

# Get the assistant's response
assistant_response = get_openai_response(messages)

# Append the assistant's response to the message history
messages.append({"role": "assistant", "content": assistant_response})

# Print the assistant's response
print(assistant_response)

# Continue the conversation with a new user message
new_user_message = "Can you show me a code example?"

# Append the new user message to the message history
messages.append({"role": "user", "content": new_user_message})

# Get the assistant's response to the new user message
assistant_response = get_openai_response(messages)

# Append the assistant's response to the message history
messages.append({"role": "assistant", "content": assistant_response})

# Print the assistant's new response
print(assistant_response)
