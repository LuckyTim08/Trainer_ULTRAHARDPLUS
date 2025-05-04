from commands import *
import time


file_name_task, name = openfile_window()
file_name = f'answers-{name}.txt'
inf = parse_in(file_name_task)
n = inf['n']
all_tasks_time = inf['t']
timelist = time_list(all_tasks_time, n)

time_start = time.ctime(time.time())
writings = []
writings.append(f'{time_start}')
writings.append('--------')

curt = 0
i = 1
sum_time = 0
while curt < all_tasks_time:
    if curt in timelist:
        task_start_time = time.time()
        writings.append(f'{task_window(inf, i, time.time())}')
        task_end_time = time.time()
        task_comp_duration = int(task_end_time - task_start_time)
        sum_time += task_comp_duration
        writings.append(f'Время выполнения задания: {round(task_comp_duration / 60 * 100) / 100} min')
        if i != n:
            writings.append('|')
        i += 1

        if task_comp_duration > 300:
            curt += 299
        else:
            curt += task_comp_duration

    time.sleep(1)
    curt += 1

end_window()
writings.append('--------')
time_end = time.ctime(time.time())
writings.append(f'{time_end}')
writings.append(f'Время выполнения всех заданий: {round(sum_time / 60 * 100) / 100} min')

upload_file(writings, file_name)

clean(file_name)
