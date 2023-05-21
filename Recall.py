import pandas as pd
import random
import time
import datetime

"""
Active recall notifier:
 - Take in notes similar to quizlet format
 - Quiz user on question (True or False), maybe type in 
 - Show stats (# questions they get right/wrong, when they perform the best, motivation)
"""
class active_recall:

    def __init__(self):
        self.vocab = pd.read_csv("Data/vocabulary.csv")
        self.vocab_len = self.vocab["English"].size
        self.test_word = self.build_question()
        self.word = self.test_word[0]
        self.word_num = self.test_word[3]
        self.answer = self.test_word[1]
        self.options = self.test_word[2]
        self.correction_stats = pd.read_csv("Data/correction_stats.csv")
        self.timeline_stats = pd.read_csv("Data/timeline_stats.csv")
        self.timestamp = datetime.datetime.now()

    def generate_random_number(self):
        return random.randrange(self.vocab_len-1)
    
    def random_word(self): #Select random word
        num = self.generate_random_number()
        return [self.vocab["English"].iloc[num],self.vocab["French"].iloc[num],num]
        # Once there is some stats, choose word based on attempts, correction, and incorrect words

    def build_question(self): 
        answer = self.random_word() # test word, answer
        # Create options for question
        options_num = [answer[2]]
        num = self.generate_random_number()
        count = 0
        while (num !=answer[2]) and (num not in options_num) and (count!=2): #options are not answer and repeated
            options_num.append(num)
            count+=1
            num =  self.generate_random_number()

        options = [self.vocab["French"].iloc[i] for i in options_num]
        random.shuffle(options) # randomize order of options
        return [answer[0],answer[1],options,answer[2]]

    def update_corrections_stats(self,result): # result (0=wrong,1=right,2=error)
        if result == 0: self.correction_stats.loc[self.word_num,"Wrong"]+=1 # update wrong stats
        elif result == 1: self.correction_stats.loc[self.word_num,"Correct"]+=1 # update right stats

        self.correction_stats.loc[self.word_num,"Attempts"]+=1 # update attempts 
        self.correction_stats.to_csv("Data/correction_stats.csv",index=False) # update csv

    def update_timeline_stats(self,english,french,result): # result (0=wrong,1=right,2=error)
        update = pd.DataFrame({"Timestamp":[self.timestamp],"English":[english],"French":[french],"Result":[result]})
        self.timeline_stats=pd.concat([self.timeline_stats, update], axis=0, ignore_index=True) # add results to df
        self.timeline_stats.to_csv("Data/timeline_stats.csv",index=False) # update csv

