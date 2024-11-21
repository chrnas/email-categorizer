from .observe import Observer
from context_classification.context import ContextClassifier

class StatCollector(Observer):
    
    def __init__(self):
        self.statistics = None

    def update(self, event_type, statistics):
        print("update stat2")
        if event_type != 'evaluating':
            return  # Ignore irrelevant eventspython
        # Handle relevant event
        print("update stat")
        self.statistics = statistics
        self.display()

    def display(self):
        # Print collected statistics
         for email_class, met in self.statistics.items():
            print(f"Email Type: {email_class}")
            print(f"Precision: {met['precision']}")
            print(f"Recall: {met['recall']}")
            print(f"F1-Score: {met['f1-score']}")
            print(f"Support: {met['support']}")
            print("\n")