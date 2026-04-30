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


# read and parse a knowledge base file
def parse_kb_file(filename):
    with open(filename, "r") as f:
        text = f.read()

    tokens = tokenize(text)
    expressions = []

    # parse multiple top-level expressions
    while tokens:
        expressions.append(parse(tokens))

    kb = []

    for expr in expressions:
        # rule: (implies body head)
        if isinstance(expr, list) and len(expr) == 3 and expr[0] == "implies":
            body = expr[1]
            head = expr[2]
            kb.append(("rule", body, head))
        else:
            # treat everything else as a fact
            kb.append(("fact", expr))

    return kb


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
# proving
# ----------------------------

def prove(goal, kb, subst):
    results = []

    for item in kb:
        if item[0] == "fact":
            fact = item[1]
            new_subst = unify(goal, fact, subst.copy())
            if new_subst is not None:
                results.append(new_subst)

        elif item[0] == "rule":
            body, head = item[1], item[2]

            new_subst = unify(goal, head, subst.copy())
            if new_subst is not None:
                results.extend(prove_body(body, kb, new_subst))

    return results


def prove_body(body, kb, subst):
    # handle (and ...)
    if isinstance(body, list) and body[0] == "and":
        results = [subst]
        for subgoal in body[1:]:
            new_results = []
            for s in results:
                sub_results = prove(subgoal, kb, s)
                new_results.extend(sub_results)
            results = new_results
        return results
    else:
        return prove(body, kb, subst)
    

# ----------------------------
# printing
# ----------------------------

def to_string(x):
    if is_list(x):
        return "(" + " ".join(to_string(e) for e in x) + ")"
    
    else:
        return x


def print_kb(kb):
    print("facts:")
    for item in kb:
        if item[0] == "fact":
            print(" ", to_string(item[1]))

    print("\nrules:")
    for item in kb:
        if item[0] == "rule":
            body, head = item[1], item[2]
            print(" ", f"{to_string(head)} :- {to_string(body)}") # prolog-style output


def print_results(results):
    if not results:
        print("no solutions")
        return

    for res in results:
        print("solution:")
        for var in res:
            val = to_string(substitute(res[var], res))
            print(f"  {var} = {val}")


# ----------------------------
# main
# ----------------------------

def main():
    kb = parse_kb_file("knowledge.txt")
    print_kb(kb)
    print()

    query = parse_expr("(wins ?X blastoise)")
    print("query:", to_string(query), "\n")

    results = prove(query, kb, {})
    print_results(results)


if __name__ == "__main__":
    main()