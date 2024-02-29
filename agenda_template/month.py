import numpy as np


class Month():
    def __init__(self, name, nb_days, d0, week_template):
        self.name = name
        self.nb_days = nb_days
        self.d0 = d0
        self.grid = self.gen_grid()
        self.week_template = week_template


    def gen_grid(self):
        """Defines an integer grid for the month.
        Each row defines a week, each collumn is a weekday. Cell values are the date for that day, or 0 otherwise.
        Example: month of 30 days, starting on a tuesday:
            [[ 0.,  1.,  2.,  3.,  4.,  5.,  6.],
            [ 7.,  8.,  9., 10., 11., 12., 13.],
            [14., 15., 16., 17., 18., 19., 20.],
            [21., 22., 23., 24., 25., 26., 27.],
            [28., 29., 30.,  0.,  0.,  0.,  0.]]
        """
        grid = np.arange(start=1, stop=self.nb_days+1)  # list of days
        grid = np.concatenate([np.zeros(self.d0),grid])  # add 0s before first days of month for empty cells
        if grid.shape[0]%7 != 0: # if the month does not finish on a Sunday (else, it is already ready to rescale)
            grid = np.concatenate([grid, np.zeros(7 - grid.shape[0] % 7)])  # add 0s to reach size k*7
        return grid.reshape((-1,7)).astype(np.int32)  # rescale 1 week per row


    def gen_html(self):
        """Returns a list of html pages for the month."""
        html_list = []
        for week_idx, week in enumerate(self.grid):
            html_list += self.week_template.gen_html(self.name, week, week_idx)

        return html_list
