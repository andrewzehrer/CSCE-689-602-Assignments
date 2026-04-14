# unify.py

import sys
import re

# ----------------------------
# parsing
# ----------------------------

def tokenize(s):
    # split into parentheses and atoms
    return re.findall(r'\(|\)|[^\s()]+', s)

def parse(tokens):
    # recursive descent parser for s-expressions
    if len(tokens) == 0:
        raise ValueError("unexpected EOF")

    token = tokens.pop(0)

    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(parse(tokens))

        tokens.pop(0)  # removes ')'

        return lst
    
    elif token == ')':
        raise ValueError("unexpected )")
    
    else:
        return token

def parse_expr(s):
    return parse(tokenize(s))


# ----------------------------
# utilities
# ----------------------------

def is_var(x):
    return isinstance(x, str) and x.startswith("?")

def is_list(x):
    return isinstance(x, list)


# ----------------------------
# substitution
# ----------------------------

def substitute(x, subst):
    # recursively apply substitutions
    while is_var(x) and x in subst:
        x = subst[x]

    if is_list(x):
        return [substitute(e, subst) for e in x]

    return x


# ----------------------------
# check occurrence
# ----------------------------

def occurs(var, x, subst):
    x = substitute(x, subst)
    if var == x:
        return True
    
    if is_list(x):
        return any(occurs(var, xi, subst) for xi in x)
    
    return False


# ----------------------------
# unification
# ----------------------------

def unify(x, y, subst):
    x = substitute(x, subst)
    y = substitute(y, subst)

    if x == y:
        return subst

    if is_var(x):
        return unify_var(x, y, subst)

    if is_var(y):
        return unify_var(y, x, subst)

    if is_list(x) and is_list(y):
        if len(x) != len(y):
            return None
        
        for xi, yi in zip(x, y):
            subst = unify(xi, yi, subst)
            if subst is None:
                return None
            
        return subst

    return None


def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)

    if is_var(x) and x in subst:
        return unify(var, subst[x], subst)

    if occurs(var, x, subst):
        return None

    subst[var] = x
    return subst


# ----------------------------
# printing
# ----------------------------

def to_string(x):
    if is_list(x):
        return "(" + " ".join(to_string(e) for e in x) + ")"
    
    else:
        return x


# ----------------------------
# main
# ----------------------------

def main():
    if len(sys.argv) != 3:
        print("usage: python unify.py \"expr1\" \"expr2\"")
        return

    expr1 = parse_expr(sys.argv[1])
    expr2 = parse_expr(sys.argv[2])

    subst = unify(expr1, expr2, {})

    if subst is None:
        print("failure")
        return

    # print substitutions
    for var in subst:
        val = substitute(subst[var], subst)
        print(f"{var} -> {to_string(val)}")

    # print unified expressions
    e1 = to_string(substitute(expr1, subst))
    e2 = to_string(substitute(expr2, subst))
    print(f"{e1} = {e2}")


if __name__ == "__main__":
    main()