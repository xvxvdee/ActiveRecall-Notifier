import PyPDF2
import pandas as pd

def format_text(): # Formats text from pdf (English:French) and returns it as a dataframe
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
    
vocabulary = format_text()
vocabulary.to_csv("Data/vocabulary.csv",index=False)

# Create csv files to store stats ---------------------

vocabulary_df= pd.read_csv("Data/vocabulary.csv")
# Corrections_stats stores [correct,wrong,attempts]
correction_stats_df = pd.DataFrame({"English":vocabulary_df["English"],"French":vocabulary_df["French"],"Correct":vocabulary_df["English"].size*[0],"Wrong":vocabulary_df["English"].size*[0],"Attempts":vocabulary_df["English"].size*[0]})
correction_stats_df.to_csv("Data/correction_stats.csv",index=False)

# Corrections_stats stores [timestamp, result(1=correct,0=wrong)]
correction_timeline_stats_df = pd.DataFrame({"Timestamp":[],"English":[],"French":[],"Result":[]})
correction_timeline_stats_df.to_csv("Data/timeline_stats.csv",index=False)

#https://www.askpython.com/python-modules/pandas/add-rows-to-dataframe needed for updating dataframe

