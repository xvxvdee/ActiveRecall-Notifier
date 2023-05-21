import PyPDF2
import pandas as pd

def format_text():

    reader = PyPDF2.PdfReader('Data/English-French Dictionary by Germain Garand.pdf') # creating a pdf reader object
    page_len=len(reader.pages) # print the number of pages in pdf file
    vocab = {}

    words = [reader.pages[i].extract_text().split("\n") for i in range(page_len) if ":" in reader.pages[i].extract_text()] # all words on pages
    words = sum(words,[]) #flatten list
    words = [k for k in words if "English−french Dictionary" not in k] # Remove page numbers ( ex. English−french Dictionary 9)

    for word in words[2:]: # First two elements are links
        definition = word.split(":")
        english,french = definition[0].strip(),definition[1].strip()
        if "English−french (dictionnaire)" in french: # Removing page title from word
            french = french.replace("English−french (dictionnaire)","")
        vocab[english]=french

    df_vocab=pd.DataFrame({"English":vocab.keys(),"French":vocab.values()})

    return df_vocab
    
#vocabulary = format_text()
#vocabulary.to_csv("Data/vocabulary.csv",index=False)

test= pd.read_csv("Data/vocabulary.csv")
print(test)