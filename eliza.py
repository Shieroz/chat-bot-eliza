from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()
first = True

def eliza():
    """ Main function for the Eliza chatbot """
    global first
    while True:
        user_input = input()
        if user_input.lower() == "goodbye":
            print("Goodbye! Have a nice day!")
            break
        clean_text = data_cleaning(user_input)

        if first:
            name = clean_text[-1]
            print(f"Hi {name}. How can I help you today?")
            first = False

        else:
            clean_text = data_cleaning(user_input)
            print(clean_text)
            
            print("I'm sorry to hear that. Can you tell me more about why you're feeling that way?")

def data_cleaning(text: str) -> list:
    """ Clean up the text data by removing punctuations stopwords and lemmatize nouns and verbs"""
    # Clean up punctuations and convert to lowercase
    tokens = tokenizer.tokenize(text.lower())

    # Clean up stopwords
    tokens = [token for token in tokens if token not in stopwords.words('english')]

    # Lemmatize nouns, verbs, adjectives and adverbs
    for i in ['n', 'v', 'a', 'r']:
        tokens = [lemmatizer.lemmatize(word, pos=i) for word in tokens]

    return tokens

if __name__ == "__main__":
    print("Hi, I'm a psychotherapist. What is your name?")
    eliza()