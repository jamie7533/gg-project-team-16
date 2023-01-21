'''Version 0.35'''

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize





def clean_tweets():
    #currently removes rt @..:, sets all to lower, removes tweets containing bad words that may be misleading
    #removes leading and trailing spaces, removes stopwords including added list, removes all characters not in normal english including '(contractions mess up with stop words needs fix)

    with open("gg2013.json", 'r') as f:
        tweets = json.load(f)
    bad_words = ["didn't", 'wish', 'hope', 'not', "should've", 'hoping']
    tweets_text = [tweet['text'] for tweet in tweets]
    tweets_text = [tweet.lower() for tweet in tweets_text]
    #uncomment to only look at tweets containing wins, runs much quicker
    #tweets_text = [tweet for tweet in tweets_text if any(bad in tweet for bad in [' wins '])]
    tweets_text = [tweet for tweet in tweets_text if not any(bad in tweet for bad in bad_words)]
    for i in range(len(tweets_text)):
        if tweets_text[i].startswith("rt @") and ':' in tweets_text[i]:
            tweets_text[i] = tweets_text[i].split(':', 1)[1]
    tweets_text = [tweet.strip() for tweet in tweets_text]

    my_stopwords = nltk.corpus.stopwords.words('english')
    my_extra = ['gg', 'goldenglobes', 'golden', 'globes', 'globe']
    my_stopwords.extend(my_extra)

    print(my_stopwords)

    for i in range(len(tweets_text)):
        clean_i = re.sub("[^a-z0-9., ]", "", tweets_text[i])
        filtered_words =[]
        token_i = word_tokenize(clean_i)
        for word in token_i:
            if word not in my_stopwords:
                filtered_words.append(word)
        tweets_text[i] = " ".join(filtered_words)

    print(tweets_text[1:5])
    return tweets_text




def find_wins(s):
    match = re.search(r"(\b\w+\s+\w+\b)\s+wins\s+(\b\w+\s+\w+\b)", s)
    if match:
        return [match.group(1), match.group(2)]
    else:
        return None

def match_hosts(str):
    match = re.search(r"host",str)
    if match:
        return str
    else:
        return None

def get_list_of_names():
    name_counts = {}
    file = open('names.txt', mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    names = []
    for line in lines:
        line = line[:-1].lower()
        names.append(line)
        name_counts[line] = 0
        
    return names, name_counts

def top_n_keys(d, n):
    # sort the items by values
    items = sorted(d.items(), key=lambda x: x[1], reverse=True)
    # take the first n items
    top_n = items[:n]
    # extract the keys from the items
    top_n_keys = [item[0] for item in top_n]
    return top_n_keys





def get_hosts(year):
    names,name_counts = get_list_of_names()
    
    f = open('gg2013.json')
    data = json.load(f)
    hosts = []
    for tweet in data:
        match = match_hosts(tweet['text'])
        if(match != None):
            words = tweet['text'].split(' ')
            for word in words:
                if(word.lower() in names):
                    name_counts[word.lower()] += 1
    possible_hosts = top_n_keys(name_counts,10)

    #Now trying to determine how many hosts there actually were
    previous_count = 0
    for i in possible_hosts:
        temp = name_counts[i]
        if(temp < (0.9 * previous_count)):
            return hosts
        else:
            hosts.append(i)
        previous_count = temp
    
    return hosts

                    



        
        

    #'''Hosts is a list of one or more strings. Do NOT change the name
    #of this function or what it returns.'''
    
    
def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def pre_ceremony():
    
    

       

    #'''This function loads/fetches/processes any data your program
    #will use, and stores that data in your DB or in a json, csv, or
    #plain text file. It is the first thing the TA will run when grading.
    #Do NOT change the name of this function or what it returns.'''
    # Your code here
    #print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    tweets = clean_tweets()
    
    print(get_hosts(2013))
    
    
            


    return

if __name__ == '__main__':
    main()
