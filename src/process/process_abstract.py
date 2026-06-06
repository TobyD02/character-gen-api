import abc


class ProcessAbstract(abc.ABC):
    @abc.abstractmethod
    def execute(self, *args, **kwargs):
            pass