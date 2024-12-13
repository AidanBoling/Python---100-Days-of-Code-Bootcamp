import sys
import re
import random

# from board import Board, COL_LABELS

def main():
    print('\n Welcome to Tic Tac Toe!\n')
    print('\nSetup: ')
    
    # BOARD SETUP
    board_size_options = [f'{i}' for i in range(3, len(COL_LABELS)+1)]
    board_size = 3
    board_prompt = f"\nBoard size is set to {board_size}. Would you like to change this? \nType 'y' to change, and 'n' (or leave blank) to keep current size: "
    board_prompt_2 = f'Enter number from 3 to {len(COL_LABELS)} (max board size): '

    change_board_size = get_input(board_prompt, allow_blank=True) 
    if change_board_size == 'y':
        board_size = int(get_input(board_prompt_2, options=board_size_options))
    
    board = Board(board_size)

    # PLAYER SETUP
    name_1 = 'Player 1'
    name_2 = 'Player 2'
    names_prompt = "\nCustomize player names? \nType 'y' to customize, and 'n' (or leave blank) to use defaults: "
    customize_names = get_input(names_prompt, options = ['y', 'n'], allow_blank=True)
    if customize_names == 'y':
        name_1 = get_input('Enter Player 1 name: ').title()
        name_2 = get_input('Enter Player 2 name: ').title()
        # Q: Add name validation?

    player_a = Player(name_1)
    player_b = Player(name_2)

    # GAME PLAY
    game_logic = GameLogic(board, player_a, player_b)
    continue_play = True
    
    while continue_play:
        game_logic.run_game()
        
        player_input = get_input('\n...Play again? (y/n) \n', options = ['y', 'n', 'yes', 'no'])
        if player_input in ['n', 'no']:
            continue_play=False

    print('\nGoodbye!\n')


# Helpers:

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


# PLAYER
class Player:
    def __init__(self, name:str):
        self.marker = None
        self.wins = 0
        self.name:str = name



# BOARD

COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class Board:
    def __init__(self, size:int=3):
        self.size = size
        self.rows = []
        self.cols = []
        self.empty_slot = ' '
        self._slots:dict = {}
        self._slots_remaining = None
        self._marker_options = ['X', 'O']       # marker order matches turn order

        self.build_board()


    def build_board(self):
        '''Runs on instantiation. Set up grid and slots based on given board size.'''
        self.cols = COL_LABELS[:self.size]
        self.rows = [i+1 for i in range(self.size)]

        for col in self.cols:
            self._slots[col] = {row: self.empty_slot for row in self.rows}

        self._slots_remaining = self.size * self.size


    def generate_board_img(self):
        '''Returns string that can be printed to show current board.'''
        row_start_spaces = 2
        cell_width = 3
        cell_border = '-' * cell_width
        cell_padding = ' ' * int((cell_width - 1) / 2)
        col_label_cell_padding = ' ' * cell_width

        col_labels_row = f'{(" " * row_start_spaces)}' + cell_padding + f'{col_label_cell_padding}'.join(self.cols)
        top_border_row = (' ' * row_start_spaces) + (('|' + cell_border) * self.size) + '|'
        border_row = (' ' * row_start_spaces) + '|' + ((cell_border + '+') * (self.size - 1)) + cell_border + '|'
        bottom_border_row = (' ' * row_start_spaces) + ' ' + ((cell_border + '-') * (self.size - 1)) + cell_border

        img_rows = [col_labels_row, top_border_row]
        for row in self.rows:
            row_as_str = f'{row} |'
            border = border_row

            for col in self.cols:
                slot_value = self._slots[col][row]
                cell = f'{cell_padding}{slot_value}{cell_padding}|'
                row_as_str += cell

            if row == self.rows[-1]:
                border = bottom_border_row
            img_rows.extend([row_as_str, border])
           
        board_img = '\n'.join(img_rows)
        
        return board_img
    

    def place_marker(self, marker:str, column:str, row:int):
        slot_selected = self._slots[column][row]    # Adding extra step so throws KeyError if *either* 'column' or 'row' are invalid (rather than just 'column')
        if slot_selected == self.empty_slot:
            self._slots[column][row] = marker
            self._slots_remaining -= 1
        else:
            raise ValueError('Invalid move: Slot already taken.\n')




#GAME BRAIN

