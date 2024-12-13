import pytest
from app.main import Board

valid_column = 'A'
valid_row = 1
invalid_column = 'F'
invalid_row = 6

e = ' '    # empty slots


def test_board_instantiation_values():
    b = Board(4)
    assert b.rows == [1, 2, 3, 4]
    assert b.cols == ['A', 'B', 'C', 'D']
    assert b._slots == {'A': {1: e, 2: e, 3: e, 4: e}, 'B': {1: e, 2: e, 3: e, 4: e}, 'C': {1: e, 2: e, 3: e, 4: e}, 'D': {1: e, 2: e, 3: e, 4: e}}


def test_board_place_marker_valid_coords():
    b = Board(4)
    assert b._slots['A'][1] == e
    assert b._slots_remaining == 16
    
    b.place_marker('X', valid_column, valid_row)
    assert b._slots['A'][1] == 'X'
    assert b._slots_remaining == 15


def test_board_place_marker_invalid_coords():
    b = Board(4)
    with pytest.raises(KeyError):
        b.place_marker('X', invalid_column, valid_row)
    with pytest.raises(KeyError):
        b.place_marker('X', valid_column, invalid_row)


def test_board_place_marker_slot_not_empty():
    b = Board(4)
    b.place_marker('X', valid_column, valid_row)
    with pytest.raises(ValueError):
        b.place_marker('X', valid_column, valid_row)

