from app.board import Board, COL_LABELS
from app.player import Player
from app.gamelogic import GameLogic
from app.helpers import get_input


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


if __name__ == "__main__":
    main()