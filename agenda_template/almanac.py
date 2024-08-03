import calendar
import skyfield.api
from skyfield.framelib import ecliptic_frame
from time import localtime
import shutil
import os.path
from agenda_template import AGENDA_RESSOURCES_DIR


class MoonAlmanac:
    def __init__(self):
        self.ts = skyfield.api.load.timescale()
        ephemeris_file_path = os.path.join(AGENDA_RESSOURCES_DIR, 'de421.bsp')
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


    def get_phase_at_date(self, year, month, day):
        t = self.ts.utc(year, month, day, -localtime().tm_gmtoff/3600, 0)
        earth = self.eph['earth'].at(t)
        sun = earth.observe(self.eph['sun']).apparent()
        moon = earth.observe(self.eph['moon']).apparent()

        _, slon, _ = sun.frame_latlon(ecliptic_frame)
        _, mlon, _ = moon.frame_latlon(ecliptic_frame)
        return (mlon.degrees - slon.degrees) % 360.


    def get_full_moon_month(self, year, month):
        _, nb_days = calendar.monthrange(year, month)
        phase_at_date = [self.get_phase_at_date(year, month, d) for d in range(nb_days+1)]
        # new_moons = [d for d in range(nb_days) if phase_at_date[d+1]) < phase_at_date[d]]
        full_moons = [d for d in range(nb_days) if phase_at_date[d] < 180. < phase_at_date[d+1]]
        return full_moons
