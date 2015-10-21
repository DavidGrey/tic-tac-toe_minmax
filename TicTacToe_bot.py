from itertools import permutations
from TicTacToe_Assist import *


def successors(state, final):
    if combine(state).count('x') > combine(state).count('o'):
        letter = 'o'
    else:
        letter = 'x'
    state = chunks(state, 3)
    variables = [0]*combine(state).count(0)
    variables[0] = letter
    variables = list(set(permutations(variables)))
    states = []
    for var in variables:
        new_board = []
        state = chunks(state, 3)
        for row in state:
            new_row = []
            for tile in row:
                if tile != 0:
                    new_row.append(tile)
                else:
                    new_row.append(var[0])
                    var = var[1:]
            new_board.append(tuple(new_row))
        if eval_state(new_board) == letter:
            if final:
                return new_board
            return{state:[letter]}
        states.append(combine(tuple(new_board)))
    return {state:[eval_state(state) for state in remove_sym(states)]}


def gen_map(dct_map):
    term = False
    new_val = []
    key = tuple(dct_map.keys())[0]
    dct_val = dct_map[key]
    if 'x' in dct_val:
        dct_map[key] = [1]
        term = True
    if 't' in dct_val:
        dct_map[key] = [0]
        term = True
    if 'o' in dct_val:
        dct_map[key] = [-1]
        term = True
    if term:    
        return dct_map
    for val in dct_val:
        if isinstance(val, tuple):
                new_val.append(gen_map(successors(val, False)))
        elif isinstance(val, dict):
                new_val.append(gen_map(successors))
    dct_map[key] = new_val
    return dct_map


def fill_in(tree):
    terms = []
    for dct in list(tree.values())[0]:
        term_len = len(terms)
        if list(dct.values())[0][0] == 1:
            terms += [1]
        if list(dct.values())[0][0] == 0:
            terms += [0]
        if list(dct.values())[0][0] == -1:
            terms += [-1]
        if len(terms) == term_len:
            terms += [get_term(fill_in(dct))]
    key = next(iter(tree))
    if combine(key).count('x') == combine(key).count('o'):
        tree[key] = [max(terms)]+tree[key]
    else:
        tree[key] = [min(terms)]+tree[key]
    return tree


def play(game_map):
    game_on = True
    state = (0,)*9
    while game_on:
        if get_turn(state) == 'x':
            val = list(game_map.values())[0]
            for dct in val[1:]:
                if list(dct.values())[0][0] == val[0]:
                    state = (list(dct)[0])
                    game_map = dct
            if game_map[state] == [1]:
                pp(tuple(successors(state, True)))
                return "You Lose"
            elif game_map[state] == [0]:
                state = combine(state)
                final = []
                for item in state:
                    if item == 0:
                        final += ['x']
                    else:
                        final += item
                pp(chunks(tuple(final),3))
                return 
            pp(state)
        if get_turn(state) == 'o':
            player_move = int(input())-1
            if isinstance(player_move, int):
                if player_move >= 0 and player_move < 9:
                    state = combine(state)
                    if state[player_move] == 0:
                        lst = list(state)
                        lst[player_move] = 'o'
                        state = chunks(tuple(lst), 3)
                        game_map = get_submap(state, game_map)
                        moved = True
                        
            if moved:
                moved = False
            else:
                print("Invalid Key entry") 
                    

game_map = fill_in(gen_map(successors((0,)*9, False)))

play(game_map)
