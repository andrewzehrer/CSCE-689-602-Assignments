N = 8
N_SQ = N**2

write_to_file = False # change to True when ready 

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

# -------- Main Execution --------

output_lines = []
num_rules = 0

# Uncomment what you want to generate
# num_rules = one_queen_each_row(num_rules, output_lines)
# num_rules = one_queen_each_col(num_rules, output_lines)
# num_rules = not_two_queens_each_row(num_rules, output_lines)

output_stream = "\n".join(output_lines)

print(f"p cnf {N_SQ} {num_rules}\n")
print(output_stream)

if write_to_file:
    with open(f"{N}queens.cnf", "w") as file:
        file.write(output_stream)