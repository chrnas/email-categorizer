from configuration_manager import ConfigurationManager
from data_preparation.data_processor import DataProcessor, DataProcessorDecorator
from feature_engineering.base_embeddings import BaseEmbeddings
from models.classification_strategy import ClassificationStrategy
from data_preparation.dataset_loader import DatasetLoader
import pandas as pd


class EmailClassifierFacade():
    df: pd.DataFrame
    emails: list[str]
    data_preprocessor: DataProcessor
    base_embeddings: BaseEmbeddings
    classification_strategy: ClassificationStrategy
    data_set_loader: DatasetLoader
    configuration_manager: ConfigurationManager

    def __init__(self,
                 data_preprocessor: DataProcessor,
                 base_embeddings: BaseEmbeddings,
                 classification_strategy: ClassificationStrategy):
        self.df = None
        self.emails: list[str] = []
        self.data_preprocessor = DataProcessor,
        self.base_embeddings = BaseEmbeddings,
        self.classification_strategy = ClassificationStrategy
        self.data_set_loader = DatasetLoader()

    def add_emails(self, path):
        self.emails = self.data_set_loader.read_data(path)
        self.emails = self.data_set_loader.renameColumns(self.df)

    def classify_emails(self):
        self.data_preprocessor.process(self.emails)
        self.base_embeddings.create_embeddings()
        self.classification_strategy.classify(self.emails)

    def change_strategy(self, strategy: ClassificationStrategy):
        self.classification_strategy.changeStrategy(strategy)

    def add_preprocessing(self, pre_processing_feature: DataProcessorDecorator):
        self.data_preprocessor.addPreprocessing(pre_processing_feature)

    def train_models(self, path):
        # load the data
        self.df = self.data_set_loader.read_data(path)
        self.df = self.data_set_loader.renameColumns(self.df)

        # preproccess the data
        self.df = self.data_preprocessor.process()

        # feature engineering
        self.base_embeddings.create_embeddings()
        X = self.base_embeddings.get_embeddings()

        # modelling
        ...

    def displayEvaluation(self):
        ...
