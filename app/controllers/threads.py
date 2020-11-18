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
            self._target()

        def join(self):
            self._stoped = True