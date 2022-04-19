#!/usr/bin/env python
'''
HW7 - Parallel Programming

I've choosed option #2 - parallel processing of big FASTA file. On my computer
this looks like CPU bound task - reading of file (IO task) faster than
count of nucleotides (CPU task). Therefore I decided to use multiprocessing.
This allows to use several CPU cores to count nucleotides and makes
file processing faster.

I split all works on jobs (processes):
 * one main job - reads file, makes tasks for other job, combines results
 * working job  - wait task and process it.

I do interprocess communication by multiprocessing.Queue(). It allows safely
exchange data between jobs (processes).
I use 2 queues:
 - TASK_QUEUE   - to send tasks from main job to working jobs,
 - TASK_RESULTS - to send task results from working jobs to main job.

To store task data I use special data class (decorator dataclass)
with requested fields (task_id, read_id, seq_id) and result field (task_res).

There are 3 parameters:

  -f, --fasta    - path to FASTA file for analysis, mandatory,
  -t, --threads  - process numbers (>=1), optional, default=1,
  -n, --nseq     - number of sequences to process, optional, default=all,

Example of script usage:

  # process all file by 4 threads
  ./nucl_content.py --fasta GRCh38_latest_genomic.fna --threads 4

  # process first 20 sequences by 1 thread
  ./nucl_content.py --fasta GRCh38_latest_genomic.fna --threads 4 --nseq 20
'''

from Bio import SeqIO
import argparse
import sys
import queue
import multiprocessing
import time
import numpy as np
import signal
from dataclasses import dataclass


# Multiprocess queue with task to count nucleotides. MainJob puts tasks to
# this queue and WorkingJobs read task and count nucleotides.
TASK_QUEUE = multiprocessing.Queue()

# Multiprocess queue for task results. WorkingJobs put tasks with counted
# nucleotides and MainJob reads them and output to console.
TASK_RESULTS = multiprocessing.Queue()


@dataclass
class Task:
    '''
    Data class to store data for:
      - task request,
      - result string with amount of nucleotides.
    '''
    task_id: int    # id of task
    read_id: str    # read id
    read_seq: str   # read sequences
    task_res: str   # task result with amount of nucleotides


# signal handler to avoid printing python exception after pressing Ctrl+C
def signal_handler(sig, frame):
    sys.exit(0)


def count_nucleotides(task: Task) -> str:
    '''
    Process task and count nucleotides. Result string is placed
    in TASK_RESULTS.
    This function calls in MainJob and in WorkingJobs.
    '''
    # I tried to use numpy array to count amount of nucleotides. But
    # performance was not great. Therefore I used python list.
    use_numpyarray = False
    if use_numpyarray:
        # count nucleotides by numpy array
        x = np.array(list(task.read_seq))
        nucs, counts = np.unique(x, return_counts=True)
        res_str = ', '.join(['{}={!r}'.format(k, v)
                             for k, v in zip(nucs, counts)])
    else:
        # count nucleotides by python list
        nucs = {}
        for n in task.read_seq:
            if n not in nucs:
                nucs[n] = 1
            else:
                nucs[n] += 1
        res_str = ', '.join(['{}={!r}'.format(k, v) for k, v in nucs.items()])

    # put task with result string to TASK_RESULTS
    task.task_res = res_str
    TASK_RESULTS.put(task)


def working_job():
    '''
    This function is called as a separate process. It reads tasks from
    TASK_QUEUE, count nucleotides and put result string to TASK_RESULTS.
    '''
    while True:
        try:
            task = TASK_QUEUE.get(block=True)
        except queue.Empty:
            continue  # read no data
        if isinstance(task, Task):
            # process the task
            count_nucleotides(task)
        else:
            # any other data from queue means termination of the job
            sys.exit()


