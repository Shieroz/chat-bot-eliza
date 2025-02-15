import nltk
import re
import random
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

#Needs name input handling

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Reflection dictionary to map user phrases
reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

# Pattern-response pairs
#enhance this to include emotions
patterns = [
    (r'i need (.*)', ["Why do you need %1?", "Would it help you to get %1?"]),
    (r'why don\'?t you (.*)\??', ["Do you really think I don't %1?", "Would you like me to %1?"]),
    (r'i can\'?t (.*)', ["What makes you think you can't %1?", "Have you tried?"]),
    (r'i am (.*)', ["Why do you think you are %1?", "How long have you been %1?"]),
    (r'i\'?m (.*)', ["How does being %1 make you feel?", "Why do you tell me you're %1?"]),
    (r'are you (.*)\??', ["What makes you ask that?", "Perhaps I am %1. What do you think?"]),
    (r'what (.*)', ["Why do you ask?", "What do you think?"]),
    (r'because (.*)', ["Is that the real reason?", "What other reasons come to mind?"]),
    (r'i feel (.*)', ["Tell me more about these %1 feelings.", "Do you often feel %1?"]),
    (r'i want (.*)', ["Why do you want %1?", "If you got %1, what would you do?"]),
    (r'(.*)\?', ["Why do you ask that?", "Can you answer that yourself?"]),
    (r'quit', ["Goodbye!", "Take care!"]),
    (r'(.*)', ["Tell me more.", "Why do you say that?", "Can you elaborate?"])
]

# Preprocessing function
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    #filtered_tokens = [word for word in tokens if word not in stop_words]
    #lemmatized_tokens = [lemmatizer.lemmatize(word, pos='v') for word in filtered_tokens]
    #return ' '.join(lemmatized_tokens)
    return ' '.join(tokens)

# Function to reflect user statements
def reflect(sentence):
    words = sentence.lower().split()
    return ' '.join([reflections.get(word, word) for word in words])

def generate_response(user_input):
    preprocessed_input = preprocess_input(user_input)
    #print(f"Preprocessed Input: {preprocessed_input}")  # Debugging line

    for pattern, responses in patterns:
        match = re.search(pattern, preprocessed_input, re.IGNORECASE)
        if match:
            #print(f"Matched Pattern: {pattern}")  # Debugging line
            response = random.choice(responses)
            if "%1" in response:
                response = response.replace("%1", reflect(match.group(1)))
            return response
    return "I'm not sure I understand. Can you tell me more?"

def eliza_chatbot():
    print("Eliza: Hi! I'm Eliza, a psychotherapist. What's on your mind?")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Eliza: Goodbye! Take care!")
            break
        response = generate_response(user_input)
        print(f"Eliza: {response}")

eliza_chatbot()

