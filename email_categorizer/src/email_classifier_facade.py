from configuration_manager import ConfigurationManager
from data_preparation.data_processor import (
    DataProcessor, DataProcessorDecorator, DeDuplicationDecorator, 
    TranslatorDecorator, NoiseRemovalDecorator, UnicodeConversionDecorator
)
from feature_engineering.base_embeddings import BaseEmbeddings
from models.classification_strategy import ClassificationStrategy
from data_preparation.dataset_loader import DatasetLoader
import pandas as pd

from feature_engineering.sentence_transformer import SentenceTransformerEmbeddings
from data_preparation.data_preprocessor_factory import DataPreProcessorFactory
from training_data import TrainingData
from models.randomforest import RandomForest


class EmailClassifierFacade():
    df: pd.DataFrame
    emails: list[str]
    data_preprocessor: DataProcessor
    base_embeddings: BaseEmbeddings
    classification_strategy: ClassificationStrategy
    data_set_loader: DatasetLoader
    configuration_manager: ConfigurationManager

    def __init__(self,
                 base_embeddings: BaseEmbeddings,
                 data_preprocessor: DataProcessor,
                 classification_strategy: ClassificationStrategy):
        self.df = None
        self.emails: list[str] = []
        self.data_preprocessor = data_preprocessor,
        self.base_embeddings = base_embeddings,
        self.classification_strategy = classification_strategy
        self.data_set_loader = DatasetLoader()
        self.model = None

    def add_emails(self, path):
        self.emails = self.data_set_loader.read_data(path)
        self.emails = self.data_set_loader.renameColumns(self.df)

    def classify_emails(self):
        self.data_preprocessor.process(self.emails)
        self.base_embeddings.create_embeddings()
        self.classification_strategy.classify(self.emails)

    def change_strategy(self, strategy: ClassificationStrategy):
        self.classification_strategy.change_strategy(strategy)

    def add_preprocessing(self, pre_processing_feature: DataProcessorDecorator):
        self.data_preprocessor = pre_processing_feature(self.data_preprocessor)

    def train_model(self, path):
        self.df = self.data_set_loader.read_data(path)
        self.df = self.data_set_loader.renameColumns(self.df)
        # load the data
        #self.df = self.data_preprocessor.process()
        # preproccess the data
        processor = DataProcessor(self.df)
        processor = DeDuplicationDecorator(processor)
        processor = NoiseRemovalDecorator(processor)
        processor = UnicodeConversionDecorator(processor)
        self.df = processor.process()
        
        # feature engineering
        self.base_embeddings = SentenceTransformerEmbeddings(self.df)
        self.base_embeddings.create_embeddings()
        X = self.base_embeddings.get_embeddings()

        # modelling
        self.data = TrainingData(X, self.df)
        self.model = RandomForest(
            'RandomForest', self.data.get_X_test(), self.data.get_type())
        self.model.train(self.data)
        self.model.predict(self.data)

    def displayEvaluation(self):
        self.model.print_results(self.data)
