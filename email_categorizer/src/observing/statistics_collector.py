from .observe import Observer
from context_classification.context import ContextClassifier

class StatCollector(Observer):
    
    def __init__(self):
        self.statistics = None

    def update(self, context: ContextClassifier):
        # Get statistics from the context
        statistics = context.print_results()
        self.statistics = statistics
        self.display()

    def display(self):
        # Print collected statistics
        print(self.statistics)