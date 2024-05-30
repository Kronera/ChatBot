# chatbot.py

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from fuzzywuzzy import fuzz

# Ensure you have the NLTK data required
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Define a dictionary of predefined responses
responses = {
    "hello": "Hi there! How can I help you?",
    "hi": "Hello! What can I do for you today?",
    "hey": "Hi there! How can I help you?",
    "hello there": "Hi there! How can I help you?",
    "how are you": "I'm doing well, thank you! How can I assist you today?",
    "how do you do": "I'm just a chatbot, but I'm here to help you!",
    "how's it going": "I'm doing well, thank you! How can I assist you today?",
    "what is your name": "I'm ChatBot, your virtual assistant.",
    "who are you": "I'm ChatBot, your virtual assistant.",
    "tell me your name": "I'm ChatBot, your virtual assistant.",
    "thank you": "You're welcome!",
    "thanks": "You're welcome!",
    "thanks a lot": "You're welcome!",
    "thank you very much": "You're welcome!",
    "how can you help me": "I can assist you with general questions. What do you need help with?"
}

# Add variations of 'bye' to be recognized as a farewell
farewell_phrases = ["bye", "goodbye", "see you later", "bye bye", "byee", "ciao", "adios"]

# Function to preprocess user input
def preprocess(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    words = [word for word in tokens if word.isalpha()]
    return ' '.join(words)

# Function to find synonyms
def find_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Function to generate all possible phrases including synonyms
def generate_phrases(phrase):
    words = word_tokenize(phrase)
    all_phrases = set()
    for i in range(len(words)):
        synonyms = find_synonyms(words[i])
        for synonym in synonyms:
            new_phrase = words[:i] + [synonym] + words[i+1:]
            all_phrases.add(' '.join(new_phrase))
    return all_phrases

# Function to get a response from the chatbot
def get_response(user_input, context):
    cleaned_input = preprocess(user_input)
    best_match = None
    best_score = 0
    
    for key in responses:
        all_phrases = generate_phrases(key)
        all_phrases.add(key)
        
        for phrase in all_phrases:
            score = fuzz.partial_ratio(cleaned_input, phrase)
            if score > best_score:
                best_score = score
                best_match = key

    if best_score > 60:
        response = responses[best_match]
        context['last_interaction'] = best_match
        return response
    
    return "I'm sorry, I don't understand that."

# Main function to interact with the chatbot
def chat():
    print("ChatBot: Hello! Type 'bye' to exit.")
    context = {}
    while True:
        user_input = input("You: ")
        if preprocess(user_input) in farewell_phrases:
            print("ChatBot: Goodbye! Have a great day!")
            break
        response = get_response(user_input, context)
        print("ChatBot:", response)

# Run the chat function
if __name__ == "__main__":
    chat()