def check_and_print_next_res(cnt_out: int) -> int:
    '''
    This function calls in MainJob. It get results from TASK_RESULTS queue
    and prints result string for 'cnt_out' task.
    This function uses an own data - dictionary
    (key = task_id, value = task_result),
      - check_and_print_next_res.out_results,
    this data is stored between function calls.
    '''

    # read data from TASK_RESULTS to OUT_RESULTS
    while True:
        try:
            task = TASK_RESULTS.get(block=False)
        except queue.Empty:
            break  # no data
        else:
            # read new task result
            check_and_print_next_res.out_results[task.task_id] = task

    # try to print result string for 'cnt_out' task
    if cnt_out in check_and_print_next_res.out_results:
        # print result string, use alignment with spaces for pretty view
        res = check_and_print_next_res.out_results[cnt_out]
        max_id_len = 16
        nspaces = max_id_len - len(res.read_id)
        spaces = ' ' if nspaces <= 0 else ' ' * nspaces
        print(f'{cnt_out}: {res.read_id}:{spaces}{res.task_res}')
        cnt_out += 1

    # return number of current awaiting task
    return cnt_out


def main_job(input_fasta: str, njobs: int, nseq: int):
    '''
    This func contains main app activities:
      - read fasta file seq by seq,
      - check availability of working jobs and try to delegate them the 
        count of nucleotides,
      - check results of culculation and print them
    '''
    # register handler to avoid printing python exception after pressing Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # initialize function internal data
    check_and_print_next_res.out_results = {}

    # start working jobs as processes
    num_work_jobs = njobs - 1  # one job is main job
    jobs = []                  # processes
    for i in range(num_work_jobs):
        job = multiprocessing.Process(target=working_job)
        job.start()
        jobs.append(job)

    # read data from file seq by seq
    cnt_read = 0  # number of current reading from file sequence
    cnt_out = 0   # number of current output to console sequence
    fasta_sequences = SeqIO.parse(open(input_fasta), 'fasta')
    for read in fasta_sequences:
        # Check amount of tasks in TASK_QUEUE and put task in queue or
        # count by self. In any case result will be placed in OUT_RESULTS.
        task = Task(cnt_read, read.id, read.seq, '')
        if TASK_QUEUE.qsize() < (num_work_jobs * 2):
            # put task to queue, allow other processes to do it
            TASK_QUEUE.put(task)
        else:
            # too much tasks in queue, count nucleotides by self
            count_nucleotides(task)
        cnt_read += 1

        # check result for cnt_out sequence and print it if ready
        cnt_out = check_and_print_next_res(cnt_out)

        # stop reading if user asks to process only 'nseq' sequences
        if cnt_read == nseq:
            break

    # help other jobs to do tasks from queue
    while True:
        # check result for cnt_out sequence and print it if ready
        cnt_out = check_and_print_next_res(cnt_out)
        # try to read task from queue
        try:
            task = TASK_QUEUE.get(block=True, timeout=0.2)
        except queue.Empty:
            # queue is empty, all is done
            break
        # do task
        count_nucleotides(task)

    # wait for all results
    while cnt_out != cnt_read:
        # check result for cnt_out sequence and print it if ready
        new_cnt_out = check_and_print_next_res(cnt_out)
        if new_cnt_out == cnt_out:
            time.sleep(0.2)
        else:
            cnt_out = new_cnt_out

    # terminate release working jobs
    for job in jobs:
        TASK_QUEUE.put('exit')  # put any data but Task to queue
    # wait termination
    for job in jobs:
        job.join()


def main():
    '''
    Main function - entry point to application.
    It processes and checks incomming arguments and starts main job.
    '''
    # process args
    parser = argparse.ArgumentParser(description='Calculate nucleotides.')
    parser.add_argument('-f', '--fasta',
                        help='Path to FASTA file for analysis.',
                        required=True, type=str)
    parser.add_argument('-t', '--threads', help='Thread numbers (>=1).',
                        required=False, type=int, default=1)
    parser.add_argument('-n', '--nseq', help='Number of sequences to process.',
                        required=False, type=int, default=-1)
    args = parser.parse_args()

    if args.threads < 1:
        print(f'ERR:  wrong thread number {args.threads}, should be >=1.')
        return -1

    # start main job
    main_job(args.fasta, args.threads, args.nseq)
    return 0


# single script application
if __name__ == "__main__":

    res = main()
    sys.exit(res)
