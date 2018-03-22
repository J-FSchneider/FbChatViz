import numpy as np
import pandas as pd
import re
import os, os.path

print('The features are created...') 
print('This may take a few seconds.') 

#### Define Util functions #### 
def msg_word_count(x):
    x = str(x)
    x = x.split(" ")
    return(len(x))
        
def question_flag(x):
    x = str(x)
    if '?' in x:
        return 1
    else:
        return 0

def is_in(m,l):
    if m in list(l):
        return 1
    else: 
        return 0
    
def group_conversation(fb_database):
    conv = fb_database.groupby(['conversation_id']).user.nunique()
    idx = conv[conv > 2].index
    fb_database['group_conversation'] = fb_database['conversation_id'].apply(lambda m: is_in(m,idx))
    return fb_database

def sticker_sent(x): 
    x = str(x)
    matchobj = re.search(r'<p><img src="messages/stickers/',x)
    if matchobj: 
        return 1
    else:
        return 0
    
def photo_sent(x):
    x = str(x)
    matchobj = re.match(r'<p><img src="messages/photos/',x)
    if matchobj: 
        return 1
    else:
        return 0
    
"""def reply_time(x)
    pass

def conversation_initiated(x)
    pass

def sentiment(x):
    pass

def no_emojis(x):
    pass

def topic(x):
    pass
    
def image(x): 
    pass

def group_conversation(x):
    pass
"""

#### load the data ####
facebook = pd.read_csv('fb_data.csv', lineterminator='\n')

#### generate features ####

facebook['msg_word_count'] = facebook.text.apply(lambda m: msg_word_count(m))
facebook['question_flag'] = facebook.text.apply(lambda m: question_flag(m))
facebook = group_conversation(facebook)
facebook['photo_sent'] = facebook.text.apply(lambda m: photo_sent(m))
facebook['sticket_sent'] = facebook.text.apply(lambda m: sticker_sent(m))

"""
facebook['group_conversation'] = None
facebook['reply_time'] = facebook.text.apply(lambda m: question_flag(m)) 
facebook['conversation_initiated'] = facebook.text.apply(lambda m: question_flag(m))
facebook['sentiment'] = facebook.text.apply(lambda m: question_flag(m))
facebook['no_emojis'] = facebook.text.apply(lambda m: question_flag(m))
facebook['topic'] = facebook.text.apply(lambda m: question_flag(m))
""" 

#### export data ####

facebook.to_csv('fb_data_features.csv', index=False)

print('Done! -> fb_data_features.csv generated') 