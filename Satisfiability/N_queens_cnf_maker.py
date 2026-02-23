N = 8
N_SQ = N**2

def one_queen_each_row(rules: int, output_lines: list):
    num_rules = rules
    index = 1
    temp_str = ""

    while index <= N_SQ:
        if index % N != 0:
            if index < 10:
                temp_str += " "
            temp_str += str(index) + " "
        else:
            if index < 10:
                temp_str += " "
            temp_str += str(index) + " 0\n"
            num_rules += 1
        index += 1

    output_lines.append("c each row has at least one queen\n")
    output_lines.append(temp_str)

    return num_rules

def one_queen_each_col(rules: int, output_lines: list):
    num_rules = rules
    index = 1
    temp_str = ""

    while index <= N_SQ:
        if index < 10:
            temp_str += " "
        temp_str += str(index) + " "

        index += N

        if index == N_SQ:
            temp_str += str(index) + " 0\n"
            num_rules += 1
            break

        if index > N_SQ:
            temp_str += "0\n"
            num_rules += 1
            index -= (N_SQ - 1)

    output_lines.append("c each col has at least one queen\n")
    output_lines.append(temp_str)

    return num_rules

def not_two_queens_each_row(rules: int, output_lines: list):
    num_rules = rules
    index = 1
    temp_str = ""

    while (index < N_SQ):
        working_list = []
        for x in range(index, index+N):
            working_list.append(x)

        # find all pairs in the working list
        for i in range(len(working_list)):
            for j in range(i + 1, len(working_list)):
                if working_list[i] < 10: temp_str += " -" + str(working_list[i])
                else: temp_str += "-" + str(working_list[i])

                if working_list[j] < 10: temp_str += "  -" + str(working_list[j]) + " 0\n"
                else: temp_str += " -" + str(working_list[j]) + " 0\n"
                num_rules += 1
        
        temp_str += "\n"
        index += N

    output_lines.append("c each row has no more than one queen\n")
    output_lines.append(temp_str)

    return num_rules

def not_two_queens_each_col(rules: int, output_lines: list):
    num_rules = rules
    index = 1
    temp_str = ""

    while (index <= N):
        working_list = []
        x = index
        while x <= N_SQ:
            working_list.append(x)
            x += N

        # find all pairs in the working list
        for i in range(len(working_list)):
            for j in range(i + 1, len(working_list)):
                if working_list[i] < 10: temp_str += " -" + str(working_list[i])
                else: temp_str += "-" + str(working_list[i])

                if working_list[j] < 10: temp_str += "  -" + str(working_list[j]) + " 0\n"
                else: temp_str += " -" + str(working_list[j]) + " 0\n"
                num_rules += 1
        
        temp_str += "\n"
        index += 1

    output_lines.append("c each column has no more than one queen\n")
    output_lines.append(temp_str)

    return num_rules

def check_left_right_diagonals(rules: int, output_lines: list):
    num_rules = rules
    diagonal_starters = list(range(1,N)) + [N*k + 1 for k in range(1, N-1)]
    temp_str = ""

    for x in diagonal_starters:
        working_list = []
        if x < N:
            limit = N - x + 1
        else:
            limit = N
        while x <= N_SQ and len(working_list) < limit:
            working_list.append(x)
            x += N + 1

        # find all pairs in the working list
        for i in range(len(working_list)):
            for j in range(i + 1, len(working_list)):
                if working_list[i] < 10: temp_str += " -" + str(working_list[i])
                else: temp_str += "-" + str(working_list[i])

                if working_list[j] < 10: temp_str += "  -" + str(working_list[j]) + " 0\n"
                else: temp_str += " -" + str(working_list[j]) + " 0\n"
                num_rules += 1
        
        temp_str += "\n"
        
    output_lines.append("c check left-right diagonals\n")
    output_lines.append(temp_str)

    return num_rules

def check_right_left_diagonals(rules: int, output_lines: list):
    num_rules = rules
    diagonal_starters = list(range(2, N+1)) + [N*k for k in range(2, N)]
    temp_str = ""

    for x in diagonal_starters:
        working_list = []
        if x < N:
            limit = x
        else:
            limit = N
        while x <= N_SQ and len(working_list) < limit:
            working_list.append(x)
            x += N - 1

        # find all pairs in the working list
        for i in range(len(working_list)):
            for j in range(i + 1, len(working_list)):
                if working_list[i] < 10: temp_str += " -" + str(working_list[i])
                else: temp_str += "-" + str(working_list[i])

                if working_list[j] < 10: temp_str += "  -" + str(working_list[j]) + " 0\n"
                else: temp_str += " -" + str(working_list[j]) + " 0\n"
                num_rules += 1
        
        temp_str += "\n"
        
    output_lines.append("c check right-left diagonals\n")
    output_lines.append(temp_str)

    return num_rules

# -------- Main Execution --------

output_lines = []
num_rules = 0

num_rules = one_queen_each_row(num_rules, output_lines)
num_rules = one_queen_each_col(num_rules, output_lines)
num_rules = not_two_queens_each_row(num_rules, output_lines)
num_rules = not_two_queens_each_col(num_rules, output_lines)
num_rules = check_left_right_diagonals(num_rules, output_lines)
num_rules = check_right_left_diagonals(num_rules, output_lines)

output_stream = "\n".join(output_lines)

print(f"p cnf {N_SQ} {num_rules}")
# print(output_stream)

write_to_file = False

if write_to_file:
    with open(f"{N}queens.cnf", "w") as file:
        file.write(f"p cnf {N_SQ} {num_rules}\n")
        file.write(output_stream)
        print(f"Wrote rules to file {file.name}\n")