def combine(l):
    if len(l) > 3:
        return l
    one_state = ()
    for row in l:
        one_state+=tuple(row)
    return tuple(one_state)


def get_turn(state):
    if combine(state).count('x') == combine(state).count('o'):
        return 'x'
    else:
        return 'o'


def chunks(l, n):
    if len(l) == n:
        return l
    if '\!' in l or 'T' in l:
        return l
    return tuple([l[i:i+n] for i in range(0, len(l), n)])


def eval_state(state):
    state = chunks(state, 3)
    for row in state:
        if row[0]==row[1]==row[2] and row[0] != 0:
            return row[0]
    for i in range(3):
        if state[0][i]==state[1][i]==state[2][i] and state[0][i]!=0:
            return state[0][i]
    if state[0][0]==state[1][1]==state[2][2] and state[0][0]!=0:
        return (state[0][0])
    if state[0][2]==state[1][1]==state[2][0] and state[0][2]!=0:
        return (state[2][0])
    for row in state:
        if 0 in row:
            return state
    return 't'


def pp(state):
    evalu = eval_state(state)
    if len(evalu) < 2:
        print(evalu.upper()+'\n')

    for row in state:
        row = str(row[0])+" | "+str(row[1])+" | "+str(row[2])
        print(row.replace("0", " "))
        print("---------")
    print('\n')


def get_term(dct):
    val = list(dct.values())[0][0]
    if isinstance(val, int):
        return val
    else:
        return False


def remove_sym(states):
    good_states = []
    for state in states:
        state = chunks(state,3)
        if tuple(state) in good_states:
            continue
        elif tuple([row[::-1] for row in state]) in good_states:
            continue
        #90
        new_state = []
        for i in range(2, -1, -1):
            new_row = []
            for row in tuple([row[::-1] for row in state]):
                new_row.append(row[i])
            new_state.append(tuple(new_row[::-1]))
        if tuple(new_state) in good_states:
            continue
        #90R
        new_state = []
        for i in range(2, -1, -1):
            new_row = []
            for row in state:
                new_row.append(row[i])
            new_state.append(tuple(new_row[::-1]))
        if tuple(new_state) in good_states:
            continue
        #180
        new_state = []
        for i in range(2, -1, -1):
            try:
                new_state.append(tuple(state[i][::-1]))
            except:
                if tuple(new_state) in good_states:
                    continue
        #180R
        new_state = []
        for i in range(2, -1, -1):
            new_state.append(state[i])
        if tuple(new_state) in good_states:
            continue
        #270
        new_state = []
        for i in range(2, -1, -1):
            new_row = []
            for row in state:
                new_row.append(row[i])
            new_state.append(tuple(new_row))
        if tuple(new_state) in good_states:
            continue
        #270R
        new_state = []
        for i in range(2, -1, -1):
            new_row = []
            for row in tuple([row[::-1] for row in state]):
                new_row.append(row[i])
            new_state.append(tuple(new_row))
        if tuple(new_state) in good_states:
            continue
        else:
            good_states.append(state)
    good_states = [combine(state) for state in good_states]
    return good_states


def get_submap(state, tree):
    for dct in next(iter(tree.values())):
        if isinstance(dct, dict):
            if len(remove_sym([state, combine(next(iter(dct)))])) == 1:
                return dct
