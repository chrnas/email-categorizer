from models.base import BaseModel
from .observe import Observer
from context_classification.context import ContextClassifier

class StatCollector(Observer):
    
    def update(self, context: ContextClassifier):
        context.print_results()
        