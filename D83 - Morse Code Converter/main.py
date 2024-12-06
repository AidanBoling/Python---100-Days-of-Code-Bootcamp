import sys
import lib

# Text-based (command line) program that takes any String input and converts it into Morse Code.

ENCODE_DICT = lib.morse_code_dict
DECODE_DICT = {value: key for key, value in ENCODE_DICT.items()}

def main():

    while True:
        action = get_input('Type "encode" to convert TO Morse Code, type "decode" to convert FROM Morse Code: \n', 'options', ['decode', 'encode'])
        message =  get_input('Type the message: \n')

        result = transform_message(action, message)
        print(f"Here's the converted message: \n{result}")

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


def transform_message(action, message):
    transformed_msg = ''

    
    # shifted_list = get_shifted_list(shift)
    # start_list = message
    # lookup_list = ENCODE_DICT

    if action == 'decode':
        pass
        # start_list = DECODE_DICT
        # lookup_list = get_shifted_list(shift)

    for char in message:
        # if char in chars:
        #     i = start_list.index(char)
        #     transformed_msg += lookup_list[i]

        # else:
        #     transformed_msg += char

    return transformed_msg





if __name__ == "__main__":
    main()