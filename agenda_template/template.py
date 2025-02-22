import numpy as np
import calendar
import os.path
from agenda_template import AGENDA_TEMPLATE_DIR, AGENDA_RESOURCES_DIR
from agenda_template import utils


MONTHS_DICT = {
    1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun',
    7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'
}


class Template():
    def __init__(self, cfg, year, month, moon_almanac, event_almanac):
        self.cfg = cfg
        self.d0, self.nb_days = calendar.monthrange(year, month)
        self.nb_weeks = (self.d0 + self.nb_days - 1) // 7 + 1  # number of weeks in month (4, 5, or 6)
        self.month_name = cfg.months[MONTHS_DICT[month]]
        self.year = year

        ## load css
        with open(os.path.join(AGENDA_TEMPLATE_DIR, 'style.css'), 'r') as f:
            self.css = f.read()

        ## general params
        self.css = self.css.replace('FONT_NAME', f'{self.cfg.font.name}')
        self.css = self.css.replace('FONT_URL', f'{os.path.join(AGENDA_RESOURCES_DIR, self.cfg.font.file)}')
        self.css = self.css.replace('TEXT_SIZE', f'{self.cfg.font_size.dates}')
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

        ## moon params
        self.css = self.css.replace('MOON_IMG_OPACITY', f'{self.cfg.moon.opacity}')
        self.css = self.css.replace('MOON_IMG_PADDING', f'{self.cfg.moon.padding}')
        self.css = self.css.replace('MOON_IMG_SIZE', f'{self.cfg.moon.size}')
        self.css = self.css.replace('MOON_IMG_ALIGN', '0 0 auto' if self.cfg.moon.align == 'top' \
                                                    else '0 0 auto' if self.cfg.moon.align == 'bottom' \
                                                    else '0 0 0')

        ## event params
        self.css = self.css.replace('EVENT_TEXT_ALIGN', f'{self.cfg.events.align}')
        self.css = self.css.replace('EVENT_TEXT_OPACITY', f'{self.cfg.events.opacity}')
        self.css = self.css.replace('EVENT_TEXT_COLOR', f'{self.cfg.events.color}')
        self.css = self.css.replace('EVENT_TEXT_SIZE', f'{self.cfg.font_size.events}')
        self.css = self.css.replace('EVENT_PADDING_TOP', f'{self.cfg.events.padding.top}')
        self.css = self.css.replace('EVENT_PADDING_SIDE', f'{self.cfg.events.padding.sides}')

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

        ## new and full moons
        self.new_moon_dates, self.full_moon_dates = moon_almanac.get_moons_for_month(year, month)
        self.new_moon_html = moon_almanac.img_new
        self.full_moon_html = moon_almanac.img_full

        ## events
        self.event_dict = event_almanac.get_events_for_month(month)


    def gen_html(self):
        """Returns a list of html pages for the month.
        :returns: list of html pages
        """
        grid = self.gen_grid()
        a = self.gen_html_month(grid) + [p for week in grid for p in self.gen_html_week(week)]


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


    def gen_html_month(self, grid):
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
        html_l = html_l.replace('BOX_TITLE', f'{self.cfg.headers.box_left_page}')
        html_l = html_l.replace('LEFT_COL_TITLE', f'{self.cfg.headers.left_col}')
        html_l = html_l.replace('RIGHT_COL_TITLE', f'{self.cfg.headers.right_col}')

        for i, name in zip([0,1,2], ['MON', 'TUE', 'WED']):
            html_l = html_l.replace(name + '_VIZ', 'display' if week[i] else 'display:none')
            html_l = html_l.replace(name + '_DATE', f'{self.cfg.days[name.lower()]} {week[i]}')
            html_l = html_l.replace(name + '_EVENT', self.event_dict[week[i]] if week[i] in self.event_dict.keys() else '')
            html_l = html_l.replace(name + '_MOON', self.new_moon_html if week[i] in self.new_moon_dates \
                                                else self.full_moon_html if week[i] in self.full_moon_dates \
                                                else '')

        ## right page
        ## blank if empty
        if not week[3:].any() and self.cfg.last_page_empty:
            html_r = ''
        else:
            html_r = self.html_week_right

            html_r = html_r.replace('BOX_TITLE', f'{self.cfg.headers.box_right_page}')
            html_r = html_r.replace('LEFT_COL_TITLE', f'{self.cfg.headers.left_col}')
            html_r = html_r.replace('RIGHT_COL_TITLE', f'{self.cfg.headers.right_col}')

            for i, name in zip([3,4,5,6], ['THU', 'FRI', 'SAT', 'SUN']):
                html_r = html_r.replace(name + '_VIZ', 'display' if week[i] else 'display:none')
                html_r = html_r.replace(name + '_DATE', f'{self.cfg.days[name.lower()]} {week[i]}')
                html_r = html_r.replace(name + '_EVENT', self.event_dict[week[i]] if week[i] in self.event_dict.keys() else '')
                html_r = html_r.replace(name + '_MOON', self.new_moon_html if week[i] in self.new_moon_dates \
                                                    else self.full_moon_html if week[i] in self.full_moon_dates \
                                                    else '')

        return [html_l, html_r]
