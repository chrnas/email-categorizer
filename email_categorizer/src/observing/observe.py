from context_classification.context import ContextClassifier

class Observer:
    
    def update(context: ContextClassifier):
        # collect the values 
        context.print_results()