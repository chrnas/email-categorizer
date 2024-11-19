from abc import ABC, abstractmethod
from sklearn.metrics import classification_report, confusion_matrix
from training_data import TrainingData

class BaseModel(ABC):
    def __init__(self) -> None:
        ...

    def train(self, data: TrainingData) -> None:
        self.mdl = self.mdl.fit(data.X_train, data.y_train)
        print("training ...")

    def predict(self, data) -> None:
        predictions = self.mdl.predict(data.X_test)
        self.predictions = predictions


    def print_results(self, data):
        print(self.predictions)
        print(classification_report(data.get_y_test(), self.predictions))
        print(confusion_matrix(data.get_y_test(), self.predictions))

    @abstractmethod
    def data_transform(self) -> None:
        return

    # def build(self, values) -> BaseModel:
    def build(self, values={}):
        values = values if isinstance(values, dict) else utils.string2any(values)
        self.__dict__.update(self.defaults)
        self.__dict__.update(values)
        return self

    def predict_emails(self, emails_to_predict):
            predictions = self.mdl.predict(emails_to_predict)
            print(predictions)
            index = 0
            for prediction in predictions:
                index += 1
                print(f"Prediction for email {index}:{prediction}")