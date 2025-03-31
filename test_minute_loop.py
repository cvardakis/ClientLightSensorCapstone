import unittest
import datetime
from main import wait_until_5_minute


class MyTestCase(unittest.TestCase):

    def test_every_5_minutes_in_day(self):
        """
        For a representative hour (simulating any time in a day),
        verify that for every minute the computed next trigger is correct.
        """
        base_date = datetime.datetime(2021, 1, 1, 10, 0, 0)
        # Loop over every minute in the hour to test the function's logic.
        for minute in range(0, 60):
            test_time = base_date.replace(minute=minute, second=10, microsecond=0)
            next_minute = (test_time.minute // 5 + 1) * 5
            if next_minute >= 60:
                expected_trigger = (test_time + datetime.timedelta(hours=1)).replace(minute=0, second=30, microsecond=0)
            else:
                expected_trigger = test_time.replace(minute=next_minute, second=30, microsecond=0)
            result = wait_until_5_minute(test_time)
            self.assertEqual(result, expected_trigger, f"Failed for time {test_time}")

    def test_turn_of_month(self):
        """
        Test that a time near the end of the month (where adding an hour causes a month rollover)
        computes the correct next trigger datetime.
        """
        # January 31, 23:57:10 rolls over to February 1
        test_time = datetime.datetime(2021, 1, 31, 23, 57, 10)
        # Since minute 57 will roll to next 5-minute mark (60), add one hour and set minute to 0.
        expected_trigger = (test_time + datetime.timedelta(hours=1)).replace(minute=0, second=30, microsecond=0)
        result = wait_until_5_minute(test_time)
        self.assertEqual(result, expected_trigger, f"Failed for turn of month at {test_time}")

    def test_turn_of_year(self):
        """
        Test that a time near the end of the year (where adding an hour causes a year rollover)
        computes the correct next trigger datetime.
        """
        # December 31, 23:57:10 should roll over to January 1 of the next year.
        test_time = datetime.datetime(2021, 12, 31, 23, 57, 10)
        expected_trigger = (test_time + datetime.timedelta(hours=1)).replace(minute=0, second=30, microsecond=0)
        result = wait_until_5_minute(test_time)
        self.assertEqual(result, expected_trigger, f"Failed for turn of year at {test_time}")


if __name__ == '__main__':
    unittest.main()
