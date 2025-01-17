import random
import json
import time
import os

# Load responses from JSON file
def load_responses(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['responses']

# Function to get a random agent name
def get_agent_name():
    agents = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Jamie", "Riley", "Avery"]
    agent = random.choice(agents)
    return agent  # Randomly selects an agent

# Function to simulate random disconnections (5% chance)
def random_disconnect():
    return random.random() < 0.05  # 5% chance of disconnection

# Function to get a response based on user input
def get_response(user_input, user_name, responses):
    user_input_lower = user_input.lower()  # Convert the input to lowercase
    found_keywords = []

    # Loop through each keyword in the responses
    for keyword in responses:
        if keyword in user_input_lower:  # Check if the keyword is in the user input
            found_keywords.append(keyword)

    if found_keywords:
        # Return the first matching response (you can modify if you want more complex matching)
        response = responses[found_keywords[0]].format(name=user_name)
        return response
    else:
        # Default response if no match is found
        return f"I'm not sure about that, {user_name}. Can you ask something else?"

# Function to load or create user preferences
def load_user_preferences():
    # Check if the user preferences file exists
    if os.path.exists("user_preferences.json"):
        with open("user_preferences.json", "r") as file:
            return json.load(file)
    else:
        return None  # If no preferences file is found, return None

# Function to save user preferences
def save_user_preferences(user_data):
    # Save the user preferences (name and agent) to a JSON file
    with open("user_preferences.json", "w") as file:
        json.dump(user_data, file, indent=4)

# Function to log the chat session with timestamps
def log_chat(log_file, user_question, agent_response):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Get current time in a readable format
    with open(log_file, 'a') as file:
        file.write(f"{timestamp} - User: {user_question}\n")
        file.write(f"{timestamp} - Agent: {agent_response}\n\n")

# Function to suggest frequent topics based on user input
def suggest_frequent_topics(frequency_dict):
    if frequency_dict:
        sorted_topics = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
        top_topics = sorted_topics[:3]  # Top 3 frequent topics
        suggestions = "\n".join([f"• {topic}" for topic, count in top_topics])
        return f"Based on your questions, here are some topics you might be interested in:\n{suggestions}"
    else:
        return "I haven't noticed any frequent topics yet."

# Main chat function
def chat():
    print("Welcome to the University of Poppleton's chat service!")
    
    # Load user preferences (for returning users)
    user_data = load_user_preferences()

    if user_data is not None and "user_name" in user_data and "last_agent" in user_data:
        # If returning user, load their name and last agent
        user_name = user_data["user_name"]
        print(f"Welcome back, {user_name}! How can I assist you today?")
        agent_name = user_data["last_agent"]
        print(f"You're chatting with Agent {agent_name} again!")
    else:
        # If no preferences are saved, prompt for name
        user_name = input("Please enter your name: ")
        print(f"Hello, {user_name}! How can I assist you today?")
        agent_name = get_agent_name()  # Get a random agent name
        print(f"You are chatting with Agent {agent_name}.")

    # Save the user's name and agent to preferences for future sessions
    user_data = {"user_name": user_name, "last_agent": agent_name}
    save_user_preferences(user_data)  # Save the updated data

    # Load responses from JSON file
    responses = load_responses('responses.json')

    # Log file setup
    log_file = "chat_log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)  # Start fresh for each session

    # Dictionary to store frequency of topics asked
    topic_frequency = {}

    while True:
        # Get user input
        user_question = input(f"{user_name}: ")

        # Check for exit condition
        if user_question.lower() in ["bye", "exit", "quit", "see you later", "goodbye"]:
            print(f"Agent {agent_name}: Thank you for chatting, {user_name}! Have a great day!")
            break
        
        # Simulate random disconnection (5% chance now)
        if random_disconnect():
            print(f"Agent {agent_name} has disconnected. Please try again later.")
            break
        
        # Get the response
        response = get_response(user_question, user_name, responses)
        
        # Log the question and response with timestamp
        log_chat(log_file, user_question, response)

        # Track topic frequency
        user_input_lower = user_question.lower()
        for keyword in responses:
            if keyword in user_input_lower:
                if keyword in topic_frequency:
                    topic_frequency[keyword] += 1
                else:
                    topic_frequency[keyword] = 1
        
        # Suggest frequent topics based on the count
        print(suggest_frequent_topics(topic_frequency))
        
        # Display the response
        print(f"Agent {agent_name}: {response}")

# Run the chat function
if __name__ == "__main__":
    chat()