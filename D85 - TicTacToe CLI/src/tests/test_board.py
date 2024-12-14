import pytest
from app.board import Board

valid_column = 'A'
valid_row = 1
invalid_column = 'F'
invalid_row = 6

e = ' '    # empty slots


@pytest.fixture
def board() -> Board:
    return Board(4)


@pytest.fixture
def board_attrs(board: Board) -> dict:
    return board.__dict__


@pytest.mark.parametrize('attribute, expected', 
                         [('rows', [1, 2, 3, 4]), 
                          ('cols', ['A', 'B', 'C', 'D']), 
                          ('_slots', {'A': {1: e, 2: e, 3: e, 4: e}, 'B': {1: e, 2: e, 3: e, 4: e}, 'C': {1: e, 2: e, 3: e, 4: e}, 'D': {1: e, 2: e, 3: e, 4: e}}),
                          ('_slots_remaining', 16),
                          ])
def test_board_instantiation_values(board_attrs: dict, attribute, expected):
    assert board_attrs[attribute] == expected


def test_board_place_marker_valid_coords(board: Board):
    '''Tests placing a marker with valid coords on empty slot'''
    slots_after_marker_placed = board._slots_remaining - 1
    
    board.place_marker('X', valid_column, valid_row)
    assert board._slots[valid_column][valid_row] == 'X'
    assert board._slots_remaining == slots_after_marker_placed


def test_board_place_marker_invalid_coords(board: Board):
    with pytest.raises(KeyError):
        board.place_marker('X', invalid_column, valid_row)
    with pytest.raises(KeyError):
        board.place_marker('X', valid_column, invalid_row)


def test_board_place_marker_slot_not_empty(board: Board):
    board.place_marker('X', valid_column, valid_row)
    with pytest.raises(ValueError):
        board.place_marker('X', valid_column, valid_row)

