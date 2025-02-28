
# def format_morph_input(morph_input_final_tuple):
#     """Formats the morph input data into the required structure."""
#     morph_input_format = []
    
#     for item in morph_input_final_tuple:
#         if isinstance(item, tuple) and item:  
#             word = item[1]
#             tags = ''.join(f'<{tag}>' for tag in item[2:])
#             morph_input_format.append(f'^{word}{tags}$')
    
#     return morph_input_format

def format_morph_input(morph_input_final_tuple):
    """Formats the morph input data into the required structure."""
    morph_input_format = []
    
    for item in morph_input_final_tuple:
        if isinstance(item, tuple) and item:
            word = item[1]
            
            # Check if the last element is a special marker (e.g., "# to")
            if item[-1].startswith('#'):
                tags = ''.join(f'<{tag}>' for tag in item[2:-1])  # Exclude last element
                marker = item[-1]  # Store the marker separately
            else:
                tags = ''.join(f'<{tag}>' for tag in item[2:])
                marker = ''
            
            # Construct the formatted string
            formatted_str = f'^{word}{tags}{marker}$'
            morph_input_format.append(formatted_str)
    
    return morph_input_format
