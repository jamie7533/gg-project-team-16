'''Version 0.35'''

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas
import ast
import gender_guesser.detector as gender
d = gender.Detector()



#should be good to use with cleaned tweets
# format:
# {award: [[ALL],[SOME],[NONE]]}
AWARDS_1315_KEYWORDS = {
    'cecil b. demille award' : [['award'],['cecil', 'demille'],[]],
    'best motion picture - drama' : [['drama'],['motion', 'picture', 'movie', 'film'],['actor', 'actress']], 
    'best performance by an actress in a motion picture - drama' : [['actress', 'drama'],['motion', 'picture', 'movie', 'film'], ['supporting']],
    'best performance by an actor in a motion picture - drama' : [['actor', 'drama'],['motion', 'picture', 'movie', 'film'], ['supporting']], 
    'best motion picture - comedy or musical' : [['comedy', 'musical'],['motion', 'picture', 'movie', 'film'],['actor', 'actress']], 
    'best performance by an actress in a motion picture - comedy or musical' : [['actress', 'comedy'],['motion', 'picture', 'movie', 'film'], ['supporting', 'television', 'tv']], 
    'best performance by an actor in a motion picture - comedy or musical' : [['actor', 'comedy'],['motion', 'picture', 'movie', 'film'], ['supporting', 'television', 'tv']], 
    'best animated feature film' : [['animated'],['motion', 'picture', 'movie', 'film'],[]], 
    'best foreign language film' : [['foreign', 'language'],['motion', 'picture', 'movie', 'film'],[]], 
    'best performance by an actress in a supporting role in a motion picture' : [['actress', 'supporting'],['motion', 'picture', 'movie', 'film'],[]], 
    'best performance by an actor in a supporting role in a motion picture' : [['actor', 'supporting'],['motion', 'picture', 'movie', 'film'],[]], 
    'best director - motion picture' : [['director'],['motion', 'picture', 'movie', 'film'],[]], 
    'best screenplay - motion picture' : [['screenplay'],['motion', 'picture', 'movie', 'film'],[]], 
    'best original score - motion picture' : [['score'],['motion', 'picture', 'movie', 'film'],[]], 
    'best original song - motion picture' : [['song'],['motion', 'picture', 'movie', 'film'],[]], 
    'best television series - drama' : [['drama'],['television','tv','series'],['actor','actress']], 
    'best performance by an actress in a television series - drama' : [['drama','actress'],['television','tv','series'],['supporting']], 
    'best performance by an actor in a television series - drama' : [['drama','actor'],['television','tv','series'],['supporting']], 
    'best television series - comedy or musical' : [['comedy'],['television','tv','series'],['actor','actress']], 
    'best performance by an actress in a television series - comedy or musical' : [['comedy','actress'],['television','tv','series'],['supporting']], 
    'best performance by an actor in a television series - comedy or musical' : [['comedy','actor'],['television','tv','series'],['supporting']], 
    'best mini-series or motion picture made for television' : [[],['mini','mini-series','limited','motion picture made television', 'movie made television'],['actor','actress','film','feature']], 
    'best performance by an actress in a mini-series or motion picture made for television' : [['actress'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['film','feature']], 
    'best performance by an actor in a mini-series or motion picture made for television' : [['actor'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['film','feature']], 
    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television' : [['actress','supporting'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['film','feature']], 
    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television' : [['actor','supporting'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['film','feature']]}


def aggregate_and_sort(strings):
    # Use Counter to count the occurrences of each string
    count = Counter(strings)
    # Convert the Counter object to a list of tuples
    tuples = list(count.items())
    # Sort the list of tuples by the second element (the number of occurrences) in descending order
    tuples.sort(key=lambda x: x[1], reverse=True)
    return tuples


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

def read_list_file(file):
    array = []
    with open(file) as my_file:
        for line in my_file:
            array.append(line.strip().lower())
    return array
    


#Returns tweet if award found in tweet, else returns None
#Relies on the AWARDS_1315_KEYWORDS format
def award_in_tweet(tweet, award):
    phrases = AWARDS_1315_KEYWORDS[award]
    found = False
    for word in phrases[0]:
        if word not in tweet:
            return None
    for word in phrases[1]:
        if word in tweet:
            found = True
    if found == False:
        return None
    for word in phrases[2]:
        if word in tweet:
            return None
    return tweet

def find_gender(full_name):
    first_name = full_name.split()[0].capitalize()
    gender = d.get_gender(first_name)
    if gender == 'male':
        return 'male'
    elif gender == 'female':
        return 'female'
    else:
        return None
    
#Takes a list of tweets and an award and finds the nominees for the award
def find_nominees(award, tweets):
    actors_list = read_list_file('actors.txt')
    directors_list = read_list_file('directors.txt')
    movie_show_list = read_list_file('movies_and_shows.txt')
    nominees = []
    tweets = [tweet for tweet in tweets if award_in_tweet(tweet, award)]

    if('actor' in award):
        gen = 'male'
    elif('actress' in award):
        gen = 'female'
    else:
        gen = None
    
    if 'actor' in award or 'actress' in award or 'cecil' in award:
        potential_nominees = {}
        for tweet in tweets:
            for name in actors_list:
                if name in tweet:
                    if(gen == None or find_gender(name) == gen):
                        if(name not in potential_nominees):
                            potential_nominees[name] = 1
                        else:
                            potential_nominees[name] += 1    
        nominees = top_n_keys(potential_nominees,7)
        print(nominees)
    elif 'director' in award:
        potential_nominees = {}
        for tweet in tweets:
            for name in directors_list:
                if name in tweet:
                    if(name not in potential_nominees):
                        potential_nominees[name] = 1
                    else:
                        potential_nominees[name] += 1    
        nominees = top_n_keys(potential_nominees,7)
        print(nominees)
    else:
        potential_nominees = {}
        for tweet in tweets:
            for movie in movie_show_list:
                if movie in tweet:
                    if(movie not in potential_nominees):
                        potential_nominees[movie] = 1
                    else:
                        potential_nominees[movie] += 1    
        nominees = top_n_keys(potential_nominees,7)
        print(nominees)
    return nominees

def find_wins(s):
    match = re.search(r"(\b\w+\s+\w+\b)\s+wins\s+(\b\w+\s+\w+\b)", s)
    if match:
        return [match.group(1), match.group(2)]
    else:
        return None


def find_winner(award, tweets):
    actors_list = read_list_file('actors.txt')
    directors_list = read_list_file('directors.txt')
    movie_show_list = read_list_file('movies_and_shows.txt')
    nominees = []
    tweets = [tweet for tweet in tweets if award_in_tweet(tweet, award)]
    tweets = [tweet for tweet in tweets if 'win' in tweet]
    if 'actor' in award or 'actress' in award or 'cecil' in award:
        potential_nominees = {}
        for tweet in tweets:
            for name in actors_list:
                if name in tweet:
                    if(name not in potential_nominees):
                        potential_nominees[name] = 1
                    else:
                        potential_nominees[name] += 1    
        nominees = top_n_keys(potential_nominees,1)
        print(nominees)
    elif 'director' in award:
        potential_nominees = {}
        for tweet in tweets:
            for name in directors_list:
                if name in tweet:
                    if(name not in potential_nominees):
                        potential_nominees[name] = 1
                    else:
                        potential_nominees[name] += 1    
        nominees = top_n_keys(potential_nominees,1)
        print(nominees)
    else:
        potential_nominees = {}
        for tweet in tweets:
            for movie in movie_show_list:
                if movie in tweet:
                    if(movie not in potential_nominees):
                        potential_nominees[movie] = 1
                    else:
                        potential_nominees[movie] += 1    
        nominees = top_n_keys(potential_nominees,1)
        print(nominees)
    return nominees

def find_wins(s):
    match = re.search(r"(\b\w+\s+\w+\b)\s+wins\s+(\b\w+\s+\w+\b)", s)
    if match:
        return [match.group(1), match.group(2)]
    else:
        return None

def find_award(s):
    match = re.search(r"(gets|won|win) the (.\w+(?:\s+\w+){2,5} award)", s)
    if match: return match.group(2)
    if not match: match = re.search(r"award for (Best .*?) goes to", s)
    if not match: match = re.search(r"the (.*?) (award|Award) goes to", s)
    if not match: match = re.search(r"(Best .*)(award|Award)", s)
    return match.group(1) if match else None


def match_hosts(str):
    match = re.search(r"host",str)
    if match:
        return str
    else:
        return None


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
        if(temp < (0.9 * previous_count)):
            return hosts
        else:
            hosts.append(i)
        previous_count = temp
    
    return hosts
                      
    
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
    return aggregate_and_sort(awards)


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


def match_presenter_award(str, award):
    
    if "present" in str:
        phrases = AWARDS_1315_KEYWORDS[award]
        found = False
        for word in phrases[0]:
            if word not in str:
                return None
        found = False
        for word in phrases[1]:
            if word in str:
                found = True
        if found == False:
            return None
        for word in phrases[2]:
            if word in str:
                return None
        return str
    else:
        return None


#https://github.com/noah-alvarado/cs-337-project-1/blob/master/reference.py has good idea for finding more refrences to awards
def get_presenters(award, tweets):
    actors_list = read_list_file('actors.txt')
    tweets = [tweet for tweet in tweets if award_in_tweet(tweet, award)]
    tweets = [tweet for tweet in tweets if 'present' in tweet]
    potential_nominees = {}
    for tweet in tweets:
        for name in actors_list:
            if name in tweet:
                if(name not in potential_nominees):
                    potential_nominees[name] = 1
                else:
                    potential_nominees[name] += 1    
    possible_presenters = top_n_keys(potential_nominees,5)
    previous_count = 0
    presenters = []
    for i in possible_presenters:
        temp = potential_nominees[i]
        if(temp < (0.75 * previous_count)):
            return presenters
        else:
            presenters.append(i)
        previous_count = temp
    print(presenters)
    return presenters
    
        
"""
    names,name_counts = get_list_of_names()
    
    presenters = []
    for tweet in tweets:
        match = match_presenter_award(tweet, award)
        if match:
            words = tweet.split(' ')
            for i in range(len(words) - 1):
                if(words[i] in names):
                    name = words[i].lower() + ' ' + words[i+1].lower()
                    if(name not in name_counts):
                        name_counts[name] = 0
                    else:
                        name_counts[name] += 1
    possible_presenters = top_n_keys(name_counts,5)
    print(possible_presenters)

    #Now trying to determine how many hosts there actually were
    previous_count = 0
    for i in possible_presenters:
        temp = name_counts[i]
        if(temp < (0.75 * previous_count)):
            return presenters
        else:
            presenters.append(i)
        previous_count = temp
    
    return presenters
"""

def pre_ceremony():
    """
    #following creates the 3 txt files from the credits csv file and tvshows csv file
    tvFile = pandas.read_csv('imdb_tvshows.csv')
    csvFile = pandas.read_csv('tmdb_5000_credits.csv')
    movie_list = csvFile["title"].to_list() + tvFile["Title"].to_list()
    casts = csvFile["cast"].to_list()
    crews = csvFile['crew'].to_list()
    actor_list = set()
    director_list = set()
    #print(casts[0][1])
    for cast in casts:
        for char in ast.literal_eval(cast):
            actor_list.add(char["name"])
    for actors in tvFile["Actors"].to_list():

        if type(actors) == str:
            actors = actors.split(',')
            for actor in actors:
                actor_list.add(actor.strip())
    actor_list = list(actor_list)
    for crew in crews:
        for person in ast.literal_eval(crew):
            if person["job"] == "Director":
                director_list.add(person["name"])
    director_list = list(director_list)

    with open('movies_and_shows.txt', 'w') as f:
        for movie in movie_list:
            f.write(f"{movie}\n".encode('utf8').decode('ascii', 'ignore'))

    with open('directors.txt', 'w') as f:
        for director in director_list:
            f.write(f"{director}\n".encode('utf8').decode('ascii', 'ignore'))

    with open('actors.txt', 'w') as f:
        for actor in actor_list:
            f.write(f"{actor}\n".encode('utf8').decode('ascii', 'ignore'))
    """

       

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
    for award in get_awards(2013): print(award)
    #names,name_counts = get_list_of_names()
    #print(names)
    
    

    with open("gg2013.json", 'r') as f:
         tweets = json.load(f)
    tweets = [tweet['text'] for tweet in tweets]
    tweets = [tweet.lower() for tweet in tweets]

    # #tweets = clean_tweets()
    # for award in AWARDS_1315_KEYWORDS.keys():
    #     print(award)
    #     # print('presenters:')
    #     # get_presenters(award, tweets)
    #     # print('nominees')
    #     find_nominees(award, tweets)
        
    #     print(get_presenters(2013,award, tweets))

    # names,name_counts = get_list_of_names()
    # for i in tweets:
    #     words = i.split(' ')
    #     for word in words:
    #         if(word in names):
    #             name_counts[word] += 1
    # for key, value in sorted(name_counts.items(), key=lambda item: item[1], reverse=True):
    #     print(key, value)


if __name__ == '__main__':
    main()
