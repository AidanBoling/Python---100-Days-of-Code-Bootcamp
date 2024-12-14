import sys

def confirm_exit(noun:str = 'program', exit_message='Exiting.'):
        confirm = input(f'No input given. Exit {noun}? (y/n) ')
        
        if confirm.strip().lower() == 'n':
            return

        else:
            print(exit_message)
            sys.exit()


def get_input(prompt, options:list = [], validation_func=None, allow_blank=False):
        '''Asks for input from user, using passed-in prompt. If any options
        passed in, only input matching one of the options is accepted. 
        
        If allow_blank=False (default), when the input is empty, user asked 
        if they would like to exit.
        
        Also accepts a validation_func: any function that accepts a string
        (the user input) and returns a boolean, where True means the string 
        is valid.
        '''

        while True:
            try:
                user_input = input(prompt).strip()
                if user_input:
                    if len(options) > 0 or validation_func:
                        if len(options) > 0 and user_input.lower() in options:
                            return user_input.lower()
                        
                        elif validation_func(user_input):
                            return user_input.lower()
                        
                        else:
                            print('\nInvalid entry. \n')

                    else:
                        return user_input.lower()

                else:
                    if not allow_blank: 
                        confirm_exit('game')
                    else: 
                        return

            except KeyboardInterrupt:
                print('\n')
                sys.exit()