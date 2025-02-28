
def generate_input_for_morph_generator(input_data):
    # print('input_data_for_morph---->', input_data)
    """Process the input and generate the input for morph generator"""
    morph_input_final_tuple = []
    morph_input_format = []
    morph_input_tuple = None
    morph_input_vtuple = None
    
    for i, data in enumerate(input_data):
        if i > 0:
            prev_data = input_data[i - 1]
        else:
            prev_data = None  
        if i < len(input_data) - 1:
            next_data = input_data[i + 1] 
        else:
            next_data = None

        if data[5] == 's':
            number = 'sg'
        if data[5] == 'p':
            number = 'pl'
        if data[6] == 'a':
            person = 'p3'
        if data[6] == 'm_1':
            person = 'p2'
        if data[6] == 'u':
            person = 'p1'


        if data[2] == 'p':
            continue     
        elif data[2] == 'n' and data[7] == 'proper':  
            morph_input_tuple = (data[0], data[1], 'np', 'ant', data[4], number)     
        elif data[2] == 'n' and data[7] != 'proper':
            morph_input_tuple = (data[0], data[1], data[2], number)
        
        elif data[2] == 'v' and data[8] == 'main' and data[6] != '0' and not next_data or (next_data and len(next_data) > 8 and next_data[8] != 'auxiliary'):
            if data[6] == 'pres':
                morph_input_tuple = (data[0], 'be', 'vblex', 'pres', person, number) 
            if data[6] == 'past':
                morph_input_tuple = (data[0], 'be', 'vblex', 'past', person, number)
            if data[6] == 'gA':
                morph_input_tuple = (data[0], 'will', 'vbmod', 'pres')
                morph_input_vtuple = (f'{data[0]}.1', data[1], 'vblex', 'inf')
            if data[6] == 'yA':
                morph_input_tuple = (data[0], data[1], 'vblex', 'past')

        # elif data[2] == 'v' and data[8] == 'main' and data[6] == '0' and next_data[1] == 'raha' and str(data[0]) == str(next_data[0]).split('.')[0]: 
        #     morph_input_tuple = (data[1], 'vblex', 'pprs')
        # elif data[1] == 'hE' and data[2] == 'v' and data[8] == 'auxiliary' and prev_data[1] == 'raha' and str(data[0]).split('.')[0] == str(prev_data[0]).split('.')[0]: 
        #     morph_input_tuple = ('be', 'vaux', 'pres', person, number)
        # elif data[1] == 'WA' and data[2] == 'v' and data[8] == 'auxiliary' and prev_data[1] == 'raha' and str(data[0]).split('.')[0] == str(prev_data[0]).split('.')[0]: 
        #     morph_input_tuple = ('be', 'vaux', 'past', person, number)
        # elif data[8] == 'auxiliary' and data[1] == 'raha' and prev_data[6] == '0':
        #     morph_input_tuple = ''
        else:
            morph_input_tuple = (data[0], data[1])

        # morph_input_final_tuple.append(morph_input_tuple)
        if morph_input_tuple:
            morph_input_final_tuple.append(morph_input_tuple)
        if morph_input_vtuple:  # Append only if it exists
            morph_input_final_tuple.append(morph_input_vtuple)
    print("# morph_input_final_tuple =================>>", morph_input_final_tuple)

    return morph_input_final_tuple

 




