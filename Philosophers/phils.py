import threading
from time import sleep
import random
forks = 5
philosophers = 5

forks_lock = [threading.Lock() for n in range(forks)]


def dining_philosopher(fork_first, fork_second, phil):
    while True:
        first_fork = min(fork_first, fork_second)
        second_fork = max(fork_first, fork_second)
        forks_lock[first_fork].acquire()
        forks_lock[second_fork].acquire()
        print(f'Философ {phil} ест')
        sleep(random.randint(1, 5))
        forks_lock[first_fork].release()
        forks_lock[second_fork].release()


for philosopher in range(philosophers):
    fork_right = philosopher
    fork_left = (philosopher+1) % philosophers
    threading.Thread(target=dining_philosopher, args=(fork_left, fork_right, philosopher)).start()
