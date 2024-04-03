DOWN = 270 
UP = 90
LEFT = 180 
RIGHT = 0

number_shapes = {
                '0': {'width': 3, 'moves': {'1': [3, 6, 3, 6], '2': [3, 6, 3, 6]}, 'directions': {'1': [LEFT, DOWN, RIGHT, UP], '2': [RIGHT, DOWN, LEFT, UP]}}, 
                '1': {'width': 1, 'moves': {'1': [7], '2': [7]}, 'directions': {'1': [DOWN], '2': [DOWN]}},
                '2': {'width': 3, 'moves': {'1': [3, 3, 3, 3, 3, 4], '2': [3, 3, 3, 3, 4]}, 'directions': {'1': [LEFT, RIGHT, DOWN, LEFT, DOWN, RIGHT], '2': [RIGHT, DOWN, LEFT, DOWN, RIGHT]}}, 
                '3': {'width': 3, 'moves': {'1': [3, 3, 3, 3, 3, 3, 4], '2': [3, 3, 3, 3, 3, 4]}, 'directions': {'1': [LEFT, RIGHT, DOWN, LEFT, RIGHT, DOWN, LEFT], '2': [RIGHT, DOWN, LEFT, RIGHT, DOWN, LEFT]}},
                '4': {'width': 3, 'moves': {'1': [6, 3, 3, 4], '2': [3, 3, 3, 7]}, 'directions': {'1': [DOWN, UP, LEFT, UP], '2': [DOWN, RIGHT, UP, DOWN]}},
                '5': {'width': 3, 'moves': {'1': [3, 3, 3, 3, 4], '2': [3, 3, 3, 3, 3, 4]}, 'directions': {'1': [LEFT, DOWN, RIGHT, DOWN, LEFT], '2': [RIGHT, LEFT, DOWN, RIGHT, DOWN, LEFT]}},
                '6': {'width': 3, 'moves': {'1': [3, 6, 3, 3, 3], '2': [3, 3, 6, 3, 3, 3]}, 'directions': {'1': [LEFT, DOWN, RIGHT, UP, LEFT], '2': [RIGHT, LEFT, DOWN, RIGHT, UP, LEFT]}},
                '7': {'width': 3, 'moves': {'1': [3, 3, 7], '2': [3, 7]}, 'directions': {'1': [LEFT, RIGHT, DOWN], '2': [RIGHT, DOWN]} },
                '8': {'width': 3, 'moves': {'1': [3, 6, 3, 6, 3, 3], '2': [3, 6, 3, 6, 3, 3]}, 'directions': {'1': [LEFT, DOWN, RIGHT, UP, DOWN, LEFT], '2': [RIGHT, DOWN, LEFT, UP, DOWN, RIGHT]}},
                '9': {'width': 3, 'moves': {'1': [3, 3, 3, 3, 7], '2': [3, 6, 3, 3, 3]}, 'directions': {'1': [LEFT, DOWN, RIGHT, UP, DOWN], '2': [RIGHT, DOWN, UP, LEFT, UP]}},
                }