

construction_dict = {}
processed_postpositions_dict = {}


def new_to_old_convert_construction_conj_dis(index_data,construction_data,conj_concept):
    # op_index=[]
    op_sub_ind=[]
    construction_data1=''
    for i, concept in enumerate(conj_concept):
        
        if 'conj' in concept :
            ind=index_data[i]
            for j, text in enumerate(construction_data):
                # if text!='':
                txt=text.split(':')[0]
                if 'op' in text and ind==int(txt):
                        op_sub_ind.append(str(index_data[j]))
        elif 'disjunct' in concept :
            ind=index_data[i]
            for j, text in enumerate(construction_data):
                # if text!='':
                txt=text.split(':')[0]
                if 'op' in text and ind==int(txt):
                        op_sub_ind.append(str(index_data[j]))
    return op_sub_ind


def set_gender_make_plural(processed_words, g, num):
    process_data = []
    # for all k1s and main verb change gender to female and number to plural
    for i in range(len(processed_words)):
        word_list = list(processed_words[i])
        if word_list[2] == 'adj':
            # 4th index - gender, 5th index - number
            word_list[4] = g
            word_list[5] = num
        elif word_list[2] == 'v':
            # 3rd index - gender, 4th index - number
            word_list[3] = g
            word_list[4] = num
        process_data.append(tuple(word_list))
    return process_data

def is_update_index_NC(i, processed_words):
    for data in processed_words:
        temp = tuple(data)
        if len(temp) > 7 and float(i) == temp[0] and temp[7] == 'NC':
            return True
    return False


def fetch_NC_head(i, processed_words):
    for data in processed_words:
        temp = tuple(data)
        if int(temp[0]) == int(i) and temp[7] == 'NC_head':
            return temp[0]
        

def process_construction_cp(relation_head, verbs_data, flag, main_verb):
    """
    Process construction data based on relation_head and verbs_data.
    
    Parameters:
        relation_head (str): The head of the relation being processed.
        verbs_data (list): A list of verbs data, each represented as a list.
        flag (bool): A flag indicating if a matching verb has been found.
        main_verb (list): The main verb object to be updated.
    
    Returns:
        tuple: Updated main_verb and flag.
    """
    # Iterate through the verbs data
    for verb in verbs_data:
        # Check if the verbalizer matches the relation head
        verbalizer_match = f"{relation_head}:verbalizer" == verb[8]
        if verbalizer_match:
            main_verb = verb
            flag = True
            break
        
        # Check if the relation_head matches verb[0] (as an integer)
        if int(relation_head) == verb[0]:
            main_verb = verb
            break
        else:
            main_verb = verb
    
    # If no match is found, return the original main_verb and flag
    return main_verb, flag


def process_construction_spatial(processed_words, construction_data,index_data,flag_spatial):
    # construction_dict.clear()
    process_data = processed_words
    # dep_gender_dict = {}
    a = 'after'
    b = 'before'
    for i,cons in enumerate(construction_data):
        if 'whole' in cons in construction_data[i]:
            start_idx = index_data[i]
            # temp = (b, 'prawyeka')
            # del processed_postpositions_dict[index_data[i]]
            temp = (a, 'meM')
            if float(start_idx) in construction_dict:
                construction_dict[float(start_idx)].append(temp)
                flag_spatial=False
            else:
                construction_dict[float(start_idx)] = [temp]
        if float(index_data[i]) in processed_postpositions_dict:
            del processed_postpositions_dict[float(index_data[i])]
            
    return process_data,flag_spatial

def process_construction_xvanxva(processed_words, construction_data,index_data,flag_xvanxva):
    # construction_dict.clear()
    process_data = processed_words
    # dep_gender_dict = {}
    a = 'after'
    b = 'before'
    for i,cons in enumerate(construction_data):
        if 'op' in cons in construction_data[i]:
            start_idx = index_data[i]
            # temp = (b, 'prawyeka')
            # del processed_postpositions_dict[index_data[i]]
            temp = (a, '-')
            if float(start_idx) in construction_dict:
                construction_dict[float(start_idx)].append(temp)
                flag_xvanxva=False
            else:
                construction_dict[float(start_idx)] = [temp]
                flag_xvanxva=False
            break
        if float(index_data[i]) in processed_postpositions_dict:
            del processed_postpositions_dict[float(index_data[i])]

    return process_data,flag_xvanxva


