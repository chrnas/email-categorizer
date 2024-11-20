from context_classification.context import ContextClassifier
from abc import ABC, abstractmethod

class Observer(ABC):
    
    @abstractmethod
    def update(self, context: ContextClassifier):
        """
        Receive update from subject.
        """ 
        ...

    def display(self):
        ...