import sys
import re
import lib

# Text-based (command line) program that takes any String input and converts it into, or out of Morse Code.
# Currently only converts English alphabet.

ENCODE_DICT = lib.morse_code_dict
DECODE_DICT = {value: key for key, value in ENCODE_DICT.items()}


def main():

    while True:
        action = get_input('Type "encode" to convert TO Morse Code, type "decode" to convert FROM Morse Code: \n', 'options', ['decode', 'encode'])
        message =  get_input('Enter message: \n')
        formatted_message = preformat_message(action, message)
        converted_msg, ignored = convert_message(action, formatted_message)
        print(f"Here's the converted message: \n{converted_msg}")
        
        if len(ignored):
            print(f'\nThe following {len(ignored)} character(s) were ignored: \n', ', '.join(ignored))

        if input('Convert another message? (y/n) ').strip().lower() != 'y':
            break


def get_input(prompt, input_validation = 'none', options = []):

    while True:
        try:
            user_input = input(prompt).strip()
            if user_input:
                if input_validation == 'numeric' and user_input.isnumeric() and 0 < int(user_input) <= len(chars):
                    return int(user_input)

                elif input_validation == 'options' and len(options) > 0 and user_input.lower() in options:
                    return user_input.lower()
                    
                elif input_validation == 'none':
                    return user_input.lower()

                else:
                    print('\nInvalid entry. \n')
            
            else:
                confirm_exit()

        except KeyboardInterrupt:
            print('\n')
            sys.exit()


def confirm_exit():
    confirm = input('No input given. Exit program? (y/n) ')
    
    if confirm.strip().lower() == 'n':
        return

    else:
        sys.exit()


def preformat_message(action: str, message: str):   
    formatted_msg = message.strip().upper()

    if action == 'encode':
        formatted_msg = re.sub("\.+|!", ' STOP', formatted_msg)     # Change end-of-sentence punctuation '...', '.', '!' to 'STOP'
        formatted_msg = re.sub("\s\s+", ' ', formatted_msg)     # Multiple spaces => only one space
    
    return formatted_msg


def convert_message(action:str, message:str):
    converted_msg = ''
    ignored_chars = []
    
    if action == 'encode':
        conversion_dict = ENCODE_DICT

        for char in message:
            if char in conversion_dict:
                if char == ' ':
                    converted_msg += conversion_dict[char]
                else:
                    converted_msg += conversion_dict[char] + conversion_dict['letter gap']
            else:
                ignored_chars.append(char)

    elif action == 'decode':
        conversion_dict = DECODE_DICT
        message_list = message.split(ENCODE_DICT['word gap'])

        for word in message_list:
            word = word.split(ENCODE_DICT['letter gap'])
            
            for char in word:
                if char in conversion_dict:
                    converted_msg += conversion_dict[char]
                else:
                    ignored_chars.append(char)
            
            converted_msg += ' '
    
    else:
        raise ValueError("Action must be either 'encode' or 'decode'.")
    
    converted_msg = converted_msg.strip()

    return converted_msg, ignored_chars


if __name__ == "__main__":
    main()




