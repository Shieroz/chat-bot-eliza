from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re, json, random, sys, string

tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()
match_groups = dict()

# Remember important details about the user
memory = {
    "last_response": "",
    "name": ""
}

# Load the responses of eliza
with open('./keywords.json', 'r') as file:
    data = json.load(file)

# Reverse dictionary to map from keywords to themes
keyword_map = dict()
for theme in data["themes"]:
    for word in data["themes"][theme]["keywords"]:
        keyword_map[word] = theme

# Returns a random response template
def _choose_response(key: str) -> str:
    response = ""
    # Whether to look in regex pattern or themes keywords
    choice = "patterns" if key not in data["themes"] else "themes"
    # Replace all place holders with user response
    response = random.choice(data[choice][key]["responses"])
    match = re.search(r'(%\d+)', response)
    if match:
        i = 0
        for group in match.groups():
            response = response.replace(group, _reflect(match_groups[key][i]))
            i += 1

    return response

def eliza():
    """ Main program loop for the Eliza chatbot """
    while True:
        # Get user input and clean it
        user_input = input("> ")
        
        if user_input == memory["last_response"]:
            print(random.choice(data["REPEATED"])) # Check if user is repeating themselves
        elif user_input == "":
            print(random.choice(data["EMPTY"]))
        else:
            memory["last_response"] = user_input
            _respond(user_input)

def _preprocess_input(text: str) -> str:
    tokens = text.lower().split(" ")
    tokens = [token for token in tokens if token not in string.punctuation] # Remove punctuations
    tokens = [data["decompose"].get(token, token) for token in tokens]
    return ' '.join(tokens)

def _reflect(sentence: str) -> str:
    words = sentence.lower().split()
    return ' '.join([data["reflections"].get(word, word) for word in words])

def _data_cleaning(text: str) -> list:
    """ Clean up the text data by removing stopwords and lemmatize nouns and verbs"""
    # Clean up punctuations and convert to lowercase
    tokens = tokenizer.tokenize(text.lower())

    # Clean up stopwords
    tokens = [token for token in tokens if token not in stopwords.words('english')]

    # Lemmatize nouns, verbs, adjectives and adverbs
    for i in ['n', 'v', 'a', 'r']:
        tokens = [lemmatizer.lemmatize(word, pos=i) for word in tokens]

    return tokens

def _respond(input: str):
    weights = dict()
    # Match all regex pattern from json and assign weights to them
    preprocess_input = _preprocess_input(input)
    for pattern in data["patterns"]:
        regex = re.compile(data["patterns"][pattern]["pattern"].replace("\\", "\\"), re.IGNORECASE)
        match = re.search(regex, preprocess_input)
        if match:
            weights[data["patterns"][pattern]["weight"]] = pattern
            match_groups[pattern] = match.groups()
    # Find keywords in input
    lemmatized_input = _data_cleaning(input)
    keywords = dict()
    for word in lemmatized_input:
        if word in keyword_map:
            keywords[word] = keyword_map[word]
            weights[data["themes"][keyword_map[word]]["weight"]] = keyword_map[word]

    # If no keywords are detected defaults to NULL responses
    if not weights:
        print(random.choice(data["NULL"]))
    # Handle program exit
    elif "quit" in keywords.values():
        print(_choose_response("quit"))
        sys.exit(0)
    # Actual response
    else:
        # Sort keywords by weights
        weight_list = sorted(weights.keys(), reverse=True)
        # Answer using the highest weighted keyword to keep it simple for now
        print(_choose_response(weights[weight_list[0]]))

if __name__ == "__main__":
    print("Type \"goodbye\" to quit.")
    print("Hello, I am Eliza. I'll be your therapist today.")
    eliza()