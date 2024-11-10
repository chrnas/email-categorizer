import pandas as pd
from .data_processor import (
    DataProcessor,
    NoiseRemovalDecorator,
    TranslatorDecorator,
    DeDuplicationDecorator,
    UnicodeConversionDecorator
)


class DataPreProcessorFactory:
    @staticmethod
    def create_data_preprocessor(df: pd.DataFrame, pre_processing_features: list[str]):

        data_preprocessor = DataProcessor(df)
        for feature in pre_processing_features:
            if feature == "noise_removal":
                data_preprocessor = NoiseRemovalDecorator(data_preprocessor)
            elif feature == "translation":
                data_preprocessor = TranslatorDecorator(data_preprocessor)
            elif feature == "deduplication":
                data_preprocessor = DeDuplicationDecorator(data_preprocessor)
            elif feature == "unicode_conversion":
                data_preprocessor = UnicodeConversionDecorator(data_preprocessor)
            else:
                raise ValueError(f"Unknown feature type: {feature}")

        return data_preprocessor