def process_construction_conj_disjunct(processed_words, root_words,construction_data1, depend_data, gnp_data, index_data,conj_concept,flag_conj,flag_disjunct):
    # Adding Ora or yA as a tuple to be sent to morph/ adding it at join_compounds only
    # if k1 in conj, all k1s and main verb g - m and n - pl
    # if all k1 male or mix - k1s g - male else g - f
    # cons list - can be more than one conj
    # k1 ka m/f/mix nikalkr k1s and verb ko g milega    index dep:gen
    # map to hold conj kaha aega
    # construction_dict.clear()
    process_data = processed_words
    dep_gender_dict = {}
    a = 'after'
    b = 'before'
    if gnp_data != []:
        gender = []
        for i in range(len(gnp_data)):
            gnp_info = gnp_data[i]
            gnp_info = gnp_info.strip().strip('][')
            gnp = gnp_info.split(' ')
            gender.append(gnp[0])

    if depend_data != []:
        dependency = []
        for dep in depend_data:
            if dep != '':
                dep_val = dep.strip().split(':')[1]
                dependency.append(dep_val)
    index=new_to_old_convert_construction_conj_dis(index_data,construction_data1,conj_concept)
    # ##print(construction_data,'conda')
    for i, dep, g in zip(index_data, dependency, gender):
        dep_gender_dict[str(i)] = dep + ':' + g
    
    # ##print(construction_data,'cccd')
    # if construction_data != '*nil' and len(construction_data) > 0:
    # construction = construction_data1.strip().split(' ')
    for cons in root_words:
        # conj_type = cons.split(':')[0].strip().lower()
        # index = cons.split('@')[1].strip().strip('][').split(',') if '@' in cons else cons.strip().strip('][').split(',')
        # index = cons.split(':')[1].strip().strip('][').split(',')
        # ##print(index)
        length_index = len(index)
        if 'conj' in cons or 'disjunct' in cons:
            cnt_m = 0
            cnt_f = 0
            PROCESS = False
            for i in index:
                # ##print(index,'index',dep_gender_dict)
                relation = dep_gender_dict[i]
                dep = relation.split(':')[0]
                gen = relation.split(':')[1]

                if dep == 'k1':
                    PROCESS = True
                    if gen == 'm':
                        cnt_m = cnt_m + 1
                    elif gen == 'f':
                        cnt_f = cnt_f + 1

            if PROCESS:
                if cnt_f == length_index:
                    g = 'f'
                    num = 'p'
                else:
                    g = 'm'
                    num = 'p'
                process_data = set_gender_make_plural(processed_words, g, num)

            update_index = index[length_index - 2]
            # check if update index is NC
            #if true then go till NC_head index update same index in construction dict and remove ppost if any from processed
            for i in index:
                if i == update_index:
                    if is_update_index_NC(i, processed_words):
                        index_NC_head = fetch_NC_head(i, processed_words)
                        i = index_NC_head
                        
                    if 'conj' in cons:
                        flag_conj=False
                        temp = (a, 'Ora')
                        # ##print(temp,'varsk')
                    elif 'disjunct' in cons:
                        flag_disjunct=False
                        temp = (a, 'yA')
                    break
                else:
                    temp = (a, ',')
                    if float(i) in construction_dict:
                        construction_dict[float(i)].append(temp)
                    else:
                        construction_dict[float(i)] = [temp]

                    # if i in ppost_dict remove ppost rAma kA Ora SAma kA -> rAma Ora SAma kA
                    if float(i) in processed_postpositions_dict:
                        del processed_postpositions_dict[float(i)]

            if float(i) in construction_dict:
                construction_dict[float(i)].append(temp)
            else:
                construction_dict[float(i)] = [temp]

            if float(i) in processed_postpositions_dict:
                del processed_postpositions_dict[float(i)]

        elif cons == 'list':
            length_list = len(index)
            for i in range(len(index)):
                if i == length_list - 1:
                    break

                if i == 0:
                    temp = (b, 'jEse')
                    if index[i] in construction_dict:
                        construction_dict[index[i]].append(temp)
                    else:
                        construction_dict[index[i]] = [temp]
                    temp = (a, ',')

                elif i < length_list - 1:
                    temp = (a, ',')

                if index[i] in construction_dict:
                    construction_dict[index[i]].append(temp)
                else:
                    construction_dict[index[i]] = [temp]
    # ##print('process_construction : ',construction_dict)
    return process_data,flag_conj,flag_disjunct

def process_construction_span(processed_words, construction_data,index_data,flag_span):
    # construction_dict.clear()
    process_data = processed_words
    dep_gender_dict = {}
    a = 'after'
    b = 'before'
    # construction_data=new_to_old_convert_construction_span(index_data,construction_data1,span_concept)
    # if construction_data != '*nil' and len(construction_data) > 0:
    # construction = construction_data.strip().split(' ')
    for i,cons in enumerate(construction_data):
        # conj_type = cons.split(':')[0].strip().lower()
        # index = cons.split(':')[1].strip(' ').strip().strip('][').split(',')
        # length_index = len(index)
        if 'start' in cons:
            start_idx = index_data[i]
            # ##print(processed_postpositions_dict)
            temp = (a, 'se')
            # del processed_postpositions_dict[index_data[i]]
            if float(start_idx) in construction_dict:
                construction_dict[float(start_idx)].append(temp)
                flag_span=False
            else:
                construction_dict[float(start_idx)] = [temp]
            if float(start_idx) in processed_postpositions_dict:
                del processed_postpositions_dict[float(i)]

        elif 'end' in cons:
            end_idx = index_data[i]
            temp = (a, 'waka')
            # del processed_postpositions_dict[index_data[i]]
            if float(end_idx) in construction_dict:
                construction_dict[float(end_idx)].append(temp)
                flag_span=False
            else:
                construction_dict[float(end_idx)] = [temp]
            if float(end_idx) in processed_postpositions_dict:
                del processed_postpositions_dict[float(i)]
    return process_data,flag_span

def process_construction_rate(processed_words, construction_data,index_data,flag_rate):
    # construction_dict.clear()
    process_data = processed_words
    # dep_gender_dict = {}
    a = 'after'
    b = 'before'
    for i,cons in enumerate(construction_data):
        if 'count' in cons and 'per_unit' in construction_data[i+1]:
            start_idx = index_data[i]
            temp = (b, 'prawyeka')
            if float(start_idx) in construction_dict:
                construction_dict[float(start_idx)].append(temp)
                flag_rate=False
            else:
                construction_dict[float(start_idx)] = [temp]
        if float(index_data[i]) in processed_postpositions_dict:
            del processed_postpositions_dict[float(index_data[i])]
            
    return process_data,flag_rate
