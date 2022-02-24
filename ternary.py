# author: @robintan, 2021

input_file_name = 'input.txt'
output_file_name = "output.txt"

#############################################################

class Conditional:

    def __init__(self, trueLogic="", trueStatement="", parent=None, logicComment=""):
        self.trueLogic = trueLogic
        self.trueStatement = trueStatement
        self.parent = parent
        self.if_child = None
        self.else_child = None
        self.logicComment = logicComment
        self.if_mode = True
        self.spacing = 0

def fill_output(curr, output):
    if (len(curr.trueLogic) > 0):
        first_line = []
        for i in range(curr.spacing):
            first_line.append(" ")
        first_line.append("(")
        first_line.append(curr.trueLogic)
        first_line.append(") ?")
        if (len(curr.logicComment) > 0):
            first_line.append(" ")
            first_line.append(curr.logicComment)
        
        first_line = ''.join(first_line)
        output.append(first_line)

        if curr.if_child is None:
            second_line = []
            for i in range(curr.spacing + 2):
                second_line.append(" ")
            second_line.append(curr.trueStatement)
            second_line.append(" :")
            second_line = ''.join(second_line)
            output.append(second_line)
        else:
            second_line_a = []
            for i in range(curr.spacing + 2):
                second_line_a.append(" ")
            second_line_a.append("(")
            second_line_a = ''.join(second_line_a)
            output.append(second_line_a)

            fill_output(curr.if_child, output)

            second_line_b = []
            for i in range(curr.spacing + 2):
                second_line_b.append(" ")
            second_line_b.append(") :")
            second_line_b = ''.join(second_line_b)
            output.append(second_line_b)

        if len(curr.else_child.trueLogic) > 0:
            third_line = []
            for i in range(curr.spacing + 4):
                third_line.append(" ")
            third_line.append("(")
            third_line = ''.join(third_line)
            output.append(third_line)

            fill_output(curr.else_child, output)

            fourth_line = []
            for i in range(curr.spacing + 4):
                fourth_line.append(" ")
            if curr.parent.else_child is None or curr.parent.else_child is curr:
                fourth_line.append(")")
            else:
                fourth_line.append(") :")
            fourth_line = ''.join(fourth_line)
            output.append(fourth_line)
        else:
            fill_output(curr.else_child, output)

    else:
        if curr.parent is not None:
            first_line = []
            for i in range(curr.spacing):
                first_line.append(" ")
            first_line.append(curr.trueStatement)
            first_line = ''.join(first_line)
            output.append(first_line)
        else:
            fill_output(curr.if_child, output)

#############################################################

dummy = Conditional()
dummy.if_mode = True
dummy.spacing = -4
stack = [dummy]

output_file = open(output_file_name, 'w')
input_file = open(input_file_name, 'r')

for line in input_file:

    line = line.strip().split()
    if len(line) == 0:
        continue
    if line[0] == "if":
        trueLogic = []
        index = 1
        while index < len(line):
            if line[index] == "//":
                break
            trueLogic.append(line[index])
            index += 1

        logicComment = []
        while index < len(line):
            logicComment.append(line[index])
            index += 1
        
        trueLogic = ' '.join(trueLogic)
        logicComment = ' '.join(logicComment)

        curr = Conditional(trueLogic, "", stack[-1], logicComment)
        if len(stack) > 0:
            if stack[-1].if_mode:
                curr.spacing = stack[-1].spacing + 4
                stack[-1].if_child = curr
            else:
                curr.spacing = stack[-1].spacing + 6
                stack[-1].else_child = curr
        stack.append(curr)
    elif line[0] == "else":
        stack[-1].if_mode = False
    else:
        trueStatement = []
        index = 0
        while index < len(line):
            trueStatement.append(line[index])
            index += 1
        trueStatement = ' '.join(trueStatement)

        if not stack[-1].if_mode:
            last = stack.pop()
            last.else_child = Conditional("", trueStatement, last, "")
            last.else_child.spacing = last.spacing + 4

            while not stack[-1].if_mode:
                stack.pop()
        else:
            stack[-1].trueStatement = trueStatement

output = []
root = dummy.if_child
fill_output(root, output)

for line in output:
    output_file.write(line)
    output_file.write("\n")

input_file.close()
output_file.close()
