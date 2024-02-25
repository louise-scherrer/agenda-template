import numpy as np
import numpy as np
import os.path
from agenda_template import AGENDA_TEMPLATE_DIR
import yaml


class ClassDict(dict):
    """Makes dict accessible by attribute.
    Taken from https://stackoverflow.com/a/1639632/6494418
    """
    def __getattr__(self, name):
        return self[name] if not isinstance(self[name], dict) \
            else ClassDict(self[name])



class Template:
    def __init__(self, param_file='params.yaml'):
        with open(os.path.join(AGENDA_TEMPLATE_DIR, param_file), 'r') as f_params:
            self.params = ClassDict(yaml.load(f_params, Loader=yaml.FullLoader))

        ## load templates
        with open(os.path.join(AGENDA_TEMPLATE_DIR,'mon-wed.html'), 'r') as f:
            self.left_page = f.read()

        with open(os.path.join(AGENDA_TEMPLATE_DIR,'thu-sun.html'), 'r') as f:
            self.right_page = f.read()

        with open(os.path.join(AGENDA_TEMPLATE_DIR,'agenda.css'), 'r') as f:
            self.css = f.read()

        ## edit css
        self.css = self.css.replace('TEXT_SIZE', f'{self.params.font_size.body}')
        self.css = self.css.replace('TITLE_SIZE', f'{self.params.font_size.title}')
        self.css = self.css.replace('MARGIN_TOP', f'{self.params.margins.top}')
        self.css = self.css.replace('MARGIN_BOT', f'{self.params.margins.bot}')
        self.css = self.css.replace('MARGIN_INNER', f'{self.params.margins.inner_side}')
        self.css = self.css.replace('MARGIN_OUTER', f'{self.params.margins.outer_side}')
        self.css = self.css.replace('LINE_SIZE', f'{self.params.line_size}')
        self.css = self.css.replace('SPACE_TITLE_TOP', f'{self.params.spacing.title.top}')
        self.css = self.css.replace('SPACE_TITLE_LEFT', f'{self.params.spacing.title.left}')
        self.css = self.css.replace('SPACE_BOX_TOP', f'{self.params.spacing.box.top}')
        self.css = self.css.replace('SPACE_BOX_RIGHT', f'{self.params.spacing.box.right}')
        self.css = self.css.replace('SPACE_BOX_BOT', f'{self.params.spacing.box.bot}')
        self.css = self.css.replace('SPACE_BOX_LEFT', f'{self.params.spacing.box.left}')


    def fill(self, month_name, week, index):
        ## week dates
        non_zero_days_idx = np.nonzero(week)[0]
        date_start = week[non_zero_days_idx[0]]
        date_end = week[non_zero_days_idx[-1]]
        week_title = f'{month_name} {date_start} - {date_end}'

        ## left page
        html_l = self.left_page

        html_l = html_l.replace('WEEK_DATES', week_title)
        html_l = html_l.replace('MON_VIZ', 'display' if week[0] else 'display:none')
        html_l = html_l.replace('MON_DATE', f'{self.params.days.mon} {week[0]}')
        html_l = html_l.replace('TUE_VIZ', 'display' if week[1] else 'display:none')
        html_l = html_l.replace('TUE_DATE', f'{self.params.days.tue} {week[1]}')
        html_l = html_l.replace('WED_VIZ', 'display' if week[2] else 'display:none')
        html_l = html_l.replace('WED_DATE', f'{self.params.days.wed} {week[2]}')
        html_l = html_l.replace('BOX_TITLE', f'{self.params.headers.box_left_page}')
        html_l = html_l.replace('LEFT_COL_TITLE', f'{self.params.headers.left_col}')
        html_l = html_l.replace('RIGHT_COL_TITLE', f'{self.params.headers.right_col}')
        html_l = html_l.replace('MY_CSS', self.css)

        ## right page
        ## blank if empty
        if not week[3:].any():
            html_r = ''
        else:
            html_r = self.right_page

            html_r = html_r.replace('THU_VIZ', 'display' if week[3] else 'display:none')
            html_r = html_r.replace('THU_DATE', f'{self.params.days.thu} {week[3]}')
            html_r = html_r.replace('FRI_VIZ', 'display' if week[4] else 'display:none')
            html_r = html_r.replace('FRI_DATE', f'{self.params.days.fri} {week[4]}')
            html_r = html_r.replace('SAT_VIZ', 'display' if week[5] else 'display:none')
            html_r = html_r.replace('SAT_DATE', f'{self.params.days.sat} {week[5]}')
            html_r = html_r.replace('SUN_VIZ', 'display' if week[6] else 'display:none')
            html_r = html_r.replace('SUN_DATE', f'{self.params.days.sun} {week[6]}')
            html_r = html_r.replace('BOX_TITLE', f'{self.params.headers.box_right_page}')
            html_r = html_r.replace('LEFT_COL_TITLE', f'{self.params.headers.left_col}')
            html_r = html_r.replace('RIGHT_COL_TITLE', f'{self.params.headers.right_col}')
            html_r = html_r.replace('MY_CSS', self.css)

        return [html_l, html_r]
