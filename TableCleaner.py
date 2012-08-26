import sublime, sublime_plugin
import re, os, sys

class TableCleanerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        positions = self.get_separators_positions(self.selected_lines(), ["|"])

        if positions:
            self.align(positions, edit)

    # Get the string containing the line
    def get_line(self, line_num):
        return self.view.substr(self.view.full_line(self.view.text_point(line_num, 0)))

    # Get an array containing the selected lines
    def selected_lines(self):
        view = self.view
        sel = view.sel()
        line_nums = [view.rowcol(line.a)[0] for line in view.lines(sel[0])]
        return [(line, self.get_line(line)) for line in line_nums]

    # Find the positions of the separators
    def get_separators_positions(self, lines, separators):
        res = []
        for line in lines:
            s = line[1]
            positions = [x for x in xrange(0, len(s)) if s[x] in separators]
            if positions:
                res.append((line[0], positions))

        return res

    # Perform the alignment
    def align(self, positions, edit):
        cols_num = min([len(line[1]) for line in positions])
        rows_num = len(positions)

        # How much has each row been shifted
        cols_shift = [0] * rows_num

        for i in xrange(1, cols_num):
            lines = [x[0] for x in positions]

            # Get the previous cols and update them with the shifts made so far
            prev_cols = [x[1][i-1] for x in positions]
            cols = [x[1][i] for x in positions]

            # Get the cols and update them with the shifts made so far
            cols = [i+j for i, j in zip(cols, cols_shift)]
            prev_cols = [i+j for i, j in zip(prev_cols, cols_shift)]

            max_col = max(cols)

            for j in xrange(0, rows_num):
                difference = max_col - cols[j]
                cols_shift[j] += difference

                left_dif  = difference / 2
                right_dif = difference - left_dif

                # The left point and the right point for the current cell of
                # the table
                left_point = self.view.text_point(lines[j], prev_cols[j]+1)
                right_point = self.view.text_point(lines[j], cols[j] + left_dif)

                self.view.insert(edit, left_point,  " " * left_dif)
                self.view.insert(edit, right_point, " " * right_dif)





