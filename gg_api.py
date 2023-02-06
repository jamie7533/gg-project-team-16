'''Version 0.35'''

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
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
    'best mini-series or motion picture made for television' : [['best'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['actor','actress','film','feature']], 
    'best performance by an actress in a mini-series or motion picture made for television' : [['actress'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['film','feature']], 
    'best performance by an actor in a mini-series or motion picture made for television' : [['actor'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['film','feature']], 
    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television' : [['actress','supporting'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['film','feature']], 
    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television' : [['actor','supporting'],['mini','mini-series','limited','motion picture made television', 'movie made television'],['film','feature']]}

def award_aggregation(awards):
    awards_dict = {}
    clean_awards = set()
    for award in awards:
        if award in awards_dict:
            awards_dict[award] += 1
        else:
            awards_dict[award] = 1
    for award in awards_dict.keys():
        for other_award in awards_dict.keys():
            if award != other_award and award in other_award:
                awards_dict[award] = 0
                awards_dict[other_award] += 1
    for key, value in awards_dict.items():
        if value > 1:
            clean_awards.add(key)
    award_list = set()
    for i in clean_awards:
        award_words = i.split(" ")
        if len(award_words[-1]) < 4:
            award_words.pop()
        if len(award_words) > 2:
            award = " ".join(award_words)
            award_list.add(award)
    return list(award_list)

#very cleaned tweets, only use if looking for easy to find things
def clean_tweets(year):
    #currently removes rt @..:, sets all to lower, removes tweets containing bad words that may be misleading
    #removes leading and trailing spaces, removes stopwords including added list, removes all characters not in normal english including '(contractions mess up with stop words needs fix)

    with open("gg{0}.json".format(year), 'r') as f:
        tweets = json.load(f)
    bad_words = {"didn't", 'wish', 'hope', 'not', "should've", 'hoping'}
    tweets_text = [tweet['text'] for tweet in tweets]
    tweets_text = [tweet.lower() for tweet in tweets_text]
    tweets_text = [tweet for tweet in tweets_text if not any(bad in tweet for bad in bad_words)]
    tweets_text = [tweet for tweet in tweets_text if not tweet.startswith("rt @") and ':' in tweet]
    tweets_text = [tweet.strip() for tweet in tweets_text]

    my_stopwords = set(stopwords.words('english'))
    my_extra = {'gg', 'goldenglobes', 'golden', 'globes', 'globe'}
    my_stopwords.update(my_extra)
    tweets_text = [re.sub("[^a-z0-9., ]", "", tweet) for tweet in tweets_text]
    tweets_text = [" ".join(word for word in word_tokenize(tweet) if word not in my_stopwords) for tweet in tweets_text]
    return tweets_text


#only text and lowercase, better to use for cases where all info is needed (nominees)
def tweets_lower(year):
    with open("gg{0}.json".format(year), 'r') as f:
        tweets = json.load(f)
    tweets_text = [tweet['text'] for tweet in tweets]
    tweets_text = [tweet.lower() for tweet in tweets_text]
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
        nominees = top_n_keys(potential_nominees,5)
    elif 'director' in award:
        potential_nominees = {}
        for tweet in tweets:
            for name in directors_list:
                if name in tweet:
                    if(name not in potential_nominees):
                        potential_nominees[name] = 1
                    else:
                        potential_nominees[name] += 1    
        nominees = top_n_keys(potential_nominees,5)
    else:
        potential_nominees = {}
        for tweet in tweets:
            for movie in movie_show_list:
                if movie in tweet:
                    if(movie not in potential_nominees):
                        potential_nominees[movie] = 1
                    else:
                        potential_nominees[movie] += 1    
        nominees = top_n_keys(potential_nominees,5)
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
    winners = []
    tweets = [tweet for tweet in tweets if award_in_tweet(tweet, award)]
    tweets = [tweet for tweet in tweets if 'win' in tweet]
    if 'actor' in award or 'actress' in award or 'cecil' in award:
        potential_winners = {}
        for tweet in tweets:
            for name in actors_list:
                if name in tweet:
                    if(name not in potential_winners):
                        potential_winners[name] = 1
                    else:
                        potential_winners[name] += 1    
        winners = top_n_keys(potential_winners,1)
    elif 'director' in award:
        potential_winners = {}
        for tweet in tweets:
            for name in directors_list:
                if name in tweet:
                    if(name not in potential_winners):
                        potential_winners[name] = 1
                    else:
                        potential_winners[name] += 1    
        winners = top_n_keys(potential_winners,1)
    else:
        potential_winners = {}
        for tweet in tweets:
            for movie in movie_show_list:
                if movie in tweet:
                    if(movie not in potential_winners):
                        potential_winners[movie] = 1
                    else:
                        potential_winners[movie] += 1    
        winners = top_n_keys(potential_winners,1)
    return winners


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


def find_presenters(award, tweets):
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
    return presenters


def get_hosts(year):
    names,name_counts = get_list_of_names()
    tweets = cleaned_tweets[year]
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

    #Now trying to determine how many hosts there actually were
    previous_count = 0
    for i in possible_hosts:

        temp = name_counts[i]
        if(temp < (0.55 * previous_count)):
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
    names, count = get_list_of_names()
    f = open('gg{0}.json'.format(year))
    data = json.load(f)
    for i in data:
        award = find_award(i['text'])
        acceptable = award and len(award.split()) > 1 and ("Best" in award or "award" in award) 
        dividers = [" for ", " but ", " goes to ", " is ", " at ", " and ", " to ", " should ", ":", ".", "|", "!", "...", "--"]
        if(acceptable):
            award = award.lower()
            for div in dividers:
                award = award.split(div)[0]
            award_words = award.split(" ")
            for word in award_words:
                if word in names:
                    award = award.split(word)[0]
                    break
            award_words = award.split(" ")
            award = " ".join(word for word in award_words if "#" not in word and "@" not in word)
            award = re.sub("[^a-zA-Z-, ]", "", award)
            award = award.strip()
            award = award.split("golden globe")[0]
            
            if len(award.split()) > 1: awards.append(award)

    award_counts = award_aggregation(awards)
    return award_counts 




def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    nominees = {}

    # if year == 2013
    awards_list = AWARDS_1315_KEYWORDS  # still need to make one for the other year?

    tweets = low_tweets[year]
    for award in awards_list.keys():
        nominees[award] = find_nominees(award, tweets)
    return nominees


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners = {}

    # if year == 2013
    awards_list = AWARDS_1315_KEYWORDS  # still need to make one for the other year?

    tweets = low_tweets[year]
    for award in awards_list.keys():
        winners[award] = find_winner(award, tweets)
    return winners


def get_presenters(year):
    presenters = {}

    # if year == 2013
    awards_list = AWARDS_1315_KEYWORDS  # still need to make one for the other year?

    tweets = low_tweets[year]
    for award in awards_list.keys():
        presenters[award] = find_presenters(award, tweets)
    return presenters




#returns the best dressed person
def best_dressed(year):
    person_list = involved_people[year]
    mentions = {}
    tweets = cleaned_tweets[year]
    tweets = [tweet for tweet in tweets if 'dress' in tweet]
    filtered_tweets = []
    praise = ["amazing", "beautiful", "wow", "love", "gorgeous", "perfect", "killing", "amazing", "spectacular", "banging", "best"]
    for tweet in tweets:
        for word in praise:
            if word in tweet:
                filtered_tweets.append(tweet)
                break   
    for tweet in filtered_tweets:
        for name in person_list:
            if name in tweet:
                if(name not in mentions):
                    mentions[name] = 1
                else:
                    mentions[name] += 1 
    return top_n_keys(mentions,1)


#returns the worst dressed person
def worst_dressed(year):
    person_list = involved_people[year]
    mentions = {}
    tweets = low_tweets[year]
    tweets = [tweet for tweet in tweets if 'dress' in tweet]
    filtered_tweets = []
    bad = ["weird", "aint", "not", "bad", "ugly", "didn't", "couldn't", 'worst']
    for tweet in tweets:
        for word in bad:
            if word in tweet:
                filtered_tweets.append(tweet)
                break   
    for tweet in filtered_tweets:
        for name in person_list:
            if name in tweet:
                if(name not in mentions):
                    mentions[name] = 1
                else:
                    mentions[name] += 1 
    return top_n_keys(mentions,1)


#doesn't run in reasonable time need to feed in short list of names (nominees + hosts + presenters)?
#returns the most talked about people, and the 5 most common words in tweets about them, ordered and filtered for stopwords
def talked_about(year):
    person_list = involved_people[year]
    tweets = low_tweets[year]
    clean_tweets = cleaned_tweets[year]
    ret_dict = {}
    mentions = {}
    for tweet in tweets:
        for name in person_list:
            if name in tweet:
                if(name not in mentions):
                    mentions[name] = 1
                else:
                    mentions[name] += 1 
    people = top_n_keys(mentions,3)
    for person in people:
        top_words = {}
        in_tweets = [tweet for tweet in clean_tweets if person in tweet]
        in_tweets = [re.sub("[^a-z ]", "", tweet) for tweet in in_tweets]
        
        in_tweets = [re.sub(person, "", tweet) for tweet in in_tweets]
        for tweet in in_tweets:
            for word in tweet.split(" "):
                if(len(word) > 3):
                    if(word not in top_words):
                        top_words[word] = 1
                    else:
                        top_words[word] += 1
        ret_dict[person] = top_n_keys(top_words, 10)
    return ret_dict

#doesn't run in reasonable time need to feed in short list of names (nominees + hosts + presenters)?
#returns the most controversial person by looking at sentiment analysis
def most_controversial(year):
    sa = SentimentIntensityAnalyzer()
    person_list = involved_people[year]
    tweets = low_tweets[year]
    ret_dict = {}
    mentions = {}
    people_tweet = {}
    for tweet in tweets:
        for name in person_list:
            if name in tweet:
                if(name not in mentions):
                    people_tweet[name] = [tweet]
                    mentions[name] = 1
                else:
                    people_tweet[name].append(tweet)
                    mentions[name] += 1 
    people = top_n_keys(mentions,20)
    for person in people:
        ret_dict[person] = 0
        for tweet in people_tweet[person]:
            ret_dict[person] += sa.polarity_scores(tweet)['neg']
        for p in ret_dict.keys():
            ret_dict[p] = ret_dict[p] / len(people_tweet[p])
    return top_n_keys(ret_dict, 1)


def pre_ceremony():
    """
    #following creates the base for the 3 txt files from the credits csv file and tvshows csv file. 
    #They were cleaned further for removal of short entries and to ensure winners were present within the lists. Some foreign films were not covered.
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


def onLoad():
    global cleaned_tweets, low_tweets
    cleaned_tweets = {2013: clean_tweets(2013), 2015: clean_tweets(2015)}
    low_tweets = {2013: tweets_lower(2013), 2015: tweets_lower(2015)}
    

# https://github.com/rromo12/EECS-337-Golden-Globes-Team-9/blob/master/gg_api.py
# reference the above repo for a nice main function that waits for input
def main():
    global involved_people
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''

    onLoad()  # to clean tweets only once
    
    awards = get_awards(2013)
    print("awards extracted")
    hosts = get_hosts(2013)
    print("hosts extracted")
    presenters = get_presenters(2013)
    print("presenters extracted")
    nominees = get_nominees(2013)
    print('nominees extracted')
    winners = get_winner(2013)
    print('winners extracted')
    
    involved_people = {2013: set(), 2015: set()}
    for i in hosts:
        involved_people[2013].add(i)
    for award in presenters.keys():
        pr = presenters[award]
        for i in pr:
            involved_people[2013].add(i)
        if 'actor' in award or 'actress' in award or 'cecil' in award or 'director' in award:
            nom = nominees[award]
            for i in nom:
                involved_people[2013].add(i)
            win = winners[award]
            involved_people[2013].add(win[0])
    involved_people[2015] = involved_people[2013]
    
    bDressed = best_dressed(2013)
    wDressed = worst_dressed(2013)
    print("found best and worst dressed")
    talked = talked_about(2013)
    controversial = most_controversial(2013)
    print("found most talked about and controversial")
    
    def human_readable(year):
        print("Host(s): {0}\n\n".format(hosts))
        print("List of mined awards: {0}\n\n".format(awards))
        for award in OFFICIAL_AWARDS_1315:
            print("Award: {0}".format(award))
            print("Presenters: {0}".format(presenters[award]))
            print("Nominees: {0}".format(nominees[award]))
            print("Winner: {0}\n\n".format(winners[award]))
        
        print("Best Dressed: {0}\n".format(bDressed[0]))
        print("Worst Dressed: {0}\n".format(wDressed[0]))
        print("Most Talked About:\n")
        for key, value in talked.items():
            print("{0}, buzzwords: {1}\n".format(key, value))
        print("Most Controversial: {0}".format(controversial[0]))


    def final_output(year):
        json_output = {}
        for award in OFFICIAL_AWARDS_1315:
            json_output[award] = {"Presenters": presenters[award], 
                                  "Nominees": nominees[award],
                                  "Winner":  winners[award]}
        json_output["Hosts"] = hosts
        return json.dumps(json_output)

    #final_output(year) returns a json object of the results
    print()
    print("json output:")
    print(final_output(2013))
    #human_readable prints the results 
    human_readable(2013)


if __name__ == '__main__':
    main()
