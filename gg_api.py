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
    # Creating a set of bad words for faster lookup
    bad_words = {"didn't", 'wish', 'hope', 'not', "should've", 'hoping'}
    tweets_text = [tweet['text'] for tweet in tweets]
    tweets_text = [tweet.lower() for tweet in tweets_text]
    # Using list comprehension and `any` function to check for bad words
    tweets_text = [tweet for tweet in tweets_text if not any(bad in tweet for bad in bad_words)]
    # Using list comprehension and `str.startswith()` and `str.split()` method for faster string manipulation
    tweets_text = [tweet.split(':', 1)[1] for tweet in tweets_text if tweet.startswith("rt @") and ':' in tweet]
    tweets_text = [tweet.strip() for tweet in tweets_text]

    # Creating a set of stop words for faster lookup
    my_stopwords = set(stopwords.words('english'))
    my_extra = {'gg', 'goldenglobes', 'golden', 'globes', 'globe'}
    my_stopwords.update(my_extra)

    # Using list comprehension and `re.sub()` function for faster string manipulation
    tweets_text = [re.sub("[^a-z0-9., ]", "", tweet) for tweet in tweets_text]
    # Using list comprehension and `word_tokenize()` function for faster tokenization
    tweets_text = [" ".join(word for word in word_tokenize(tweet) if word not in my_stopwords) for tweet in tweets_text]
    return tweets_text




def find_wins(s):
    match = re.search(r"(\b\w+\s+\w+\b)\s+wins\s+(\b\w+\s+\w+\b)", s)
    if match:
        return [match.group(1), match.group(2)]
    else:
        return None

def find_award(s):
    match = re.search(r"award for (Best .*?) goes to", s)
    if not match: match = re.search(r"the (.*?) (award|Award) goes to", s)
    if not match: match = re.search(r"(Best .*)(award|Award)", s)
    return match.group(1) if match else None

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


def filter_hosts(strings):
    pattern = r"next year"
    filtered_strings = []
    for string in strings:
        match = re.search(pattern, string)
        if not match:
            filtered_strings.append(string)
    return filtered_strings



def get_hosts(year):
    names,name_counts = get_list_of_names()
    tweets = clean_tweets()
    tweets = filter_hosts(tweets)
    
    
    
    hosts = []
    for tweet in tweets:
        match = match_hosts(tweet)
        if(match != None):
            words = tweet.split(' ')
            for i in range(len(words) - 1):
                if(words[i].lower() in names):
                    name = words[i].lower() + ' ' + words[i+1].lower()
                    if(name not in name_counts):
                        name_counts[name] = 0
                    else:
                        name_counts[name] += 1
    possible_hosts = top_n_keys(name_counts,5)
    print(possible_hosts)

    #Now trying to determine how many hosts there actually were
    previous_count = 0
    for i in possible_hosts:
        temp = name_counts[i]
        if(temp < (0.75 * previous_count)):
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
    awards = []
    f = open('gg{0}.json'.format(year))
    data = json.load(f)
    for i in data:
        award = find_award(i['text'])
        if(award != None):
            awards.append(award)
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

    #tweets = clean_tweets()
    
    #print(get_hosts(2013))
    print(get_awards(2013))

    return

if __name__ == '__main__':
    main()
