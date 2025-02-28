import csv

def generate_input_for_morph_generator(input_data, tam_term, depend_data, sentence_type):
    """Load auxiliary data and process the input for the morph generator."""
    
    morph_input_final_tup = []
    depend_dict = {i + 1: item.split(':')[1] for i, item in enumerate(depend_data)}
    
    # Load auxiliary data from TSV file
    with open("repository/tam_morph_tuple.tsv", 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header row  
        for row in reader:
            if len(row) < 6:
                continue  # Skip incomplete rows
            hindi_tam = row[0].strip()
            tuple_info = row[5].strip()
            if tam_term == hindi_tam:
                moph_tuples = tuple(eval(part) for part in tuple_info.split(';'))
                
    for i, data in enumerate(input_data):
        morph_input_tuple = None  # Reset for each iteration

        person_mapping = {'a': 'p3', 'm_1': 'p2', 'u': 'p1'}
        person = person_mapping.get(data[6], None)
        number = 'sg' if data[5] == 's' else 'pl'
        gender = data[4]

        
            
        if data[2] == 'p' and data[1] == 'this':
            morph_input_tuple = (data[1], 'det', 'dem', number)  
        elif data[2] == 'p' and data[1] == 'that':
            morph_input_tuple = (data[1], 'prn', 'dem', 'mf', number)
        elif data[2] == 'p' and data[0] in depend_dict and depend_dict[data[0]] in ['k2', 'k4']:
            morph_input_tuple = ('prpers', 'prn', 'obj', person, gender, number)
        elif data[2] == 'p':
            morph_input_tuple = ('prpers','prn', 'subj', person, gender, number) 
        elif data[2] == 'n' and data[1] in ['not', 'after', 'before', 'near', 'far']:
            morph_input_tuple = (data[1], 'adv')
        elif data[2] == 'n' and data[7] == 'proper':  
            morph_input_tuple = (data[1], 'np', 'ant', gender, number)   
        elif data[2] == 'n' and data[7] != 'proper':
            morph_input_tuple = (data[1], data[2], number)
        elif (sentence_type[1:] in ['negative', 'interrogative'] and tam_term == 'wA_hE_1'):
            morph_input_tuple = ('do', 'vaux', 'pres')
        
        if morph_input_tuple: 
            morph_input_final_tup.append(morph_input_tuple)

        if data[8] == 'main':
            word = data[1]
            gen = data[4]
            person_mapping = {'a': 'p3', 'm_1': 'p2', 'u': 'p1'}
            per = person_mapping.get(data[5], None)
            num = 'sg' if data[4] == 's' else 'pl'

    if moph_tuples:
        morph_input_final_tup.extend(moph_tuples)  
    
    morph_input_final_tup = [
        tuple(word if item == 'vm' else item for item in tup)
        for tup in morph_input_final_tup
    ]
    morph_input_final_tup = [
        tuple(per if item == 'per' else item for item in tup)
        for tup in morph_input_final_tup
    ]
    morph_input_final_tup = [
        tuple(num if item == 'num' else item for item in tup)
        for tup in morph_input_final_tup
    ]
    
    morph_input_final_tuple = []
    for tup in morph_input_final_tup:
        word = tup[0]
        index = next((data[0] for data in input_data if data[1] == word), None)
        
        if index is not None:
            morph_input_final_tuple.append((index,) + tup)
        else:
            morph_input_final_tuple.append((-1,) + tup)  # Use -1 if no match found

    return morph_input_final_tuple

