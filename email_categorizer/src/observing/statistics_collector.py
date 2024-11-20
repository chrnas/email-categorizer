from .base import BaseModel
from .observe import Observer
from context_classification.context import ContextClassifier

class StatCollector (Observer):
    
    def update(context: ContextClassifer):
        context.print_results()
        