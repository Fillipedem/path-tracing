import regex

SPACE_REGEX = '[ ]+'

def read_lines(f: str):

    def remove_spaces(line):
        line = regex.sub(SPACE_REGEX, ' ', line)
        return line.strip()

    lines = []
    for line in f.split('\n'):
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue 
        lines.append(remove_spaces(line))

    return lines

def to_int(input):
    return list(map(int, input))

def to_float(input):
    return list(map(float, input))
