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

def index_kb(kb):
    facts = {}
    rules = {}

    for item in kb:
        if item[0] == "fact":
            pred = item[1][0]
            facts.setdefault(pred, []).append(item[1])

        elif item[0] == "rule":
            body, head = item[1], item[2]
            pred = head[0]
            rules.setdefault(pred, []).append((body, head))

    return facts, rules

# ----------------------------
# utilities
# ----------------------------

def to_string(x):
    if is_list(x):
        return "(" + " ".join(to_string(e) for e in x) + ")"
    
    else:
        return x

def is_var(x):
    return isinstance(x, str) and x.startswith("?")

def is_list(x):
    return isinstance(x, list)

def substitute(x, subst):
    # recursively apply substitutions
    while is_var(x) and x in subst:
        x = subst[x]

    if is_list(x):
        return [substitute(e, subst) for e in x]

    return x

def occurs(var, x, subst):
    x = substitute(x, subst)
    if var == x:
        return True
    
    if is_list(x):
        return any(occurs(var, xi, subst) for xi in x)
    
    return False

# ----------------------------
# standardization
# ----------------------------

counter = 0

def standardize_apart(expr, mapping=None):
    global counter
    if mapping is None:
        mapping = {}

    if is_var(expr):
        if expr not in mapping:
            counter += 1
            mapping[expr] = f"?{expr[1:]}_{counter}"
        return mapping[expr]

    elif is_list(expr):
        return [standardize_apart(e, mapping) for e in expr]

    else:
        return expr

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

goal_cache = {}

def prove(goal, kb_index, subst, trace=False, depth=0):
    facts, rules = kb_index

    goal = substitute(goal, subst)
    key = to_string(goal)

    # memoization (prevents repetition explosion)
    if key in goal_cache:
        return goal_cache[key]

    trace_print(trace, depth, f"prove: {key}")

    # equality
    if isinstance(goal, list) and goal[0] == "=":
        x, y = goal[1], goal[2]
        new_subst = unify(x, y, subst.copy())
        return [new_subst] if new_subst is not None else []

    # inequality
    if isinstance(goal, list) and goal[0] == "not":
        inner = goal[1]
        if isinstance(inner, list) and inner[0] == "=":
            x, y = inner[1], inner[2]
            new_subst = unify(x, y, subst.copy())
            return [] if new_subst is not None else [subst]

    results = []

    if not isinstance(goal, list):
        return []

    pred = goal[0]

    # facts
    for fact in facts.get(pred, []):
        new_subst = unify(goal, fact, subst.copy())
        if new_subst is not None:
            trace_print(trace, depth, f"  fact: {to_string(fact)}")
            results.append(new_subst)

    # rules
    for body, head in rules.get(pred, []):
        mapping = {}
        body2 = standardize_apart(body, mapping)
        head2 = standardize_apart(head, mapping)

        new_subst = unify(goal, head2, subst.copy())
        if new_subst is not None:
            trace_print(trace, depth, f"  rule: {to_string(head)}")
            results.extend(prove_body(body2, kb_index, new_subst))

    return results

def prove_body(body, kb_index, subst, trace=False, depth=0):
    if isinstance(body, list) and body[0] == "and":
        return prove_and(body[1:], kb_index, [subst], trace, depth)
    else:
        return prove(body, kb_index, subst, trace, depth)

def prove_and(goals, kb_index, states, trace, depth):
    if not goals:
        return states

    first, *rest = goals
    new_states = []

    for s in states:
        subgoal = substitute(first, s)
        results = prove(subgoal, kb_index, s, trace, depth+1)
        new_states.extend(results)

    return prove_and(rest, kb_index, new_states, trace, depth)

def normalize_solution(res, query_vars):
    out = {}
    for var in query_vars:
        if var in res:
            val = fully_resolve(res[var], res)
            out[var] = to_string(val)
    return tuple(sorted(out.items()))
    
# ----------------------------
# printing
# ----------------------------

def trace_print(trace, depth, msg):
    if trace:
        print("  " * depth + msg)

def get_vars(expr):
    if is_var(expr):
        return [expr]
    elif is_list(expr):
        out = []
        for e in expr:
            out.extend(get_vars(e))
        return out
    return []

def fully_resolve(var, subst):
    while is_var(var) and var in subst:
        var = subst[var]
    return var

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

def print_results(results, query):
    if not results:
        print("no solutions")
        return

    query_vars = get_vars(query)

    for res in results:
        print("solution:")

        for var in query_vars:
            if var in res:
                val = fully_resolve(res[var], res)
                print(f"  {var} = {to_string(val)}")

def print_query_results(results, query):
    query_vars = list(set(get_vars(query)))

    seen = set()
    found = False

    for res in results:
        norm = normalize_solution(res, query_vars)

        if norm in seen:
            continue
        seen.add(norm)

        found = True
        for var, val in norm:
            print(f"{var} = {val}")
        print()

    if not found:
        print("no solutions\n")

# ----------------------------
# main
# ----------------------------

def repl(kb_index):
    print("Enter queries in S-expression form. Type 'exit' to quit.\n")

    while True:
        try:
            line = input("> ").strip()

            if not line:
                continue

            if line.lower() in ["exit", "quit"]:
                break

            query = parse_expr(line)

            # clear cache per query
            global goal_cache
            goal_cache = {}

            results = prove(query, kb_index, {}, trace=False)

            print_query_results(results, query)

        except Exception as e:
            print("error:", e, "\n")

def main():
    kb = parse_kb_file("knowledge.txt")
    kb_index = index_kb(kb)

    print("KB loaded.")
    repl(kb_index)

if __name__ == "__main__":
    main()