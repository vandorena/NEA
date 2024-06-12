import Test_API_ECMWF
import unittest

def test_start_stop_dates_time():
    assert Test_API_ECMWF.start_stop_dates_time() == ("06", "12062024", "15062024")

if __name__ == "__main__":
    test_start_stop_dates_time()
    print("Everything Passed")