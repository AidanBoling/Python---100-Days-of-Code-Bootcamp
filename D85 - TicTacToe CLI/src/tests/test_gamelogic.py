import pytest
from app.board import Board
from app.player import Player
from app.gamelogic import GameLogic


@pytest.fixture
def board() -> Board:
    return Board(3)


@pytest.fixture
def game(board:Board) -> GameLogic:
    player_a = Player(name='Player A')
    player_b = Player(name='Player B')
    return GameLogic(board, player_a, player_b)


@pytest.fixture
def players(game:GameLogic) -> list[Player]:
    return [game.player_a, game.player_b]


def test_prep_new_game(game: GameLogic, players: list[Player]):
    game.prep_new_game()
    assert players[0].marker in game.marker_options
    assert players[1].marker in game.marker_options
    assert game.player_current_turn != None


def test_prep_new_game_player_order(game: GameLogic, players: list[Player]):
    '''Whoever lost last game => assigned to first marker in marker_options (default 'X'), and goes first next game'''
    game.total_games = 1
    game.winner_last_game = players[0]

    game.prep_new_game()
    assert game.player_current_turn == players[1]
    assert game.player_b.marker == game.marker_options[0]
    assert game.player_a.marker == game.marker_options[1]


def test_switch_player_turn(game: GameLogic): 
    '''Testing function to change turn to next player.'''
    players = [game.player_a, game.player_b]
    game.player_current_turn = players[0]

    game.switch_player_turn()
    assert game.player_current_turn == players[1]


@pytest.mark.parametrize( 'coordinate_set, expected',  
    [  
        ([('A', 1), ('B', 1), ('C', 1)], True),  # Win along a row
        ([('A', 1), ('A', 2), ('A', 3)], True),  # Win along a column
        ([('A', 1), ('B', 2), ('C', 3)], True),  # Win along a diagonal
        ([], False),     # empty board => no win
    ])  
def test_check_for_win(game:GameLogic, board:Board, coordinate_set:list, expected:bool):
    '''Testing check_for_win() function. Tests various sets of marker placements 
    (e.g. coordinates for a win along each possible vector -- row, column, diagonal).'''
    
    board.build_board()
    for coord in coordinate_set:
        board.place_marker('X', coord[0], coord[1])
    assert game.check_for_win() == expected