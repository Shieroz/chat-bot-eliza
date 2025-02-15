from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json
import random
import sys

tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()

# Remember important details about the user
memory = dict()

# Load the responses of eliza
with open('./keywords.json', 'r') as file:
    data = json.load(file)

# Reverse dictionary to map from keywords to theme
keyword_map = dict()
for theme in data:
    if "keywords" in data[theme]:
        for word in data[theme]["keywords"]:
            keyword_map[word] = theme

# Returns a random response template
def _choose_response(theme: str) -> str:
    return random.choice(data[theme]["responses"])

def eliza():
    """ Main program loop for the Eliza chatbot """
    while True:
        # Get user input and clean it
        user_input = input("> ")
        if user_input == "":
            print(random.choice(data["EMPTY"]))
        else:
            clean_text = _data_cleaning(user_input)
            _respond(clean_text)

def _data_cleaning(text: str) -> list:
    """ Clean up the text data by removing punctuations stopwords and lemmatize nouns and verbs"""
    # Clean up punctuations and convert to lowercase
    tokens = tokenizer.tokenize(text.lower())

    # Clean up stopwords
    tokens = [token for token in tokens if token not in stopwords.words('english')]

    # Lemmatize nouns, verbs, adjectives and adverbs
    for i in ['n', 'v', 'a', 'r']:
        tokens = [lemmatizer.lemmatize(word, pos=i) for word in tokens]

    return tokens

def _respond(input: list):
    # Find keywords in input
    keywords = dict()
    weights = dict()
    for word in input:
        if word in keyword_map:
            keywords[word] = keyword_map[word]
            weights[data[keyword_map[word]]["weight"]] = keyword_map[word]

    # If no keywords are detected defaults to NULL responses
    if not keywords:
        print(random.choice(data["NULL"]))
    # Handle program exit
    elif "quit" in keywords.values():
        sys.exit(_choose_response("quit"))
    # Actual response
    else:
        # Sort keywords by weights
        weight_list = sorted(weights.keys(), reverse=True)
        # Answer using the highest weighted keyword to keep it simple for now
        print(_choose_response(weights[weight_list[0]]))

if __name__ == "__main__":
    print("Type \"goodbye\" to quit.")
    print("Hi, I'm a psychotherapist. What is your name?")
    eliza()