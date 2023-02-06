# gg-project-master
Golden Globe Project Master

Link to repo: https://github.com/jamie7533/gg-project-team-16

Project Info and Approach:
For the Tweet Mining & The Golden Globes project we tried to extract information about the Golden Globes awards ceremony from a file of tweets. 
Our approach to this was to look for references to different awards in the tweets using equivalence classes for each award. Using these references 
to the awards, we looked for information, specifically the nominees, presenters and the winner of the award. To do this we looked at several key
phrases to further filter the tweets and then searched for names and movie titles from lists created using imdb files. Since these files took 
significant time to create they have been pregenerated and stored as text files which are then referenced. 

Additional Goals:
For our additional goals we wanted to find out more about the red carpet and the experience outside of the ceremony itself.
To do this we looked for four things
* Best dressed: The name of the best dressed person
* Worst dressed: The name of the worst dressed person
* Most talked about: The name of the three most talked about people along with a list of buzzwords from the tweets talking about them
* Most controversial: The name of the most controversial person based on the output of a sentiment analyzer over tweets they were mentioned in terms of average negative sentiment

TA Instructions for Running:
* run main in `gg_api.py`
  * this will run all of the `get_[*](year)` functions as well as our `onLoad()` which cleans the tweets 
  * status updates will be printed, then the complete json object, then the human readable output
* `human_readable(year)` prints all results for the given year formatted in the terminal
* `final_output(year)` returns all results for the given year as a json object