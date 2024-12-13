from app.main import Board, Player, GameLogic

board = Board(3)
player_a = Player(name='Player A')
player_b = Player(name='Player B')
game = GameLogic(board, player_a, player_b)


def test_prep_new_game():
    game.prep_new_game()
    marker_options = board._marker_options
    assert player_a.marker in marker_options
    assert player_b.marker in marker_options

    assert game.player_current_turn != None


def test_prep_new_game_player_order():
    # Whoever lost last game --> assigned 'X' and goes first next game (winner gets 'O')
    game.winner_last_game = player_a
    game.prep_new_game()
    assert game.player_current_turn == player_b
    assert game.player_b.marker == board._marker_options[0]
    assert game.player_a.marker == board._marker_options[1]


def test_switch_player_turn(): 
    game.player_current_turn = player_a
    game.switch_player_turn()
    assert game.player_current_turn == player_b


def test_check_for_win():
    # Create test win for each possible vectors (row, column, diagonal), with fresh board
    # check_for_win() should return True in each case
    row_win_coords = [('A', 1), ('B', 1), ('C', 1)]
    col_win_coords = [('A', 1), ('A', 2), ('A', 3)]
    diagonal_win_coords = [('A', 1), ('B', 2), ('C', 3)]
    
    for coordinate_set in [row_win_coords, col_win_coords, diagonal_win_coords]:
        board.build_board()
        for coord in coordinate_set:
            board.place_marker('X', coord[0], coord[1])
        assert game.check_for_win() == True
    

    board.build_board()
    assert game.check_for_win() == False    # empty board => no win

   
