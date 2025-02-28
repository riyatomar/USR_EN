import sys, re, os
import repository.constant

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

def log(mssg, logtype='OK'):
    '''Generates log message in predefined format.'''

    # Format for log message
    print(f'log : [{logtype}]:{mssg}')
    if logtype == 'ERROR':
        path = sys.argv[1]
        write_hindi_test(' ', 'Error', mssg, 'test.csv', path)

def write_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, OUTPUT_FILE, path):
    """Append the hindi text into the file"""
    OUTPUT_FILE = 'TestResults.csv'# temporary for presenting
    str = path.strip('lion_story/')
    if str == '1':
        with open(OUTPUT_FILE, 'w') as file:
            file.write("")

def extract_tamdict_hin():
    extract_tamdict = []
    try:
        with open(repository.constant.TAM_DICT_FILE, 'r') as tamfile:
            for line in tamfile.readlines():
                hin_tam = line.strip()
                if hin_tam:  # Ensure the line is not empty
                    extract_tamdict.append(hin_tam)
        # ##print(extract_tamdict)
        return extract_tamdict
    except FileNotFoundError:
        log('TAM Dictionary File not found.', 'ERROR')
        sys.exit()


def parse_morph_tags_as_list(morph_form):
    """
    Extracts the word and its corresponding morphological tags from the given morph-form string.

    Example:
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    [{'form': 'mA', 'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p'}]
    """
    # Split the morph-form by '/' to get individual word segments
    word = morph_form.split('/')[0].replace('^','')
    segments = morph_form.split('/')
    
    result = []
    # Iterate over each segment
    for segment in segments:
        form = segment.split("<")[0]  # Extract the word (before the first '<')
        if word==form:
            matches = re.findall("<(.*?)>", segment)  # Find all morphological tags
            tag_dict = {match[0]: match[1] for match in matches}  # Convert matches to a dictionary
            tag_dict['form'] = form  # Add the word under the 'form' key
            result.append(tag_dict)  # Add the dictionary to the result list
    # ##print(result,'result')
    return result

def find_tags_from_dix_as_list(word):
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac /home/lc4eu/LC/Hybrid-Hindi-generator/apertium-eng/eng.automorf.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    p_m=parse_morph_tags_as_list(morph_forms)
    # ##print(p_m,'pmmmmmmmmm')
    return p_m
    