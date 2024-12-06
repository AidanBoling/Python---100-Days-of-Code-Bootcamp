from main import preformat_message, convert_message
import pytest

# valid_eng_message_raw = "This is a test. Don't stop the music!"


def test_convert_message_invalid_action():
    # Error if action is neither 'decode' nor 'encode'
    with pytest.raises(ValueError):
        convert_message('', 'TEST')


def test_convert_message_action_mismatch():
    msg_in_morse = '. . .   ---'
    msg_in_eng = 'This is a test.'
    
    encode_output, encode_ignored = convert_message('encode', msg_in_morse)
    assert encode_output == ''
    assert encode_ignored == ['.', '.', '.', '-', '-', '-']
    
    decode_output, decode_ignored = convert_message('decode', msg_in_eng)
    assert decode_output == ''
    assert decode_ignored == ['This is a test.']


def test_convert_valid():
    valid_eng_message_formatted = 'THIS IS A TEST STOP DONT STOP THE MUSIC STOP'
    valid_morse_message = '---   . . . .   . .   . . .       . .   . . .       . ---       ---   .   . . .   ---       . . .   ---   --- --- ---   . --- --- .       --- . .   --- --- ---   --- .   ---       . . .   ---   --- --- ---   . --- --- .       ---   . . . .   .       --- ---   . . ---   . . .   . .   --- . --- .       . . .   ---   --- --- ---   . --- --- .'
    symbols_only = '%?@$'

    encode_output, encode_ignored = convert_message('encode', valid_eng_message_formatted)
    assert encode_output == valid_morse_message
    assert encode_ignored == []

    encode_out, encode_ignored = convert_message('encode', symbols_only)
    assert encode_out == ''
    assert encode_ignored == ['%', '?', '@', '$']

    decode_output, decode_ignored = convert_message('decode', valid_morse_message)
    assert decode_output == valid_eng_message_formatted
    assert decode_ignored == []


def test_preformat_encode():
    action = 'encode'

    # Converting sentence stops (!, ., ...)
    assert preformat_message(action, '!') == ' STOP'
    assert preformat_message(action, 'Test!') == 'TEST STOP'
    assert preformat_message(action, 'Test... !') == 'TEST STOP STOP'

    # Space removal
    assert preformat_message(action, 'Testing  space   removal.    ') == 'TESTING SPACE REMOVAL STOP'
    

def test_preformat_decode():
    # Should be unchanged except for: start/end spaces stripped, and converted to uppercase

    action = 'decode'
    morse_with_preceding_spaces = '    ---   .   . . .   ---       . . .   ---   --- --- ---   . --- --- .'
    morse_no_preceding_spaces = '---   .   . . .   ---       . . .   ---   --- --- ---   . --- --- .'
    
    assert preformat_message(action, morse_with_preceding_spaces) == morse_no_preceding_spaces
    assert preformat_message(action, '  Test message.') == 'TEST MESSAGE.'
    assert preformat_message(action, 'Testing  space   removal.') == 'TESTING  SPACE   REMOVAL.'