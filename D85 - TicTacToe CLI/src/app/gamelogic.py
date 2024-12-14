import re
import random
from app.board import Board
from app.player import Player
from app.helpers import get_input


class GameLogic:
    def __init__(self, board: Board, player_a: Player, player_b: Player):
        self.board = board
        self.marker_options = self.board._marker_options
        self.player_a: Player = player_a
        self.player_b: Player = player_b
        self.player_current_turn: Player = None
        self.winner_last_game: Player = None
        self.last_game_tied: bool = False
        self.total_games = 0
        self.ties = 0
        self.game_over = True
        
        self.prep_new_game()


    def prep_new_game(self):
        players = [self.player_a, self.player_b]
        is_first = None

        if self.winner_last_game == None or self.total_games == 0 or self.last_game_tied:
            is_first = random.choice(players)  
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