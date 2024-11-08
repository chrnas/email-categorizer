from email_classifier import EmailClassifier
from data_preparation.data_processor import DataProcessor
from feature_engineering.base_embeddings import BaseEmbeddings
from models.classification_factory import ClassificationFactory


class EmailClassifierFactory:

    @staticmethod
    def create_email_classifier(
        embeddings: list[str],
        pre_processing_features: list[str],
        classification_algorithm: str
    ):
        feature_engineer = BaseEmbeddings(embeddings)
        data_processor = DataProcessor(pre_processing_features)
        classification_factory = ClassificationFactory()
        classification_algorithm = classification_factory.create_classification_algorithm(
            classification_algorithm)
        email_classifier = EmailClassifier(
            feature_engineer, data_processor, classification_algorithm)
        return email_classifier
