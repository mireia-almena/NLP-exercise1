
## Exercise 1 NLP ##
##  Mireia Almena ##

#We import the necessary libraries 
from pathlib import Path
import spacy
import re 
import matplotlib.pyplot as plt 

#First of all we access our directories where we have previously saved our songs
eng_directory = Path("C:/Users/mirei/OneDrive/Escritorio/Uni/Master/NLP/cançons/en")
cat_directory = Path("C:/Users/mirei/OneDrive/Escritorio/Uni/Master/NLP/cançons/cat")

#We load the spacy pipelines for each language
nlp = spacy.load("en_core_web_sm")
cat_nlp = spacy.load("ca_core_news_sm")

#We create a function to apply to each directory, so we don't have to repeat the process for each language 
def zipfslaw_abbreviation(directory, language):
    text=""
    #We then iterate over the directory to access all of the files
    for file in directory.iterdir():
        with open(file, "r", encoding='utf-8') as f: 
            text += f.read() + "\n" #we compile all the texts in the directory, meaning putting all the songs for one language together 

    #Before tokenizing, we need to remove the [Verse / Pre-Chorus / etc.] that comes with Genius lyrics
    clean_text = re.sub(r'\[.*?\]', '', text)
    tokens = []

    #Then, we can tokenize it with spacy, using a different pipeline depending on the language
    if language == 'English':
        doc = nlp(clean_text.lower()) #we also lower the text because we want to treat all of them the same 
        for token in doc:
            if token.is_alpha: #We are only taking alphabetic characters, so we don't count spaces, numbers and punctuation. But we should be aware we are removing genitive 's and such.
                tokens.append(token.text) 

    if language == 'Catalan': 
        doc = cat_nlp(clean_text.lower())  
        for token in doc:
            if token.is_alpha: 
                tokens.append(token.text) 

                    
    #Then we need to measure the frequency of each word and put it in a dictionary
    freq = {}
    for token in tokens:
        if token in freq:
            freq[token] +=  1
        else: 
            freq[token]=1

    #We then order them with sorted(), reverse=True puts them in descending order, because we want them from highest to lowest frequency
    ranked_freq = sorted(freq.items(), key=lambda 
                            item: item[1], reverse=True) 
    
    #We print to check out which words have the highest frequency, here we can already check if they are shorter
    print(ranked_freq[:10])
    #We also print out some of the words with the lowest frequency, to check if they are longer
    print(ranked_freq[-10:])

    #However, we might still want to plot them 
    #So we create lists with frequency and word length
    frequency = []
    word_length = []

    for word, count in ranked_freq:
        word_length.append(len(word))
        frequency.append(count) 

    #We plot the frequency in a scatter plot 
    plt.scatter(word_length,frequency)
    plt.xlabel('Word Length')
    plt.ylabel('Frequency')
    plt.title(f'Zipf\'s Law of Abbreviation for {language} Songs')
    plt.show()


#We apply the function to the files in our directories    
zipfslaw_abbreviation(cat_directory, 'Catalan')
print("="*60)
zipfslaw_abbreviation(eng_directory, 'English')


