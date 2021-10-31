from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())


def get_massage_timestamp(receive_time_stamp, counter):
    return max(receive_time_stamp, counter) + 1


def event(pid, counter):
    counter += 1
    print('Some event in {} !'. format(pid) + local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    counter += 1
    pipe.send(('Empty shell', counter))
    print('This message sent from ' + str(pid) + local_time(counter))
    return counter


def get_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = get_massage_timestamp(timestamp, counter)
    print('This message received at ' + str(pid) + local_time(counter))
    return counter


def process_one(pipe12):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = get_message(pipe12, pid, counter)
    event(pid, counter)


def process_two(pipe21, pipe23):
    pid = getpid()
    counter = 0
    counter = get_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    get_message(pipe23, pid, counter)


def process_three(pipe32):
    pid = getpid()
    counter = 0
    counter = get_message(pipe32, pid, counter)
    send_message(pipe32, pid, counter)


if __name__ == '__main__':
    first_second, second_done = Pipe()
    second_third, third_second = Pipe()

    first_process = Process(target=process_one, args=(first_second,))
    second_process = Process(target=process_two, args=(second_done, second_third))
    third_process = Process(target=process_three, args=(third_second,))

    first_process.start()
    second_process.start()
    third_process.start()

    first_process.join()
    second_process.join()
    third_process.join()