class GameLogic:
    def __init__(self, board: Board, player_a: Player, player_b: Player):
        self.board = board
        self.marker_options = self.board._marker_options
        self.player_a: Player = player_a
        self.player_b: Player = player_b
        self.player_current_turn: Player = None
        self.winner_last_game: Player = None
        self.total_games = 0
        self.ties = 0
        self.game_over = True
        
        self.prep_new_game()


    def prep_new_game(self):
        players = [self.player_a, self.player_b]
        is_first = None

        if self.winner_last_game == None or self.total_games == 0 or self.last_game_tied:
            is_first = random.choice([self.player_a, self.player_b])  
        else:
            for player in players:
                if player != self.winner_last_game:
                    is_first = player

        players.remove(is_first)
        players.insert(0, is_first)

        for i in range(2):
            players[i].marker = self.marker_options[i]

        self.player_current_turn = players[0]

        if self.total_games > 0:
            self.board.build_board()


    def run_game(self):
        self.prep_new_game()    
        self.game_over = False
        print(f"\n{self.player_a.name} is '{self.player_a.marker}', {self.player_b.name} is '{self.player_b.marker}'.")
        print(f'{self.player_current_turn.name} goes first.')
        print('\nGame on!')

        self.display_current_board()

        while not self.game_over:
            self.get_player_move()
            
            # Process end-of-turn:
            self.display_current_board()

            player_won = self.check_for_win()
            is_tie = self.board._slots_remaining == 0

            if not player_won and not is_tie:
                self.switch_player_turn()
            else:
                if is_tie:
                    self.last_game_tied = True
                else:
                    self.last_game_tied = False

                self.game_over = True

        # Process end-of-game:
        end_of_game_message = ''
        if self.last_game_tied:
            winner = None
            self.ties += 1
            end_of_game_message = f"It's a tie!"
        else:
            winner = self.player_current_turn
            self.winner_last_game = winner
            winner.wins += 1
            end_of_game_message = f'{winner.name} wins!'

        
        self.total_games += 1

        print(f'\n{end_of_game_message}\n')
        print('\n---Running stats---\n')
        print('Total games: ', self.total_games)
        print(f'Ties: ', self.ties)
        print(f'\n{self.player_a.name} wins: ', self.player_a.wins)
        print(f'{self.player_b.name} wins: ', self.player_b.wins)
        print('\n-------------------\n')

    
    def switch_player_turn(self):
        for player in [self.player_a, self.player_b]:
            if self.player_current_turn != player:
                self.player_current_turn = player
                break


    def get_player_move(self):
        '''Takes input from user, and enters onto board. If input not valid at 
        any point, prompts player for input again.'''

        player = self.player_current_turn
        marker = player.marker
        column = None
        row = None


        def move_validation(input:str) -> bool:  
            input.replace(' ', '')   
            if not len(input)==2:
                return
            if not input.isalnum():
                return
            if not (re.search('[a-zA-Z]+', input) and re.search('[0-9]', input)):
                return
            
            return True
        

        marker_placed = False
        while not marker_placed:
            player_prompt = f"{player.name}'s move: "
            
            player_move = get_input(player_prompt, validation_func=move_validation)
            
            coordinates = list(player_move)
            for coord in coordinates:
                if coord.isalpha():
                    column = coord.upper()
                if coord.isnumeric():
                    row = int(coord)

            try:
                self.board.place_marker(marker, column, row)
                marker_placed = True
            except KeyError:
                print('Invalid move -- outside of board. Please try again.')
                print(f'Valid column letters: {self.board.cols}\nValid row numbers: {self.board.rows}\n')
            except ValueError as e:
                print(e)


    def display_current_board(self):
        img = self.board.generate_board_img()
        print('\n\n', img, '\n')
        

    def check_for_win(self) -> bool:
        '''Determine if there has been a win -- any row, column, 
        or diagonal with the same marker filling all slots.'''
        vectors = []
        row_nums = self.board.rows
        col_labels = self.board.cols
        slots = self.board._slots
        diagonals = [[],[]]
        
        # Columns
        cols = [slots[col].values() for col in slots.keys()]
        vectors.extend(cols)
        
        #Rows
        for num in row_nums:
            row = [slots[col][num] for col in col_labels]
            vectors.append(row)

        #Diagonals
        for i in range(self.board.size):
            col = col_labels[i]
            row = i+1
            row_rev = self.board.size - i
            
            diagonals[0].append(slots[col][row])
            diagonals[1].append(slots[col][row_rev])
        vectors.extend(diagonals)

        for vector in vectors:
            vector = list(set(vector))
            if len(vector) == 1 and vector[0] != self.board.empty_slot:
                return True
        
        return False


if __name__ == "__main__":
    main()