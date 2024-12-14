
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

