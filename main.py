from utils import parallelize_scraping, rename_and_save_excel_files, open_csv, modify_csv
import time
import pandas as pd

def initialize(start_batch, end_batch, input_list):
    print(f'Start: {start_batch}, End: {end_batch}')
    start_time_batch = time.time()

    try:
        list_comb = input_list[start_batch:end_batch]
        queue_errors = parallelize_scraping(list_comb)
    except Exception as e:
        print(f'Error: {e}')

    print(f'Batch elapsed time: {time.time() - start_time_batch}')
    return queue_errors


def start(start_number, total_number, batch_size, input_list):
    start_batch = start_number
    queue_errors = []
    end_batch = 0
    for i in range(batch_size+start_number, total_number+start_number+1, batch_size):
        end_batch = i
        queue_errors += initialize(start_batch, end_batch, input_list)
        start_batch = end_batch

    if end_batch < total_number+start_number:
        queue_errors += initialize(end_batch, total_number+start_number)

    return queue_errors

tot = 0
number = 1
tot_err = 0
comb_tot = 3500
start_time = time.time()
if __name__ == "__main__":
    while tot < comb_tot:
        start_number = 0
        total_number = 100 # batches of 20, 170 seconds, 5000 per night 10 hours
        batch_size = 20
        start_time_0 = time.time()
        print(f'-------------------------------------------- {number}/{int(comb_tot/(total_number-start_number))} --------------------------------------------')
        input_list = open_csv()
        queue_errors = start(start_number, total_number, batch_size, input_list)
        forgotten_elements = rename_and_save_excel_files()
        modify_csv(queue_errors, start_number, total_number, forgotten_elements)
        print(f'Total elapsed time for {total_number} combinations: {time.time() - start_time_0}')
        print(f'Combinations done from {start_number} to {start_number + total_number}')
        print(f'Errors: {queue_errors}')
        print(f'Missing elements: {forgotten_elements}')
        print(f'Total elements computed correctly: {total_number - len(forgotten_elements)}, errors:{len(forgotten_elements)}')
        tot += total_number-start_number
        tot_err += len(forgotten_elements)
        number += 1

print(f'--------------------------- End of the scraping session for {comb_tot} combinations! ---------------------------')
print(f'Total elements computed correctly: {comb_tot - tot_err}, errors:{tot_err}')
print(f'Total time elapsed: {time.time() - start_time}')



