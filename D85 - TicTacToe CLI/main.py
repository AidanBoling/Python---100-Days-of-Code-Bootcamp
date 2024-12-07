def main():

    # Initial setup user questions:
    # - board size? 
    #       Make note to user that max board size is {len(COL_LETTERS)}.
    #       User input validation: only accept numbers, which are <= len(COL_LETTERS)
    
    pass


class GameLogic:
    pass


# Board

COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class Board:
    def __init__(self, board_size:int=3):
        self.board_size = board_size
        self.rows = []
        self.cols = []
        self.empty_slot = ' '
        self._slot_matrix = []

        self.build_board()


    def build_board(self):
        '''Runs on instantiation. Set up grid and slots based on given board size.'''
        row_num = 0
        slot_row = []
        for i in range(self.board_size):
            row_num += 1
            self.rows.append(row_num)
            self.cols.append(COL_LABELS[i])
            slot_row.append(self.empty_slot)

        for _ in range(self.board_size):
            self._slot_matrix.append(slot_row)
    

    def generate_board_img(self):
        '''Returns string that can be printed to show current board.'''
        cell_width = 3
        cell_border = '-' * cell_width
        cell_padding = ' ' * int((cell_width - 1) / 2)
        col_label_cell_padding = ' ' * cell_width
        row_start_spaces = 2

        col_labels_row = f'{(" " * row_start_spaces)} ' + cell_padding + f'{col_label_cell_padding}'.join(self.cols)
        top_border_row = (' ' * row_start_spaces) + (('|' + cell_border) * self.board_size) + '|'
        border_row = (' ' * row_start_spaces) + '|' + ((cell_border + '+') * (self.board_size - 1)) + cell_border + '|'
        bottom_border_row = (' ' * row_start_spaces) + ' ' + ((cell_border + '-') * (self.board_size - 1)) + cell_border

        img_rows = [col_labels_row, top_border_row]
        for i, row_num in enumerate(self.rows, 0):
            row = self._slot_matrix[i]
            row_as_string = f"{row_num} |{cell_padding}{f'{cell_padding}|{cell_padding}'.join(row)}{cell_padding}|"
            if i > 0:
                img_rows.append(border_row)
            img_rows.append(row_as_string)

        img_rows.append(bottom_border_row)
        
        board_img = '\n'.join(img_rows)
        
        return board_img
    
    
    def place_marker(self, marker):
        pass
    
    # TODO (?): throw error if try to instantiate with board size larger than LETTERS


if __name__ == "__main__":
    main()