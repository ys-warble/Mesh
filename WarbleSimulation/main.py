import time
import uuid
from multiprocessing import Process, Queue, Pipe

from WarbleSimulation.System.Entity.Concrete.Light import Light
from WarbleSimulation.System.Entity.Function.Tasked import Task
from WarbleSimulation.System.Entity.Task import Command

if __name__ == '__main__':
    light1 = Light(uuid=uuid.uuid4())
    light2 = Light(uuid=uuid.uuid4())

    result_queue = Queue()
    light1_ppipe, light1_cpipe = Pipe()
    light2_ppipe, light2_cpipe = Pipe()
    light1_p = Process(target=light1.run, args=(result_queue, light1_cpipe))
    light2_p = Process(target=light2.run, args=(result_queue, light2_cpipe))

    light1_p.start()
    light2_p.start()

    print('Send pipe 1')
    light1_ppipe.send(Task(Command.END))
    print(light1_ppipe.recv())
    time.sleep(1)

    print('Send pipe 2')
    light2_ppipe.send(Task(Command.END))
    print(light2_ppipe.recv())
    time.sleep(1)

    light1_p.join()
    light2_p.join()
