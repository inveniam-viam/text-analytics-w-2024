
# Natural Language Processing

# Process by which natural language (usually written language) is converted
# into a form (usually numbers) that could be understood by a computer.


import nltk 
from nltk.tokenize import sent_tokenize, word_tokenize

example_text: str = "Hello Mr. Smith, how are you doing today? The weather is great and Python is awesome. The sky is pinkish-blue. You should not eat cardboard."

# tokenizing by sentence
print(sent_tokenize(example_text))

# tokenizing by word
print(word_tokenize(example_text))
