from threading import Event, Thread
from queue import Queue
from urllib.parse import urljoin
from requests import get


class Worker(Thread):
    """Hand down of Thread's superclass.

    Subscribing the run's function because the event must
    wait for requests to be in queue."""
    

    def __init__(self, target, *, name='Worker'):
        super().__init__()
        self.name = name
        self._target = target
        self._stoped = False 
        print(self.name, 'started')

        def run(self):
            event.wait()
            while not self.queue.empty():
                request = self.queue.get()
                print(self.name, request)
                if request == 'Kill':
                    self.queue.put(response)
                    self._stoped = True
                break
                self._target(request)

        def join(self):
            while not self._stoped:
                sleep(0.1)