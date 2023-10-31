import re
import argparse
import json



# python hmmdecode.py ./it_isdt_dev_raw.txt
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('textpath', help='/path/to/input')
    args = parser.parse_args()
    

    # Load model
    model_path = './hmmmodel.txt'
    model_file = open(model_path, "r")

    raw_model = model_file.readlines()
    
    tag_word = json.loads(raw_model[0])
    tag_ptag = json.loads(raw_model[1])
    init_prob = json.loads(raw_model[2])
    
    # Load input data
    input_file = open(args.textpath, "r")
    raw_text = input_file.read()
    line_split = re.split('\n',raw_text)


    output = ""

    tag_prob_matrix = [init_prob]
    tag_backpointer_matrix = []

    all_tags = tag_ptag.keys()
    

    lines = 0
    for line in line_split:
        # small check for annoying empty line in input
        if len(line) <= 0:
            continue
        input_split = re.split('\s',line)
        t = 0
        tag_prob_matrix = [init_prob]
        tag_backpointer_matrix = []

        for word in input_split:
            t += 1
            this_prob = {}
            this_pointer = {}
            for tag in all_tags:
                
                # Check if emission is in the dict
                if word in tag_word[tag]:
                    
                    # If the word has been seen, cut out 90% of 0 emissions
                    if 0 == tag_word[tag][word]:
                        this_prob[tag] = 0
                        this_pointer[tag] = tag

                    else:
                        emission_prob = [(tag_prob_matrix[-1][ptag]*tag_ptag[tag][ptag],ptag) for ptag in all_tags]
                        # Finds max probability, and the tag that was given to this
                        max_prob,prevtag = max(emission_prob,key=lambda x:x[0])
                        # State update using max(previous state*transition) * emission (From lecture)
                        this_prob[tag] = max_prob * tag_word[tag][word]
                        this_pointer[tag] = prevtag
                
                # If it is not in the dictionary, rely on transition probabilities only
                # Note that there is a difference between seen in training + 0 emissions
                # versus a completely new token
                else:
                    # Similar to above, but attach the tag that gave us the probability
                    emission_prob = [(tag_prob_matrix[-1][ptag]*tag_ptag[tag][ptag],ptag) for ptag in all_tags]              
                    max_prob,prevtag = max(emission_prob,key=lambda x:x[0])
                    this_prob[tag] = max_prob
                    this_pointer[tag] = prevtag

            # tag_prob is a dict of {tag:probabilities}
            # tag_backpointer keeps a record of which tag gave tag_prob its probability {tag:previous tag}
            tag_prob_matrix.append(this_prob)
            tag_backpointer_matrix.append(this_pointer)
            
        # Get the most likely last tag based on max in tag_prob
        last_tag_prob = tag_prob_matrix[-1]
        max_tag = max(last_tag_prob,key = last_tag_prob.get)
        
        # Using the max_prob tag, follow backpointers to recover the most likely chain of tags
        tagged_list = []
        # Backwards pass to attach tags to words
        for word,pointer_dict in zip(reversed(input_split),reversed(tag_backpointer_matrix)):
            
            tagged_list.append(word + "/" + max_tag)
            max_tag = pointer_dict[max_tag]
        # Tagged word list build backwards, so reverse it again
        tagged_list.reverse()
        
        for word_tag in tagged_list:
            output += word_tag + " "
        output += "\n"
        
    
    # Write json 
    with open('hmmoutput.txt','w',encoding='utf8') as outfile:
        outfile.write(output)
        
        
        