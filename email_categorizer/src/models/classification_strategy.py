from abc import ABC, abstractmethod


class ClassificationStrategy(ABC):
    @staticmethod
    @abstractmethod
    def classify():
        "Implementors must select the default method"
        print("This is the default method")