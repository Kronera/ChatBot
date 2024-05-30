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
def get_response(user_input):
    # Preprocess the user input
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
    
    if best_score > 60:  # Lower threshold for fuzzy matching
        return responses[best_match]
    
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
