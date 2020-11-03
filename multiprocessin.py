'''2 threads would read from 2 different json files, write to a queue.
Main reads from that queue and sends to a child process through a pipe
Child process receives from the pipe and writes to a csv file'''

import multiprocessing as mp
import csv
import json
import concurrent.futures
import queue
import time

def file_reader(files):
    with open(files) as fr:
        data = json.load(fr)
        for i in data:
            q.put(i)
        q.put('end', timeout=2)

def write_to_csv(child_conn):
    with open('result.csv', 'w+') as fw:
        fieldnames = ['id', 'first_name', 'middle_name', 'last_name', 'gender', 'email', 'job_title']
        write_to_file = csv.DictWriter(fw, fieldnames=fieldnames)
        write_to_file.writeheader()
        data = child_conn.recv()
        while data != 'end':
            write_to_file.writerow(data)
            data = child_conn.recv()
            print(data)

if __name__=='__main__':
    parent_conn, child_conn = mp.Pipe()
    q = queue.Queue()
    file_first = 'people1.json'
    file_second = 'people2.json'
    starttime = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(file_reader, file_first)
        executor.submit(file_reader, file_second)

    p = mp.Process(target=write_to_csv, args=(child_conn,))
    p.start()
    count = 0
    while count <= 2:
        info = q.get()
        if info == 'end':
            count += 1
            if count == 2:
                # print(info)
                parent_conn.send(info)
        else:
            # print(info)
            parent_conn.send(info)


    print(f'It took {time.time()-starttime}sec')
    print('Finished')