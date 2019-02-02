import multiprocessing
import time
from unittest import TestCase

import run


class TestRun(TestCase):
    def test_main(self):
        testTime = 20

        mainProcess = multiprocessing.Process(target=run.main(), name='main')
        mainProcess.start()

        for i in range(testTime):
            time.sleep(1)
            self.assertTrue(mainProcess.is_alive(), 'Main process is not alive after 3 seconds')

        mainProcess.terminate()
        mainProcess.join()
