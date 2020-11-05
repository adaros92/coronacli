import numpy as np

from tabulate import tabulate


class TruncatedDisplay(object):
    """ Performs similar functionality as less command in unix OS where stdout is chunked up into a set number of
    lines and user needs to provide input to continue displaying lines """

    def __init__(self, num_lines=10):
        # TODO make num_lines config driven
        self.num_lines = num_lines

    def __ror__(self, other):
        s = str(other).split("\n")
        # Print only self.num_lines from the string to print
        for i in range(0, len(s), self.num_lines):
            print(*s[i: i + self.num_lines], sep="\n")
            # Prompt the user if they want to continue displaying line batches or not
            val = input('Press <Enter> to continue or <q> to quit\n')
            if val == 'q':
                exit(0)


class DataFrameTabularDisplay(object):
    """ Displays entire data frame in psql command line format """

    def __init__(self, data_frame):
        self.data_frame = data_frame

    def run(self):
        printable_df = self.data_frame.reset_index().drop(columns='index')
        print(tabulate(printable_df, headers='keys', tablefmt='psql'))


class DataFrameTruncatedDisplay(object):
    """ Displays batches of lines from a data frame """

    def __init__(self, data_frame, num_lines=10):
        # TODO make num_lines config driven
        self.data_frame = data_frame
        self.num_lines = num_lines

    def run(self):
        # Start by printing out the column names of the data frame
        string_to_print = ''
        row_count = 0
        # Then print batches of self.num_lines
        for index, row in self.data_frame.iterrows():
            if row_count % (self.num_lines - 1) == 0:
                string_to_print += '   '.join([column.upper() for column in self.data_frame.columns])
                string_to_print += '\n'
            row_dict = dict(np.ndenumerate(row))
            string_to_print += '   '.join(map(str, row_dict.values()))
            string_to_print += '\n'
            row_count += 1
        # Given text with strings separated by \n, this will print each line similar to the unix less command
        display = TruncatedDisplay(self.num_lines)
        string_to_print[:-1] | display


def get_display(display_option="truncated_df"):
    """ Factory function to retrieve a particular display type from a given display option

    :param string display_option: a config driven option for how to display results to the user
    :returns a display class corresponding to the display_option given
    """
    # TODO make display_option config driven
    available_displays = {
        "truncated_df": DataFrameTruncatedDisplay,
        "truncated": TruncatedDisplay,
        "tabular_df": DataFrameTabularDisplay
    }
    if display_option not in available_displays:
        raise KeyError("{0} display not one of {1}".format(display_option, set(available_displays)))
    return available_displays[display_option]
