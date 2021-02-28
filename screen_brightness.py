import datetime

import pysolar.radiation
import pysolar.solar

BRIGHTNESS_FILE = '/sys/class/backlight/rpi_backlight/brightness'
MINIMUM_BRIGHTNESS = 15  # After some manual testing, any lower than this and the display turns off.
MAXIMUM_BRIGHTNESS = 255


class ScreenBrightness:
    def __init__(self, lat, long):
        self.lat, self.long = lat, long

    def update_based_on_time_of_day(self):
        brightness_ratio = self.current_sunlight_as_ratio()
        self.set_display_brightness(brightness_ratio)

    def set_display_brightness(self, brightness_ratio):
        with open(BRIGHTNESS_FILE, 'w') as file:
            file.write(str(self.brightness_ratio_to_rpi_value(brightness_ratio)))

    @staticmethod
    def brightness_ratio_to_rpi_value(brightness_ratio):
        return round(brightness_ratio * (MAXIMUM_BRIGHTNESS - MINIMUM_BRIGHTNESS)) + MINIMUM_BRIGHTNESS

    def current_sunlight_as_ratio(self):
        date = datetime.datetime.utcnow().astimezone()
        altitude_deg = pysolar.solar.get_altitude(self.lat, self.long, date)
        radiation = pysolar.radiation.get_radiation_direct(date, altitude_deg)
        return min(radiation / 863, 1.0)
