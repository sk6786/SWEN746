from abc import ABC, abstractmethod


class Observer:
    """
    Observer interface for the Observer design pattern. Provides a means for the Subject to update its Observers.
    """

    @abstractmethod
    def update(self):
        """
        Force the Observer to update according to the Subject that called it.
        :param subject: Subject that is updating the Observer.
        :return: void.
        """
        pass
