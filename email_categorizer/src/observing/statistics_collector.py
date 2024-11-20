from .observe import Observer
from context_classification.context import ContextClassifier

class StatCollector(Observer):
    
    def __init__(self):
        self.statistics = None

    def update(self, event_type, statistics):
        if event_type != 'evaluating':
            return  # Ignore irrelevant events
        # Handle relevant event
        # Get statistics from the context
        self.statistics = statistics
        self.display()

    def display(self):
        # Print collected statistics
        print(self.statistics)