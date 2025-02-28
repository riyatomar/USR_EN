import json
import re
# from repository.common_v4 import *
# import updated.repository.constant

spkview_list = ['BI_1', 'samAveSI', 'alAvA', 'awirikwa']
discourse_list = ['samuccaya', 'AvaSyakawApariNAma', 'kAryakAraNa', 'pariNAma', 'viroXIxyowaka', 'vyaBicAra', 
                  'viroXI', 'anyawra', 'samuccaya x', 'arWAwa', 'uwwarkAla', 'kAryaxyowaka', 'uxaharaNasvarUpa']

def clean(word, inplace=''):
    """
    Clean concept words by removing numbers and special characters from it using regex.
    >>> clean("kara_1-yA_1")
    'karayA'
    >>> clean("kara_1")
    'kara'
    >>> clean("padZa_1")
    'pada'
    >>> clean("caDZa_1")
    'caDa'
    """
    # Replace specific patterns
    word = word.replace('dZ', 'd').replace('jZ', 'j').replace('DZ', 'D')
    # Remove numbers and special characters
    return re.sub(r'[^a-zA-Z]+', inplace, word)

def extract_discourse_values(data, segment_id):
    # Initialize a list to store discourse values and a flag for specific data
    discourse_values = []
    # #print(data)
    # Assuming 'data' is a JSON string
    data = json.loads(data)
    sp_data = ''
    # #print('nnnnnnnm')
    # Iterate through each entry in the JSON data
    for entry in data:
        # usr_sub_id = entry.get('usr_id')
        rows = entry.get('tokens', [])
        # #print(discourse_head)
        # Collect discourse values from each row
        for row in rows:
            #print(row)
            discourse_value = row.get('discourse_rel', '')
            discourse_head = row.get('discourse_head', '')
            if discourse_value:
                # #print(discourse_head)
                if segment_id == discourse_head.split('.')[0] and 'coref' not in discourse_value:
                    spkview_value = row.get('speaker_view', '')

                    # Check if specific conditions are met
                    if 'AvaSyakawApariNAma' in discourse_value and 'nahIM' in spkview_value:
                        sp_data = 'nahIM wo'
                        return discourse_value, sp_data
                    
                    # Return default values if conditions are not met
                    
                    return discourse_value, None

    # Return default values if no matching discourse value is found
    
    return None, None

def extract_spkview_values(data, segment_id, POST_PROCESS_OUTPUT):
    # Iterate through each entry in the JSON data
    data = json.loads(data)
    for entry in data:
        usr_sub_id = entry.get('usr_id')
        rows = entry.get('tokens', [])

        # Collect discourse values from each row
        for row in rows:
            discourse_value = row.get('discourse_rel', '')
            discourse_head = row.get('discourse_head', '')
            spkview_value = row.get('speaker_view', '')
            
            if discourse_value:
                # disc_value = discourse_value.split(':')[1]
                if discourse_value in discourse_list and spkview_value in spkview_list:
                    # discourse_id = discourse_value.split('.')[0]
                    if segment_id == discourse_head.split('.')[0]:
                        # Process based on spkview_value
                        if 'BI_1' in spkview_value:
                            POST_PROCESS_OUTPUT = 'nA kevala ' + POST_PROCESS_OUTPUT
                            return POST_PROCESS_OUTPUT

    # Return POST_PROCESS_OUTPUT if no conditions are met
    return POST_PROCESS_OUTPUT

def process_coref(val, index_data,words_info,json_data,discourse_data,coref_list):
    json_data = json.loads(json_data)
    for i in range(len(discourse_data)):
        sub_coref_list=[]
        if 'coref' in discourse_data[i] and '.' in discourse_data[i]:
            discourse_id=discourse_data[i].split('.')[0]
            discourse_head=discourse_data[i].split('.')[1].split(':')[0]
            
            for j, sentence in enumerate(json_data):
                usr_sub_id = sentence.get('usr_id')
                tokens = sentence.get("tokens",[])
                if usr_sub_id == discourse_id:
                    for token in tokens:
                        # #print(discourse_head,'dhhh')
                        ind=token.get('index')
                        if str(ind) == discourse_head:
                            print(token.get('morpho_sem'),'token')
                            sub_coref_list.append(index_data[i])  # Add the index data
                            concpt=token.get('concept')
                            coref_word = clean(concpt)  # Get coref word
                            sub_coref_list.append(coref_word)
                            morpho_sem = token.get('morpho_sem')
                            if morpho_sem:
                                words_info[i] = words_info[i][:3] + (morpho_sem,) + words_info[i][4:]
                            print(words_info[i],'llll')
                            # sub_coref_list.append(morpho_sem)
                            # #print(sub_coref_list,'cpcccc')
                            break

        elif 'coref' in discourse_data[i]:  # No '.' in discourse_head, simpler case
            sub_coref_list.append(index_data[i])
            indx=int(discourse_data[i].split(':')[0])
            for processed_word in words_info:
                if processed_word[0]==indx:  # Check if indx is composed entirely of digits
                    coref_word = clean(processed_word[1])
                    morpho_sem = processed_word[3]
                    if morpho_sem:
                        words_info[i] = words_info[i][:3] + (morpho_sem,) + words_info[i][4:]
                    sub_coref_list.append(coref_word)

                    break

        if sub_coref_list:  # Append to coref_list if there's any coreference info
            coref_list.append(sub_coref_list)
    print(coref_list,'list')
    return coref_list,words_info