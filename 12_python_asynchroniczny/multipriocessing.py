import multiprocessing as mp
import time

def deamon_task():
    name = mp.current_process().name
    print(f'Process{name} rozpoczęty')
    for i in range (1, 100):
        print(i)
        time.sleep(1)
    time.sleep(10)
    print(f'proces {name} zakończony')

def nondeamon_task():
    name = mp.current_process().name
    print(f'Process{name} rozpoczęty')
    time.sleep(2)
    print(f'proces {name} zakończony')

if __name__ == '__main__':
    deamon_process = mp.Process(target=deamon_task, name='Deamon process')
    deamon_process.daemon = True
    nondeamon_process = mp.Process(target=nondeamon_task, name='Non_deamon process')
    nondeamon_process.daemon = False
    deamon_process.start()
    nondeamon_process.start()

    nondeamon_process.join()

    print('Koniec')