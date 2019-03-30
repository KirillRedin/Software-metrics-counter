import re


class LinesCounter:
    def __init__(self):
        self.empty_lines_amount = 0
        self.physical_lines_amount = 0
        self.logical_lines_amount = 0
        self.comments_amount = 0


    def count_lines(self, name):
        file = open(name, 'r')

        lines_amount = 0

        for line in file:
            lines_amount += 1

            # Check if line is empty
            if not line.strip():
                self.empty_lines_amount += 1
            else:
                self.analyze_line(line)

        self.get_physical_lines_amount(lines_amount)


    def analyze_line(self, line):
        line = self.clear_line(line)

        if self.line_is_comment(line):
            self.comments_amount += 1
        else:
            if self.line_has_comment(line):
                self.comments_amount +=1

        return line


    def clear_line(self, line):
        # Remove metacharacters ' and " escaped with \ so we can correctly recognize phrases in "..." and '...'
        line = re.sub(r'\\[\'\"]', '', line)
        # Remove phrases in '...' and "..." to avoid quoted text recognition
        line = re.sub(r'\'[^\']*\'', '', line)
        line = re.sub(r'(\"[^\"]*\")', '', line)
        return line


    def line_is_comment(self, line):
        return line[0]=='#'


    def line_has_comment(self, line):
        result = re.findall(r'#.*', line)
        print(result)
        return result


    def get_physical_lines_amount(self, lines_amount):
        # If ratio of empty lines to all lines is more than 25%,
        # only 25% of empty lines are counted in physical lines amount
        if self.empty_lines_amount / lines_amount > 0.25:
            self.physical_lines_amount = int(lines_amount - self.empty_lines_amount * 0.75)
        else:
            self.physical_lines_amount = lines_amount


    def print_result(self):
        print('Physical lines amount: %d' % (self.physical_lines_amount))
        print('Comments amount: %d' % (self.comments_amount))
        print('Empty lines amount: %d' % (self.empty_lines_amount))


p = LinesCounter()
p.count_lines('euro_diffusion.py')
p.print_result()

