from abc import ABC, abstractmethod

from ..driver import Driver

class Attend(ABC, Driver):
    def __init__(self, **kwargs):
        super(ABC).__init__()
        self.__meet_url = None

        try:
            self._driver = kwargs["driver"]
        except (KeyError): pass

        try: self.set_meeting_url(kwargs["code"])
        except KeyError: pass


    @abstractmethod
    def goto_meet(self): raise NotImplementedError

    @abstractmethod
    def set_meeting_url(self, code): raise NotImplementedError

    @property
    def meet_url(self):
        return self.__meet_url
