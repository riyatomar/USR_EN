# import sys

# input_usr = '''<sent_id=354>
# #rAma Ora sIwA acCe hEM.
# rAma 1 per/male - - - - - 5:op1
# sIwA 2 per/female - - - - - 5:op2
# acCA_1 3 - - 4:k1s - - - - 
# as2_1-pres 4 - - 0:main - - - - 
# [conj_1] 5 - - 4:k1 - - - - 
# %affirmative
# </sent_id>
# '''

# if len(sys.argv) > 1:
#     arg = sys.argv[1].lower()
# else:
#     arg = "eng"  # Default to 'eng'

# if arg == "hin":
#     column_to_check = 1
# elif arg == "skt":
#     column_to_check = 2

# lines = input_usr.split("\n")

# concept_dict = {}
# with open("/home/lc4eu/LC/Hybrid-Hindi-generator/lc4eu/dictionaries/concept-to-mrs-rels.dat", "r") as f:
#     for row in f:
#         cols = row.strip().split()
#         if len(cols) >= 4:
#             key = cols[2] if arg == "skt" else cols[1]
#             concept_dict[key] = cols[3]

# updated_lines = []
# for line in lines:
#     words = line.split()
    
#     # Skip metadata lines
#     if not words or words[0].startswith("<") or words[0].startswith("#") or words[0].startswith("%"):
#         updated_lines.append(line)
#         continue

#     # Replace only if the word exists in concept_dict
#     if words[0] in concept_dict:
#         words[0] = concept_dict[words[0]]
#     elif '-' in words[0]:
#         base_word = words[0].split('-')[0]
#         suffix = words[0].split('-')[1]
        
#         if base_word in concept_dict:  # Check before accessing dictionary
#             words[0] = concept_dict[base_word] + '-' + suffix
#         else:
#             words[0] = base_word + '-' + suffix
#             # print(f"Warning: {base_word} not found in concept_dict")  # Debugging output


#     updated_lines.append(" ".join(words))

# print("\n".join(updated_lines))



import sys

def process_input(input_text, lang="eng", concept_file="dictionaries/concept-to-mrs-rels.dat"):
    """
    Processes the input text, replacing words based on a concept dictionary.
    
    Parameters:
    input_text (str): The input text containing tagged sentences.
    lang (str): The language to process ('eng', 'hin', 'skt'). Defaults to 'eng'.
    concept_file (str): Path to the concept-to-mrs-rels.dat dictionary.

    Returns:
    str: The processed text with words replaced based on the dictionary.
    """
    
    if lang == "hin":
        column_to_check = 1
    elif lang == "skt":
        column_to_check = 2
    else:
        column_to_check = 1  # Default to Hindi if unspecified

    # Load the concept dictionary
    concept_dict = {}
    try:
        with open(concept_file, "r", encoding="utf-8") as f:
            for row in f:
                cols = row.strip().split()
                if len(cols) >= 4:
                    key = cols[2] if lang == "skt" else cols[1]
                    concept_dict[key] = cols[3]
    except FileNotFoundError:
        print(f"Error: Concept file '{concept_file}' not found.")
        return input_text  # Return original text if dictionary file is missing

    lines = input_text.split("\n")
    updated_lines = []

    for line in lines:
        words = line.split()

        # Skip metadata and comments
        if not words or words[0].startswith(("<", "#", "%")):
            updated_lines.append(line)
            continue

        # Replace word if found in concept_dict
        if words[0] in concept_dict:
            words[0] = concept_dict[words[0]]
        elif '-' in words[0]:  # Handle hyphenated words
            base_word, suffix = words[0].split('-', 1)
            words[0] = concept_dict.get(base_word, base_word) + '-' + suffix

        updated_lines.append(" ".join(words))

    return "\n".join(updated_lines)


# # Example usage
# input_usr = '''<sent_id=354>
# #rAma Ora sIwA acCe hEM.
# rAma 1 per/male - - - - - 5:op1
# sIwA 2 per/female - - - - - 5:op2
# acCA_1 3 - - 4:k1s - - - - 
# as2_1-pres 4 - - 0:main - - - - 
# [conj_1] 5 - - 4:k1 - - - - 
# %affirmative
# </sent_id>
# '''

# result = process_input(input_usr, lang="skt")  # Change lang to "skt" if needed
# print(result)
