import calendar
import skyfield.api
from skyfield.framelib import ecliptic_frame
from time import localtime
import holidays
import shutil
import os.path
from agenda_template import AGENDA_RESOURCES_DIR, AGENDA_TEMPLATE_DIR
from agenda_template import utils
import yaml


class MoonAlmanac:
    def __init__(self, cfg):
        self.enable = cfg.moon.enable and (cfg.moon.new.enable or cfg.moon.full.enable)
        if self.enable:
            self.ts = skyfield.api.load.timescale()
            ephemeris_file_path = os.path.join(AGENDA_RESOURCES_DIR, 'de421.bsp')
            try:
                self.eph = skyfield.api.load_file(ephemeris_file_path)  # JPL ephemeris DE421 (covers 1900-2050)
            except FileNotFoundError:
                ans = input('JPL ephemeris file not found, would you like to download it? [y/n] ').lower()
                if ans == 'y':
                    print('ok! downloading NASA\'s JPL ephemeris DE421')
                    self.eph = skyfield.api.load('de421.bsp')
                    shutil.move('./de421.bsp', ephemeris_file_path)
                else:
                    print('umpf. then set disable add_moons in your config file')
                    exit()

        self.img_new = utils.image_html_code(cfg.moon.new.image, cfg.moon.color) if cfg.moon.new.enable else ''
        self.img_full = utils.image_html_code(cfg.moon.full.image, cfg.moon.color) if cfg.moon.full.enable else ''


    def get_phase_at_date(self, year, month, day):
        t = self.ts.utc(year, month, day, -localtime().tm_gmtoff/3600, 0)
        earth = self.eph['earth'].at(t)
        sun = earth.observe(self.eph['sun']).apparent()
        moon = earth.observe(self.eph['moon']).apparent()

        _, slon, _ = sun.frame_latlon(ecliptic_frame)
        _, mlon, _ = moon.frame_latlon(ecliptic_frame)
        return (mlon.degrees - slon.degrees) % 360.


    def get_moons_for_month(self, year, month):
        if self.enable:
            _, nb_days = calendar.monthrange(year, month)
            phase_at_date = [self.get_phase_at_date(year, month, d) for d in range(nb_days+1)]
            new_moons = [d for d in range(nb_days) if phase_at_date[d+1] < phase_at_date[d]]
            full_moons = [d for d in range(nb_days) if phase_at_date[d] < 180. < phase_at_date[d+1]]
            return new_moons, full_moons
        else:
            return [], []



class EventAlmanac:
    def __init__(self, year, cfg):
        self.year = year
        self.calendar = {}

        ## load custom events calendar
        if cfg.events.custom.enable:
            with open(os.path.join(AGENDA_TEMPLATE_DIR, cfg.events.custom.yaml), 'r') as f:
                self.calendar = yaml.load(f, Loader=yaml.FullLoader)

        ## load holidays for target year
        if cfg.events.holidays.enable:
            holiday_calendar = holidays.country_holidays(cfg.events.holidays.country.upper(), years=year, language=cfg.events.holidays.lang)

            ## merge calendars
            for k in holiday_calendar.keys():
                holiday_text = holiday_calendar[k] if cfg.events.holidays.use_names else cfg.events.holidays.custom_text
                if k.month not in self.calendar.keys():
                    self.calendar[k.month] = {k.day: holiday_text}
                elif k.day not in self.calendar[k.month].keys():
                    self.calendar[k.month][k.day] = holiday_text
                else:
                    self.calendar[k.month][k.day] = holiday_text + '<br>' + self.calendar[k.month][k.day]

            if cfg.events.holidays.use_names and cfg.events.holidays.lang == 'fr':
                ## hard coded substitutions cause I don't like the names
                self.calendar[5][8] = self.calendar[5][8].replace('Fête de la Victoire', 'Armistice 1945')
                self.calendar[11][11] = self.calendar[11][11].replace('Armistice', 'Armistice 1918')


    def get_events_for_month(self, month):
        try:
            return self.calendar[month]
        except KeyError:
            return {}
