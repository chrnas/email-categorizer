from .observe import Observer
from context_classification.context import ContextClassifier
from pandas import DataFrame

class ResultDisplayer(Observer):
    
    def __init__(self):
        self.results = []

    def update(self, context: ContextClassifier, emails: DataFrame):
        # Get predictions from the context
        predictions = context.predict_emails()

        # Ensure predictions and emails have the same length
        if len(predictions) != len(emails):
            raise ValueError("The number of predictions does not match the number of emails.")

        # Collect predictions along with corresponding email content
        for email, prediction in zip(emails.itertuples(index=False), predictions):
            self.results.append((prediction, email.content))  # Adjusted order for clarity

        self.display()

    def display(self):
        # Print collected results
        for prediction, email_content in self.results:
            print(f"Prediction: {prediction} | Email: {email_content}")