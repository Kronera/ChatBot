# chatbot.py

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure you have the NLTK data required
nltk.download('punkt')
nltk.download('stopwords')

# Define a dictionary of predefined responses
responses = {
    "hello": "Hi there! How can I help you?",
    "hi": "Hello! What can I do for you today?",
    "how are you": "I'm just a chatbot, but I'm here to help you!",
    "what is your name": "I'm ChatBot, your virtual assistant.",
    "bye": "Goodbye! Have a great day!",
    "thank you": "You're welcome!",
    "thanks": "You're welcome!"
}

# Function to preprocess user input
def preprocess(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Convert to lower case
    tokens = [word.lower() for word in tokens]
    # Remove punctuation and non-alphabetic characters
    words = [word for word in tokens if word.isalpha()]
    return ' '.join(words)

# Function to get a response from the chatbot
def get_response(user_input):
    # Preprocess the user input
    cleaned_input = preprocess(user_input)
    # Check if the cleaned input exactly matches any predefined response keys
    if cleaned_input in responses:
        return responses[cleaned_input]
    return "I'm sorry, I don't understand that."

# Main function to interact with the chatbot
def chat():
    print("ChatBot: Hello! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print("ChatBot: Goodbye! Have a great day!")
            break
        response = get_response(user_input)
        print("ChatBot:", response)

# Run the chat function
if __name__ == "__main__":
    chat()
