import re
import argparse
import json


# Attempts to add 1 to 2D frequency dictionary, if keyerror, then
# create a new dictionary at that spot with key_2:1
def add_or_update_count(dict,key_1,key_2,add_zero=False):
    if add_zero:
        try:
            dict[key_1][key_2] += 0
        except KeyError:
            try:
                dict[key_1].update({key_2:0})
            except KeyError:
                dict[key_1] = {key_2:0}
    else:   
        try:
            dict[key_1][key_2] += 1
        except KeyError:
            try:
                dict[key_1].update({key_2:1})
            except KeyError:
                dict[key_1] = {key_2:1}
        
            
    

# Normalizes values in a key:value dicitonary
def dict_normalize(dict):
    total = sum(dict.values())
    for key in dict:
        dict[key] = dict[key]/total
    return dict


# python hmmlearn.py ./it_isdt_train_tagged.txt
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='/path/to/input')
    args = parser.parse_args()
    
    
    
    training_file = open(args.filepath, "r")
    raw_train = training_file.read()
    line_split = re.split('\n',raw_train)

    tag_ptag_freq = {} # tag given previous tag
    tag_word_freq = {} # probability of tag given word
    init_prob = {} # probability for a tag to appear after the end of a sentence
    
    previous_tag = '!?!' # Special tag for first tag in training set (previous tag is !?!) and only occurs once
    
    unique_words = []
    for line in line_split:
        train_split = re.split('\s',line)
        first_tag = True
        for word_tag in train_split:
            match = re.match('^(.*)\/(.*?)$',word_tag)
            if match:
                word,tag = match.group(1),match.group(2)
                unique_words += word
                # Add count to word_tag frequencies
                add_or_update_count(tag_word_freq,tag,word)
                
                # Add count to tag_previous_tag frequencies
                add_or_update_count(tag_ptag_freq,tag,previous_tag)
                
                if first_tag:
                    try:
                        init_prob[tag] += 1
                    except KeyError:
                        init_prob[tag] = 1
                first_tag = False
                
                previous_tag = tag


    # Save unique words and tags for add 1 smoothing
    unique_words = set(unique_words)
    unique_tags = tag_ptag_freq.keys()
    
    
    
    # Normalize tag_word frequencies first, then add 0
    for tag in tag_word_freq:
        tag_word_freq[tag] = dict_normalize(tag_word_freq[tag])

    # Add zero to tag_word frequencies for all unique words
    # to make distinction between unknown token and 0 prob during training
    for tag in unique_tags:
        for word in unique_words:
            add_or_update_count(tag_word_freq,tag,word,add_zero=True)
    
    # Go through two dictionaries, do add 1 smoothing to transitions and init probabilities
    for tag in unique_tags:
        # Initial probability smoothing
        try:
            init_prob[tag] += 1
        except KeyError:
            init_prob[tag] = 1
        
        # Transition matrix smoothing
        for prev_tag in unique_tags:
            add_or_update_count(tag_ptag_freq,tag,prev_tag) 
    #/NO([\sA-z]*?)/PR counts 2 concurrent tags


    for tag in tag_ptag_freq:
        tag_ptag_freq[tag] = dict_normalize(tag_ptag_freq[tag])

    init_prob = dict_normalize(init_prob)
    
    # Write json 
    with open('hmmmodel.txt','w',encoding='utf8') as outfile:
        json.dump(tag_word_freq, outfile, ensure_ascii=False)
        outfile.write('\n')
        json.dump(tag_ptag_freq, outfile, ensure_ascii=False)
        outfile.write('\n')
        json.dump(init_prob, outfile, ensure_ascii=False)


    print(init_prob)    


