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
    
    all_tags = tag_ptag.keys()
    tag_backpointer_matrix = {}
    
    for tag in all_tags:
        tag_backpointer_matrix[tag] = '!?!'
 
    lines = 0
    for line in line_split:
        input_split = re.split('\s',line)
        t = 0
        tag_prob_matrix = [init_prob]
        tag_backpointer_matrix = {}

        for word in input_split:
            t += 1
            this_prob = {}
            for tag in all_tags:
                
                # Check if emission is in the dict
                if word in tag_word[tag]:
                    
                    # If the word has been seen, cut out 90% of 0 emissions
                    if 0 == tag_word[tag][word]:
                        this_prob[tag] = 0
                    else:
                        
                        # State update using max(previous state*transition) * emission (From lecture)
                        this_prob[tag] = max(
                            [tag_prob_matrix[-1][ptag]*tag_ptag[tag][ptag] for ptag in all_tags]) * tag_word[tag][word]
                
                # If it is not in the dictionary, rely on transition probabilities only
                else:
                    print(word + " not in " + tag)
                    this_prob[tag] = max(
                        [tag_prob_matrix[-1][ptag]*tag_ptag[tag][ptag] for ptag in all_tags])
                    
            tag_prob_matrix.append(this_prob)
            
            print(this_prob)
            
            max_tag = max(this_prob,key = this_prob.get)
            print(word + " / " + max_tag)
            
            output = output + word + "/" + max_tag + " "
            #print(word)
            #print(tag_prob_matrix)
            #print(init_prob)
            
            
        output += "\n"
        lines += 1
        if lines > 20:
            break

    for i in tag_prob_matrix:
        print(i)
    print(len(raw_text))
    print(output)

        