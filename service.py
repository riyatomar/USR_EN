import sys
# from repository.common import *
from repository.common_v4 import *
from repository.USR_to_JSON import USR_to_json
from repository.extract_json2 import *
import json
from repository.constant import *
# from my_masking_model import *
# from repository.generateTupleForMorph import *
from repository.extractTupleInfo import *
from map_concept import process_input



# Main function that handles the core processing logic
def process_file_data(input_data,segment_id,json_output):
    global HAS_CONSTRUCTION_DATA, HAS_SPKVIEW_DATA, HAS_MORPHO_SEMANTIC_DATA, HAS_DISCOURSE_DATA, HAS_COREF
    global flag_conj, flag_disjunct, flag_span, flag_cp, flag_meas, flag_rate, flag_spatial, flag_waw, flag_cal, flag_xvanxva, flag_temporal, k1_not_need, has_changes

    # Initialize flags and output data list
    output_data_list = []
    coref_list=[]
    pass_list=['pass-affirmative','pass-interrogative','pass-negative']
    
    try:
        reset_global_dicts()
        rules_info = generate_rulesinfo(input_data) #Extracting Rules from each row of USR
        
        # Extracting Information
        src_sentence = rules_info[0]
        root_words = rules_info[1]
        index_data = [int(x) for x in rules_info[2]]
        seman_data = rules_info[3]
        gnp_data = rules_info[4]
        depend_data = rules_info[5]
        print('depend_data=================>>>>>', depend_data)
        discourse_data = rules_info[6]
        spkview_data = rules_info[7]
        scope_data = rules_info[8]
        construction_data = rules_info[9]
        sentence_type = rules_info[10]

        if sentence_type[1:] in pass_list:
            k1_not_need=True
        
        # check_main_verb(depend_data)
        try:
            has_main_verb = check_main_verb(depend_data)
            if not has_main_verb:
                raise Exception("Main verb is missing in the dependency data")
        except Exception as e:
            return str(e).splitlines()[-1]
        # depend_data,flag_conj,flag_disjunct,flag_span,flag_cp,flag_meas,flag_rate,flag_waw,flag_cal,flag_spatial,flag_xvanxva,flag_temporal = identify_constructions(root_words,index_data,depend_data,spkview_data,construction_data)
        for i, concept in enumerate(root_words):
            if 'conj' in concept :
                flag_conj=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row(i,construction_data,depend_data,index_data)
                # del(gnp_data[i])
            elif 'disjunct' in concept :
                flag_disjunct=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row(i,construction_data,depend_data,index_data)
                # del(gnp_data[i])
            elif 'span' in concept :
                flag_span=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_span(i,construction_data,depend_data,index_data)
                # del(gnp_data[i])
            elif 'cp' in concept:
                flag_cp=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_cp(i,construction_data,depend_data,index_data,spkview_data)
            elif 'meas' in concept:
                flag_meas=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_meas(i,construction_data,depend_data,index_data)
                # del(gnp_data[i])
            elif 'rate' in concept:
                flag_rate=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_meas(i,construction_data,depend_data,index_data)
            elif 'waw' in concept:
                flag_waw=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_waw(i,construction_data,depend_data,index_data)
            elif clean(concept) in ('compound','waw'):
                flag_waw=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_waw(i,construction_data,depend_data,index_data)
            elif 'calender' in concept:
                flag_cal=True
                HAS_CONSTRUCTION_DATA = True
                depend_data=construction_row_calender(i,construction_data,depend_data,index_data)
            elif 'spatial' in concept:
                flag_spatial=True
                HAS_CONSTRUCTION_DATA = True
                depend_data= construction_row_spatial(i,construction_data,depend_data,index_data)
            elif 'xvanxva' in concept:
                flag_xvanxva=True
                HAS_CONSTRUCTION_DATA = True
                depend_data= construction_row(i,construction_data,depend_data,index_data)
            elif 'temporal' in concept:
                flag_temporal=True
                HAS_CONSTRUCTION_DATA = True
                depend_data= construction_row_temporal(i,construction_data,depend_data,index_data)
                flag_span=True
                
        if spkview_data != [] or len(spkview_data) > 0:
            HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data,discourse_data,index_data)
        if discourse_data != [] or len(discourse_data) > 0:
            HAS_DISCOURSE_DATA = True
        if any('coref' in item for item in discourse_data):
            HAS_COREF = True

        # Making a collection of words and its rules as a list of tuples.
        words_info = generate_wordinfo(root_words, index_data, seman_data,
                                    gnp_data, depend_data, discourse_data, spkview_data,scope_data,construction_data)
                                           
        # Categorising words as Nouns/Pronouns/Adjectives/..etc.
        if HAS_COREF:
            coref_list,words_info = add_coreferences(
                    segment_id, index_data, words_info, json_output, discourse_data, coref_list
                )
        #  Processing Stage - identify the cat and proces each cat
        processed_foreign_words,processed_indeclinables,processed_nouns,processed_pronouns,processed_others,process_nominal_form,processed_verbs, processed_auxverbs,processed_adjectives,processed_words= all_processed_cat(
            index_data,gnp_data,seman_data,depend_data,spkview_data,sentence_type,words_info,k1_not_need,has_changes)
        
        for info in words_info:
            if info[4] == '0:main':
                main_verb_tam = info[1]
        tam_term = identify_tam_terms(main_verb_tam)
        morph_input_final_tuple = generate_input_for_morph_generator(processed_words, tam_term, depend_data, sentence_type)
        
        print('# processed_words---------------->', processed_words)
        
        if HAS_CONSTRUCTION_DATA:
            if flag_conj or flag_disjunct:
                processed_words, flag_conj, flag_disjunct = process_construction_conj_disjunct(
                    processed_words, root_words, construction_data, depend_data, 
                    gnp_data, index_data, root_words, flag_conj, flag_disjunct
                )
            if flag_span:
                processed_words, flag_span = process_construction_span(
                    processed_words, construction_data, index_data, flag_span
                )
            if flag_rate:
                processed_words, flag_rate = process_construction_rate(
                    processed_words, construction_data, index_data, flag_rate
                )
            if flag_spatial:
                processed_words, flag_spatial = process_construction_spatial(
                    processed_words, construction_data, index_data, flag_spatial
                )
            if flag_xvanxva:
                processed_words, flag_xvanxva = process_construction_xvanxva(
                    processed_words, construction_data, index_data, flag_xvanxva
                )

        # Input for morph generator is generated and fed into it.
        # Generator outputs the result in a file named morph_input.txt-out.txt
        outputData = generate_morph(processed_words, tam_term, depend_data, sentence_type)
        
        # outputData = check_words_in_dict(outputData,processed_words)
        
        # Check for any non-generated words (mainly noun) & change the gender for non-generated words
    
        # # -> is for the concept which is in dict but its morph data is not found
        # * -> then the conept is not found in dict
        has_changes, processed_nouns = handle_unprocessed(index_data,depend_data,outputData, processed_nouns)
        # handle unprocessed_verbs also with verb agreement
        # If any changes is done in gender for any word.
        # Adjectives and verbs are re-processed as they might be dependent on it.
        if has_changes:
            # Reprocessing adjectives and verbs based on new noun info
            processed_foreign_words,processed_indeclinables,processed_nouns,processed_pronouns,processed_others,process_nominal_form,processed_verbs, processed_auxverbs,processed_adjectives,processed_words= all_processed_cat(index_data,gnp_data,seman_data,depend_data,spkview_data,sentence_type,words_info,k1_not_need,has_changes)

            # Sentence is generated again
            if HAS_CONSTRUCTION_DATA:
                # (processed_words, flag_conj, flag_disjunct, flag_span, flag_rate, flag_spatial, flag_xvanxva) = process_constructions(processed_words, root_words, construction_data, depend_data, gnp_data, index_data, root_words, flag_conj, flag_disjunct, flag_span, flag_rate, flag_spatial, flag_xvanxva)
                if flag_conj or flag_disjunct:
                    processed_words, flag_conj, flag_disjunct = process_construction_conj_disjunct(
                        processed_words, root_words, construction_data, depend_data, 
                        gnp_data, index_data, root_words, flag_conj, flag_disjunct
                    )
                if flag_span:
                    processed_words, flag_span = process_construction_span(
                        processed_words, construction_data, index_data, flag_span
                    )
                if flag_rate:
                    processed_words, flag_rate = process_construction_rate(
                        processed_words, construction_data, index_data, flag_rate
                    )
                if flag_spatial:
                    processed_words, flag_spatial = process_construction_spatial(
                        processed_words, construction_data, index_data, flag_spatial
                    )
                if flag_xvanxva:
                    processed_words, flag_xvanxva = process_construction_xvanxva(
                        processed_words, construction_data, index_data, flag_xvanxva
                    )
            
            outputData = generate_morph(processed_words, tam_term, depend_data, sentence_type)
        # outputData = check_words_in_dict(outputData,processed_words)
    
        # Post-Processing Stage
        # generated words and word-info data is combined #pp data not yet added

        # transformed_data = analyse_output_data(outputData, processed_words)
        transformed_data = analyse_output_data(outputData, morph_input_final_tuple)
        print('transformed_data------------>', transformed_data)
        # if HAS_COREF:
        #     coref_list = process_coreferences(
        #         segment_id, index_data, processed_words, json_output, discourse_data, coref_list
        #     )
        #post-positions are joined.
        
        PP_fulldata = add_postposition(transformed_data,index_data,depend_data, processed_postpositions_dict)
        
        #construction data is joined
        if HAS_CONSTRUCTION_DATA:
            PP_fulldata = add_construction(PP_fulldata, construction_dict)
        
        if HAS_SPKVIEW_DATA:
            PP_fulldata = add_spkview(PP_fulldata, spkview_dict)

        HAS_MORPHO_SEMANTIC_DATA,PP_fulldata = populate_morpho_semantic_dict(index_data,gnp_data, PP_fulldata,words_info)
        if HAS_MORPHO_SEMANTIC_DATA:
            PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)

        # if HAS_ADDITIONAL_WORDS:
        #     PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)

        POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata, coref_list)
        POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT.split()
        POST_PROCESS_OUTPUT = [
            word for word in POST_PROCESS_OUTPUT 
            if clean(word) not in repository.constant.construction_list
        ]
        POST_PROCESS_OUTPUT = clean_post_process_output(POST_PROCESS_OUTPUT, processed_foreign_words)

        if HAS_DISCOURSE_DATA:
            discourse, sp_data = extract_discourse_values(json_output, segment_id)
            POST_PROCESS_OUTPUT = add_discourse_elements_to_output(
                discourse_data,discourse, spkview_data, sp_data, POST_PROCESS_OUTPUT
            )

        POST_PROCESS_OUTPUT = has_ques_mark(POST_PROCESS_OUTPUT, sentence_type)
        POST_PROCESS_OUTPUT = extract_spkview_values(json_output, segment_id, POST_PROCESS_OUTPUT)
        POST_PROCESS_OUTPUT = check_special_conditions(discourse_data, spkview_data, POST_PROCESS_OUTPUT)
        # masked_hindi_data=collect_hindi_output(POST_PROCESS_OUTPUT)
        return POST_PROCESS_OUTPUT
    
    except Exception as e:
            # Return the last line of the error message
        return str(e).splitlines()[-1]
    
