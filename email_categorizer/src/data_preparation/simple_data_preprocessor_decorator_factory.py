import pandas as pd
from .data_processor import (
    NoiseRemovalDecorator,
    TranslatorDecorator,
    DeDuplicationDecorator,
    UnicodeConversionDecorator,
    DataProcessorDecorator
)


class SimpleDataPreProcessorDecoratorFactory:
    @staticmethod
    def create_data_preprocessor(feature: str) -> DataProcessorDecorator:

        if feature == "noise_removal":
            return NoiseRemovalDecorator
        elif feature == "translation":
            return TranslatorDecorator
        elif feature == "deduplication":
            return DeDuplicationDecorator
        elif feature == "unicode_conversion":
            return UnicodeConversionDecorator
        else:
            raise ValueError(f"Unknown feature type: {feature}")
