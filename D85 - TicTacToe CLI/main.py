def main():

    # Initial setup user questions:
    # - board size? 
    #       Make note to user that max board size is {len(COL_LETTERS)}.
    #       User input validation: only accept numbers, which are <= len(COL_LETTERS)
    
    # create Board
    # create players
    # game_logic = GameLogic
    # game_logic.run_game()
    
    # After game over: Play again?
    pass


class Player:
    def __init__(self):
        self.marker = None
        self.wins = 0



# Board

COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class Board:
    def __init__(self, size:int=3):
        self.size = size
        self.rows = []
        self.cols = []
        self.empty_slot = ' '
        self._slot_matrix:list = []
        self._slots:dict = {}

        self.build_board()


    def build_board(self):
        '''Runs on instantiation. Set up grid and slots based on given board size.'''
        self.cols = COL_LABELS[:self.size]
        self.rows = [i+1 for i in range(self.size)]

        for col in self.cols:
            self._slots[col] = {row: self.empty_slot for row in self.rows}


    def generate_board_img(self):
        '''Returns string that can be printed to show current board.'''
        row_start_spaces = 2
        cell_width = 3
        cell_border = '-' * cell_width
        cell_padding = ' ' * int((cell_width - 1) / 2)
        col_label_cell_padding = ' ' * cell_width

        col_labels_row = f'{(" " * row_start_spaces)} ' + cell_padding + f'{col_label_cell_padding}'.join(self.cols)
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
        self._slots[column][row] = marker
        
        # Should throw index (?) error if row or column is outside of board

    # TODO (?): throw error if try to instantiate with board size larger than LETTERS



class GameLogic:
    def __init__(self, board: Board, player_a: Player, player_b: Player):
        self.board = board
        self.player_a = player_a
        self.player_b = player_b
        self.player_current_turn: Player = None
        self.winner_last_game: Player = None
        self.total_games = 0
        self.game_over = True
        

    def setup_new_game(self):
        # assign markers to players:
        #       - random if total_games == 0
        #       - otherwise, whoever didn't win
        
        # Set current_player_turn -- whoever assigned "X"
        pass
    

    def run_game(self):
        self.setup_new_game()
        self.game_over = False

        while not self.game_over:
            self.get_player_move()
            
            # Process end-of-turn:
            # Once move is input successfully, print board
            self.display_updated_board()
            
            # Assess if player has won
            player_won = self.check_for_win()
            
            if not player_won:
                self.switch_player_turn()
        
        # Process end-of-game:
            # Update stats:
            # set winner_last_game = current_turn_player
            # set current_turn_player.wins += 1
            # set self.total_games += 1

            # Get input:  (--> should prob be in main())
            # Ask if play again
            # If yes, ask if change board size
                
    
    def switch_player_turn(self):
        players = [self.player_a, self.player_b]
        for player in players:
            if self.player_current_turn != player:
                self.player_current_turn = player


    def get_player_move(self):
        #   Get user input
            #   - only accept strings of length 2, alphanumeric, containing 1 number, and 1 alpha.

        # update board upon input
            # split input into appropriate parts (column is alpha, row is number) 
            # try/catch self.board.place_marker -- If board returns index error, tell user that it is invalid, 
                                                #  If no error, break input loop
        pass
    
    
    def display_updated_board(self):
        img = self.board.generate_board_img()
        print('\n', img, '\n')
        

    def check_for_win(self):
        vectors = []
        row_nums = self.board.rows
        col_labels = self.board.cols
        slots = self.board._slots

        diagonals = [[],[]]
        
        # Option B (dict):
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
                print('Win found!')
                return True
        
        print('No wins')
            


if __name__ == "__main__":
    main()