from freezegun import freeze_time
from pyfakefs.fake_filesystem_unittest import TestCase
from unittest import main
import os

from screen_brightness import ScreenBrightness, BRIGHTNESS_FILE


class ScreenBrightnessTest(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        os.makedirs(os.path.dirname(BRIGHTNESS_FILE))
        self.screen_brightness = ScreenBrightness(51.4779423, -0.0036555)

    @freeze_time("2021-06-19 13:00:00")
    def test_midday_summer(self):
        self.screen_brightness.update_based_on_time_of_day()
        self.assert_brightness('254')

    @freeze_time("2021-02-12 12:14:00")
    def test_midday_winter(self):
        self.screen_brightness.update_based_on_time_of_day()
        self.assert_brightness('255')

    @freeze_time("2021-02-12 17:10:00")
    def test_sunset_winter(self):
        self.screen_brightness.update_based_on_time_of_day()
        self.assert_brightness('15')

    @freeze_time("2020-08-12 00:00:00")
    def test_midnight(self):
        self.screen_brightness.update_based_on_time_of_day()
        self.assert_brightness('15')

    def assert_brightness(self, expected):
        with open(BRIGHTNESS_FILE, 'r') as f:
            self.assertEqual(expected, f.read())


if __name__ == '__main__':
    main()
