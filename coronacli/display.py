from tabulate import tabulate


class TruncatedDisplay(object):
    """ Performs similar to less command in unix OS where stdout is chunked up into a set number of
    lines and user needs to provide input to continue displaying lines """
    def __init__(self, num_lines):
        self.num_lines = num_lines

    def __ror__(self, other):
        s = str(other).split("\n")
        for i in range(0, len(s), self.num_lines):
            print(*s[i: i + self.num_lines], sep="\n")
            val = input("Press <Enter> for more or <q> to quit\n")
            if val == 'q':
                exit(0)


class Output(object):

    def __init__(self, data_frame):
        self.data_frame = data_frame

    def run(self):
        prinatable_df = self.data_frame.reset_index().drop(columns="index")
        print(tabulate(prinatable_df, headers='keys', tablefmt='psql'))
        '''
        less = display.TruncatedDisplay(num_lines=50)
        "\n".join([str(x) for x in range(100)]) | less'''
