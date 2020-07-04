'''1. Write a class Bakery, which:
• has a common variable called storage (int)
• has a function called baker() which (for 10 loops) notes down current state of the
storage, sleeps for 0.1s and adds 1 to the storage, then sleeps for 1s
• has a function called customer() which (for 10 loops) notes down current state of the
storage, sleeps for 0.2s and removes 2 from the storage if storage >= 2, then sleeps
for 1s
2. use threading.Lock to prevent race conditions
3. Run 2 customer threads and 1 baker thread
4. Use logging to ensure all functions are working'''


import logging
import time
import threading
import concurrent.futures

l = logging.getLogger()
l.setLevel(logging.DEBUG)

h = logging.StreamHandler()
h.setLevel(logging.INFO)
h.setFormatter(logging.Formatter('%(lineno)d - %(message)s'))
l.addHandler(h)

class Bakery:
    def __init__(self):
        self.storage = 0
        self.__lock = threading.Lock()

    def baker(self):
        for _ in range(10):
            with self.__lock:
                l.info(f'baker had-> {self.storage} cookies')
                time.sleep(0.1)
                self.storage += 1
                l.info(f'baker cooked-> {self.storage} cookies')
        time.sleep(1)

    def customer(self):
        for _ in range(10):
            with self.__lock:
                if self.storage > 0 and self.storage < 2:
                    self.storage -= 1
                    l.info(f'customer bought 1 and left -> {self.storage}')
                time.sleep(0.2)
                if self.storage >= 2:
                    self.storage -= 2
                    l.info(f'customer bought 2 and left -> {self.storage}')
        time.sleep(1)


if __name__ == '__main__':
    b = Bakery()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(b.customer)
        executor.submit(b.customer)
        executor.submit(b.baker)