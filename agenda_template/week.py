import numpy as np
import os.path
from agenda_template import AGENDA_TEMPLATE_DIR
from agenda_template.utils import ClassDict


class Week:
    def __init__(self, config):
        self.cfg = config

        ## load templates
        with open(os.path.join(AGENDA_TEMPLATE_DIR,'week_left.html'), 'r') as f:
            self.left_page = f.read()

        with open(os.path.join(AGENDA_TEMPLATE_DIR,'week_right.html'), 'r') as f:
            self.right_page = f.read()

        with open(os.path.join(AGENDA_TEMPLATE_DIR,'week.css'), 'r') as f:
            self.css = f.read()

        ## edit css
        self.css = self.css.replace('TEXT_SIZE', f'{self.cfg.font_size.body}')
        self.css = self.css.replace('TITLE_SIZE', f'{self.cfg.font_size.title}')
        self.css = self.css.replace('MARGIN_TOP', f'{self.cfg.margins.top}')
        self.css = self.css.replace('MARGIN_BOT', f'{self.cfg.margins.bot}')
        self.css = self.css.replace('MARGIN_INNER', f'{self.cfg.margins.inner_side}')
        self.css = self.css.replace('MARGIN_OUTER', f'{self.cfg.margins.outer_side}')
        self.css = self.css.replace('LINE_SIZE', f'{self.cfg.line_size}')
        self.css = self.css.replace('SPACE_TITLE_TOP', f'{self.cfg.spacing.title.top}')
        self.css = self.css.replace('SPACE_TITLE_LEFT', f'{self.cfg.spacing.title.left}')
        self.css = self.css.replace('SPACE_BOX_TOP', f'{self.cfg.spacing.box.top}')
        self.css = self.css.replace('SPACE_BOX_RIGHT', f'{self.cfg.spacing.box.right}')
        self.css = self.css.replace('SPACE_BOX_BOT', f'{self.cfg.spacing.box.bot}')
        self.css = self.css.replace('SPACE_BOX_LEFT', f'{self.cfg.spacing.box.left}')

        self.left_page = self.left_page.replace('MY_CSS', self.css)
        self.right_page = self.right_page.replace('MY_CSS', self.css)


    def gen_html(self, month_name, week, index):
        ## week dates
        non_zero_days_idx = np.nonzero(week)[0]
        date_start = week[non_zero_days_idx[0]]
        date_end = week[non_zero_days_idx[-1]]
        if date_start == date_end:
            week_title = f'{month_name}<br>{date_start}'
        else:
            week_title = f'{month_name}<br>{date_start} - {date_end}'

        ## left page
        html_l = self.left_page

        html_l = html_l.replace('WEEK_DATES', week_title)
        html_l = html_l.replace('MON_VIZ', 'display' if week[0] else 'display:none')
        html_l = html_l.replace('MON_DATE', f'{self.cfg.days.mon} {week[0]}')
        html_l = html_l.replace('TUE_VIZ', 'display' if week[1] else 'display:none')
        html_l = html_l.replace('TUE_DATE', f'{self.cfg.days.tue} {week[1]}')
        html_l = html_l.replace('WED_VIZ', 'display' if week[2] else 'display:none')
        html_l = html_l.replace('WED_DATE', f'{self.cfg.days.wed} {week[2]}')
        html_l = html_l.replace('BOX_TITLE', f'{self.cfg.headers.box_left_page}')
        html_l = html_l.replace('LEFT_COL_TITLE', f'{self.cfg.headers.left_col}')
        html_l = html_l.replace('RIGHT_COL_TITLE', f'{self.cfg.headers.right_col}')

        ## right page
        ## blank if empty
        if not week[3:].any() and self.cfg.last_page_empty:
            html_r = ''
        else:
            html_r = self.right_page

            html_r = html_r.replace('THU_VIZ', 'display' if week[3] else 'display:none')
            html_r = html_r.replace('THU_DATE', f'{self.cfg.days.thu} {week[3]}')
            html_r = html_r.replace('FRI_VIZ', 'display' if week[4] else 'display:none')
            html_r = html_r.replace('FRI_DATE', f'{self.cfg.days.fri} {week[4]}')
            html_r = html_r.replace('SAT_VIZ', 'display' if week[5] else 'display:none')
            html_r = html_r.replace('SAT_DATE', f'{self.cfg.days.sat} {week[5]}')
            html_r = html_r.replace('SUN_VIZ', 'display' if week[6] else 'display:none')
            html_r = html_r.replace('SUN_DATE', f'{self.cfg.days.sun} {week[6]}')
            html_r = html_r.replace('BOX_TITLE', f'{self.cfg.headers.box_right_page}')
            html_r = html_r.replace('LEFT_COL_TITLE', f'{self.cfg.headers.left_col}')
            html_r = html_r.replace('RIGHT_COL_TITLE', f'{self.cfg.headers.right_col}')

        return [html_l, html_r]