def hindi_generation(input_text):
    """
    Process Hindi text input, extracting sentences, segment IDs, and generating structured output.
    """
    input_text = preprocess_input_text(input_text)
    segments = parse_segments(input_text)

    sentences, all_output, segment_ids = [], [], []
    parser = USR_to_json(input_text)
    parser.parse_input_text()
    json_output = parser.get_json_output()

    for segment in segments:
        
        segment_id, sentence, output = process_segment(segment)

        if segment_id:
            segment_ids.append(segment_id)
        if output:
            try:
            #     processed_output = process_file_data(output, segment_id, json_output)
            #     all_output.append(processed_output)
                output1=process_file_data(output,segment_id,json_output)
                if '<>' in output1:
                    # print(output1,'oppp')
                    output1 = output1.replace('<>','[MASK]')
                # print(output1,'oppp')
                all_output.append(output1)
            except Exception as e:
                all_output.append(f"Error processing {segment_id}: {str(e).splitlines()[-1]}")
    # print(segment_ids)
    # json_output1 = convert_sentences_to_json(all_output)
    # all_output=process_masked_multiple_sentences(json_output1)
    last_output = process_sentence(segment_ids, sentences, all_output)
    print('\n-----------------------------------------\n',last_output)
    # print(global_starred_words, 'Global starred words with categories')

    return last_output

if __name__ == '__main__':
    input = '''<sent_id=354>
#rAma Ora sIwA acCe hEM.
rAma 1 per/male - - - - - 5:op1
sIwA 2 per/female - - - - - 5:op2
acCA_1 3 - - 4:k1s - - - - 
as2_1-past 4 - - 0:main - - - - 
[conj_1] 5 - - 4:k1 - - - - 
%affirmative
</sent_id>
'''

    # file_path = './output.txt' 
    
    # Read input data from the file
    # input_data = read_file(file_path)
    input_data = process_input(input, sys.argv[1])
    hindi_generation(input_data)
# [{"segment_id": "7a", "text": "ना केवल वे आज्ञाकारी ही थे।"}, {"segment_id": "7b", "text": "बल्कि वे बहुत समझदार भी थे भी।"}]}
