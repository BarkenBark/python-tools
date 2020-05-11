from os.path import join
import time
from time import sleep
import tempfile

from barktools.base_utils import RingBuffer
from barktools.base_utils import Clocker

from tests.test_helper import TMP_DIR

class TestRingBuffer:
    
    def test_1(self):
        buffer_size = 3
        ring_buffer = RingBuffer(buffer_size=buffer_size)
        items_to_put = [0,1,2,3,4,5,6,7,8,9]
        for item in items_to_put:
            ring_buffer.put(item)
        assert ring_buffer.items() == [9,7,8]
        assert ring_buffer.n_last(2) == [8,9]

    def test_2(self):
        buffer_size = 1
        ring_buffer = RingBuffer(buffer_size=buffer_size)
        for item in [1,2,3,4]:
            ring_buffer.put(item)
        assert ring_buffer.last() == 4  

class TestClocker:

    def test_1(self):
        with tempfile.TemporaryDirectory() as tmp_dir:

            # Simulate process and make measurements
            clocker = Clocker(tmp_dir)

            for _ in range(100):
                clocker.clock('sleep_centi')
                sleep(0.01)
                clocker.clock('sleep_milli')
                sleep(0.001)
            centi_path = join(tmp_dir, "sleep_centi.txt")
            milli_path = join(tmp_dir, "sleep_milli.txt")
            del(clocker) # NOTE: Necessary for tempfile to clean tmp_dir
            
            # Assert that measurements are acceptable
            individual_centi_tol = 5e-2
            mean_centi_tol = 2e-3
            centi_times = []
            with open(centi_path, 'r') as file:
                for line in file:
                    centi_times.append(float(line))
            assert all([abs(centi_time-0.01) < individual_centi_tol for centi_time in centi_times])
            centi_times_mean = sum(centi_times)/len(centi_times)
            assert abs(centi_times_mean-0.01) <  mean_centi_tol

            individual_milli_tol = 5e-2
            mean_milli_tol = 2e-3
            milli_times = []
            with open(milli_path, 'r') as file:
                for line in file:
                    milli_times.append(float(line))
            assert all([abs(milli_time-0.001) < individual_milli_tol for milli_time in milli_times])
            milli_times_mean = sum(milli_times)/len(milli_times)
            assert abs(milli_times_mean-0.001) <  mean_milli_tol