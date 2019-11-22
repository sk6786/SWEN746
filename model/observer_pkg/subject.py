from abc import ABC, abstractmethod
from model.observer_pkg.observer import Observer


class Subject(ABC):
    """
    Subject Abstract Class for the Observer design pattern. Provides a means for attaching, detaching, and notifying
    Observers. It is up for the Subject to decide when to notify each Observer.
    """

    def __init__(self):
        self.observers = []

    @abstractmethod
    def attach(self, observer: Observer):
        """
        Attach an Observer to the Subject.
        :param observer: Observer instance to inform about the Subject.
        :return: void.
        """
        pass
    
    @abstractmethod
    def detach(self, observer: Observer):
        """
        Remove an Observer from the Subject.
        :param observer: Observer instance to stop informing about the Subject.
        :return: void.
        """
        pass
