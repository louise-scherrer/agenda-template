import numpy as np
import calendar
import os.path
from agenda_template import AGENDA_TEMPLATE_DIR, AGENDA_RESSOURCES_DIR
from agenda_template import utils, almanac


MONTHS_DICT = {
    1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun',
    7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'
}


class Template():
    def __init__(self, cfg, year, month):
        self.cfg = cfg
        self.d0, self.nb_days = calendar.monthrange(year, month)
        self.nb_weeks = (self.d0 + self.nb_days - 1) // 7 + 1  # number of weeks in month (4, 5, or 6)
        self.month_name = cfg.months[MONTHS_DICT[month]]
        self.year = year

        ## load css
        with open(os.path.join(AGENDA_TEMPLATE_DIR, 'style.css'), 'r') as f:
            self.css = f.read()

        ## general params
        self.css = self.css.replace('MY_FONT', f'{self.cfg.font}')
        self.css = self.css.replace('TEXT_SIZE', f'{self.cfg.font_size.body}')
        self.css = self.css.replace('WEEK_TITLE_SIZE', f'{self.cfg.font_size.week_title}')
        self.css = self.css.replace('MONTH_TITLE_SIZE', f'{self.cfg.font_size.month_title}')
        self.css = self.css.replace('MONTH_GRID_SIZE', f'{self.cfg.font_size.month_grid}')
        self.css = self.css.replace('LINE_SIZE', f'{self.cfg.line_size}')

        ## page params
        self.css = self.css.replace('PAGE_WIDTH', f'{self.cfg.page.width}')
        self.css = self.css.replace('PAGE_HEIGHT', f'{self.cfg.page.height}')
        self.css = self.css.replace('PAGE_BORDER_SIZE', f'{"1px" if self.cfg.page.display_borders else 0}')
        self.css = self.css.replace('PAGE_ALTERNATE_MARGIN', f'{"auto" if self.cfg.page.alternate_align else "none"}')
        self.css = self.css.replace('PAGE_ALTERNATE_BORDER', f'{"none solid solid" if self.cfg.page.alternate_align else "solid solid none"}')
        self.css = self.css.replace('PAGE_MARGIN_TOP', f'{self.cfg.page.padding.top}')
        self.css = self.css.replace('PAGE_MARGIN_BOT', f'{self.cfg.page.padding.bot}')
        self.css = self.css.replace('PAGE_MARGIN_INNER', f'{self.cfg.page.padding.inner_side}')
        self.css = self.css.replace('PAGE_MARGIN_OUTER', f'{self.cfg.page.padding.outer_side}')

        ## week page spacing
        self.css = self.css.replace('SPACE_WEEK_TITLE_TOP', f'{self.cfg.spacing.week_title.top}')
        self.css = self.css.replace('SPACE_WEEK_TITLE_LEFT', f'{self.cfg.spacing.week_title.left}')
        self.css = self.css.replace('SPACE_WEEK_CELL_TOP', f'{self.cfg.spacing.week_cell.top}')
        self.css = self.css.replace('SPACE_WEEK_CELL_LEFT', f'{self.cfg.spacing.week_cell.left}')
        self.css = self.css.replace('SPACE_BOX_CELL_TOP', f'{self.cfg.spacing.box.top}')
        self.css = self.css.replace('SPACE_BOX_CELL_RIGHT', f'{self.cfg.spacing.box.right}')
        self.css = self.css.replace('SPACE_BOX_CELL_BOT', f'{self.cfg.spacing.box.bot}')
        self.css = self.css.replace('SPACE_BOX_CELL_LEFT', f'{self.cfg.spacing.box.left}')
        self.css = self.css.replace('COLLUMN_TITLE_PADDING', f'{self.cfg.spacing.collumn_title.padding}')
        self.css = self.css.replace('COLLUMN_TITLE_TOP', f'{self.cfg.spacing.collumn_title.top}')

        ## month page spacing
        self.css = self.css.replace('SPACE_MONTH_TITLE_TOP', f'{self.cfg.spacing.month_title.top}')
        self.css = self.css.replace('SPACE_MONTH_GRID_TOP', f'{self.cfg.spacing.month_grid.top}')
        self.css = self.css.replace('SPACE_MONTH_GRID_RIGHT', f'{self.cfg.spacing.month_grid.right}')
        self.css = self.css.replace('SPACE_MONTH_GRID_BOT', f'{self.cfg.spacing.month_grid.bot}')
        self.css = self.css.replace('SPACE_MONTH_GRID_LEFT', f'{self.cfg.spacing.month_grid.left}')
        self.css = self.css.replace('SPACE_MONTH_CELL_TOP', f'{self.cfg.spacing.month_grid.cell.top}')
        self.css = self.css.replace('SPACE_MONTH_CELL_LEFT', f'{self.cfg.spacing.month_grid.cell.left}')
        self.css = self.css.replace('MONTH_GRID_WIDTH', f'{self.cfg.month_grid.width}')
        self.css = self.css.replace('MONTH_GRID_HEIGHT', f'{self.cfg.month_grid.height}')
        self.css = self.css.replace('NB_WEEKS_MONTH', f'{self.nb_weeks}')

        ## load html and insert CSS
        with open(os.path.join(AGENDA_TEMPLATE_DIR, 'week_left.html'), 'r') as f:
            self.html_week_left = f.read()

        with open(os.path.join(AGENDA_TEMPLATE_DIR, 'week_right.html'), 'r') as f:
            self.html_week_right = f.read()

        with open(os.path.join(AGENDA_TEMPLATE_DIR, 'month.html'), 'r') as f:
            self.html_month = f.read()

        self.html_week_left = self.html_week_left.replace('MY_CSS', self.css)
        self.html_week_right = self.html_week_right.replace('MY_CSS', self.css)
        self.html_month = self.html_month.replace('MY_CSS', self.css)

        ## full moons
        if self.cfg.add_moons:
            fullmoon_img = utils.image_base64(os.path.join(AGENDA_RESSOURCES_DIR, 'howling_wolf.png'))
            self.fullmoon_html = '<img src=data:image/png;base64,BINARY_CHUNKS alt=",">'.replace('BINARY_CHUNKS', fullmoon_img)
            self.moon_dates = almanac.MoonAlmanac().get_full_moon_month(year, month)
        else:
            self.moon_dates = []


    def gen_html(self):
        """Returns a list of html pages for the month.
        :returns: list of html pages
        """
        grid = self.gen_grid()
        html_list = self.gen_html_title(grid)

        for week in grid:
            html_list += self.gen_html_week(week)

        return html_list


    def gen_grid(self):
        """Defines an integer grid for the month.
        Each row defines a week, each collumn is a weekday. Cell values are the date for that day, or 0 otherwise.
        Example: month of 30 days, starting on a Tuesday:
            [[ 0,  1,  2,  3,  4,  5,  6],
            [ 7,  8,  9, 10, 11, 12, 13],
            [14, 15, 16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25, 26, 27],
            [28, 29, 30,  0,  0,  0,  0]]
        :returns: month grid
        """
        grid = np.arange(start=1, stop=self.nb_days+1)  # list of days
        grid = np.concatenate([np.zeros(self.d0), grid])  # add 0s before first days of month for empty cells
        if grid.shape[0]%7 != 0: # if the month does not finish on a Sunday (else, it is already ready to rescale)
            grid = np.concatenate([grid, np.zeros(7 - grid.shape[0] % 7)])  # add 0s to reach size k*7
        return grid.reshape((-1,7)).astype(np.int32)  # rescale 1 week per row


    def gen_html_title(self, grid):
        """Create month title/grid page.
        :param grid: month grid, see gen_grid
        :returns: html for title page
        """
        if not self.cfg.grid_month and not self.cfg.title_month:
            return ['']

        html = self.html_month

        if self.cfg.title_month:
            html = html.replace('MONTH', self.month_name)
            html = html.replace('YEAR', str(self.year))

        if self.cfg.grid_month:
            ## handle 4-week month
            html = html.replace('IGNORE_FIFTH_WEEK', '<!--' if self.nb_weeks < 5 else '', 1)
            html = html.replace('END_IGNORE_FIFTH_WEEK', '-->' if self.nb_weeks < 5 else '')
            ## handle 5-week month
            html = html.replace('IGNORE_SIXTH_WEEK', '<!--' if self.nb_weeks < 6 else '', 1)
            html = html.replace('END_IGNORE_SIXTH_WEEK', '-->' if self.nb_weeks < 6 else '')
            for i in range(self.nb_weeks):
                for j in range(7):
                    try:
                        date = grid[i,j]
                    except IndexError:
                        date = 0
                    html = html.replace(f'C{i+1}{j+1}_VIZ', 'visible' if date else 'hidden')
                    html = html.replace(f'C{i+1}{j+1}_DATE', str(date))

        return [html, '']


    def gen_html_week(self, week):
        """Create week pages.
        :param week: week as line of month grid, see gen_grid
        :returns: list of left and right pages
        """
        ## week dates
        non_zero_days_idx = np.nonzero(week)[0]
        date_start = week[non_zero_days_idx[0]]
        date_end = week[non_zero_days_idx[-1]]
        if date_start == date_end:
            week_title = f'{self.month_name} {date_start}'
        else:
            week_title = f'{self.month_name} {date_start} - {date_end}'

        ## left page
        html_l = self.html_week_left

        html_l = html_l.replace('WEEK_DATES', week_title)
        html_l = html_l.replace('MON_VIZ', 'display' if week[0] else 'display:none')
        html_l = html_l.replace('MON_DATE', f'{self.cfg.days.mon} {week[0]}')
        html_l = html_l.replace('MON_MOON', self.fullmoon_html if week[0] in self.moon_dates else '')
        html_l = html_l.replace('TUE_VIZ', 'display' if week[1] else 'display:none')
        html_l = html_l.replace('TUE_DATE', f'{self.cfg.days.tue} {week[1]}')
        html_l = html_l.replace('TUE_MOON', self.fullmoon_html if week[1] in self.moon_dates else '')
        html_l = html_l.replace('WED_VIZ', 'display' if week[2] else 'display:none')
        html_l = html_l.replace('WED_DATE', f'{self.cfg.days.wed} {week[2]}')
        html_l = html_l.replace('WED_MOON', self.fullmoon_html if week[2] in self.moon_dates else '')
        html_l = html_l.replace('BOX_TITLE', f'{self.cfg.headers.box_left_page}')
        html_l = html_l.replace('LEFT_COL_TITLE', f'{self.cfg.headers.left_col}')
        html_l = html_l.replace('RIGHT_COL_TITLE', f'{self.cfg.headers.right_col}')

        ## right page
        ## blank if empty
        if not week[3:].any() and self.cfg.last_page_empty:
            html_r = ''
        else:
            html_r = self.html_week_right

            html_r = html_r.replace('THU_VIZ', 'display' if week[3] else 'display:none')
            html_r = html_r.replace('THU_DATE', f'{self.cfg.days.thu} {week[3]}')
            html_r = html_r.replace('THU_MOON', self.fullmoon_html if week[3] in self.moon_dates else '')
            html_r = html_r.replace('FRI_VIZ', 'display' if week[4] else 'display:none')
            html_r = html_r.replace('FRI_DATE', f'{self.cfg.days.fri} {week[4]}')
            html_r = html_r.replace('FRI_MOON', self.fullmoon_html if week[4] in self.moon_dates else '')
            html_r = html_r.replace('SAT_VIZ', 'display' if week[5] else 'display:none')
            html_r = html_r.replace('SAT_DATE', f'{self.cfg.days.sat} {week[5]}')
            html_r = html_r.replace('SAT_MOON', self.fullmoon_html if week[5] in self.moon_dates else '')
            html_r = html_r.replace('SUN_VIZ', 'display' if week[6] else 'display:none')
            html_r = html_r.replace('SUN_DATE', f'{self.cfg.days.sun} {week[6]}')
            html_r = html_r.replace('SUN_MOON', self.fullmoon_html if week[6] in self.moon_dates else '')
            html_r = html_r.replace('BOX_TITLE', f'{self.cfg.headers.box_right_page}')
            html_r = html_r.replace('LEFT_COL_TITLE', f'{self.cfg.headers.left_col}')
            html_r = html_r.replace('RIGHT_COL_TITLE', f'{self.cfg.headers.right_col}')

        return [html_l, html_r]
