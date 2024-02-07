import numpy as np
import os.path
from agenda_template import AGENDA_TEMPLATE_DIR
import yaml
from collections import namedtuple


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

        Page = namedtuple('Page', ['html', 'css'])
        with open(os.path.join(AGENDA_TEMPLATE_DIR,'lun-mer.html'), 'r') as f_html, open(os.path.join(AGENDA_TEMPLATE_DIR,'style-lun-mer.css'), 'r') as f_css:
            self.left_page = Page(f_html.read(), f_css.read())

        with open(os.path.join(AGENDA_TEMPLATE_DIR,'jeu-dim.html'), 'r') as f_html, open(os.path.join(AGENDA_TEMPLATE_DIR,'style-jeu-dim.css'), 'r') as f_css:
            self.right_page = Page(f_html.read(), f_css.read())


    def fill(self, month_name, week, index):
        ## week dates
        non_zero_days_idx = np.nonzero(week)[0]
        date_start = week[non_zero_days_idx[0]]
        date_end = week[non_zero_days_idx[-1]]
        week_title = f'{month_name} {date_start} - {date_end}'

        ## left page
        html_l = self.left_page.html
        css_l = self.left_page.css

        html_l = html_l.replace('WEEK_DATES', week_title)
        if index == 0 and non_zero_days_idx[0] != 0:  # remove col headers if the month is not starting on a Monday
            html_l = html_l.replace('perso', '')
            html_l = html_l.replace('boulot', '')
        html_l = html_l.replace('MON_DATE', f'{self.params.days.mon} {week[0]}' if week[0] else '')
        html_l = html_l.replace('TUE_DATE', f'{self.params.days.tue} {week[1]}' if week[1] else '')
        html_l = html_l.replace('WED_DATE', f'{self.params.days.wed} {week[2]}' if week[2] else '')

        css_l = css_l.replace('MON_ROW', 'lundi boulot' if week[0] else '. .')
        css_l = css_l.replace('TUE_ROW', 'mardi mar_droite' if week[1] else '. .')
        css_l = css_l.replace('WED_ROW', 'mercredi mer_droite' if week[2] else '. .')


        ## right page
        html_r = self.right_page.html
        css_r = self.right_page.css

        if index == 0 and non_zero_days_idx[0] > 3:  # remove col headers if the month is starting starting after Thursday
            html_r = html_r.replace('perso', '')
            html_r = html_r.replace('boulot', '')

        html_r = html_r.replace('THU_DATE', f'{self.params.days.thu} {week[3]}' if week[3] else '')
        html_r = html_r.replace('FRI_DATE', f'{self.params.days.fri} {week[4]}' if week[4] else '')
        html_r = html_r.replace('SAT_DATE', f'{self.params.days.sat} {week[5]}' if week[5] else '')
        html_r = html_r.replace('SUN_DATE', f'{self.params.days.sun} {week[6]}' if week[6] else '')

        css_r = css_r.replace('THU_ROW', 'jeudi boulot' if week[3] else '. .')
        css_r = css_r.replace('FRI_ROW', 'vendredi ven_droite' if week[4] else '. .')
        css_r = css_r.replace('SAT_CELL', 'samedi' if week[5] else '.')
        css_r = css_r.replace('SUN_CELL', 'dimanche' if week[6] else '.')

        return [(html_l, css_l), (html_r, css_r)]
