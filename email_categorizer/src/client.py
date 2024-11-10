import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import InMemoryHistory
from email_classifier_facade import EmailClassifierFacade
from email_classifier_factory import EmailClassifierFactory
from data_preparation.dataset_loader import DatasetLoader


class Client:

    email_classifier: EmailClassifierFacade
    data_set_loader: DatasetLoader

    def __init__(self):
        self.data_set_loader = DatasetLoader()

    def print_startup(self):
        print("Startup complete")
        print("Welcome to Email Classifier application.")

    def run_cli(self):
        parser = create_parser()
        history = InMemoryHistory()
        completer = create_completer()

        self.print_startup()

        while True:
            try:
                input_str = prompt("> ", completer=completer, history=history)
                if input_str.strip().lower() == 'exit':
                    print("Exiting CLI.")
                    break
                args = parser.parse_args(input_str.split())
                self.handle_command(args)
            except SystemExit:
                # argparse throws a SystemExit exception if parsing fails, we'll catch it to keep the loop running
                continue
            except Exception as e:
                print(f"Error: {e}")

    def handle_command(self, args) -> bool:
        match args.command:
            case "test":
                print("Args are:")
                for arg in vars(args):
                    if arg != 'command':
                        print(f"{arg}: {getattr(args, arg)}")
                print("test command executed")
            case "add_emails":
                print("Add emails")
            case "classify_emails":
                self.email_classifier.classifyEmails()
            case "create_email_classifier":
                config = {
                    "embeddings": "tfidf",
                    "pre_processing_features": ["noise_removal", "deduplication"],
                    "classification_algorithm": "rainforest"
                }
                print(args.path)
                df = self.data_set_loader.read_data(args.path)
                df = self.data_set_loader.renameColumns(df)
                self.email_classifier = EmailClassifierFactory().create_email_classifier(
                    df=df,
                    embeddings=config["embeddings"],
                    pre_processing_features=config["pre_processing_features"],
                    classification_algorithm=config["classification_algorithm"]
                )
                self.email_classifier.train_model(args.path)
            case "change_strategy":
                self.email_classifier.change_strategy(args.strategy)
            case "add_preprocessing":
                self.email_classifier.add_preprocessing(args.feature)
                print("Preprocessing {args.command} added")
            case "display_evaluation":
                self.email_classifier.displayEvaluation()
            case "exit":
                print("Exiting CLI.")
                exit(0)
            case _:
                print("Unknown command")
        return False


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI for estimating positions based on sound files.")
    subparsers = parser.add_subparsers(dest='command')

    # Test command
    subparsers.add_parser(
        'test', help='Execute a test command to verify CLI functionality.')

    # PosList command
    add_email_parser = subparsers.add_parser(
        'add_emails', help='Classify email comand.')
    add_email_parser.add_argument('path', help='Path to the email files.')

    subparsers.add_parser(
        'classify_emails', help='Classify email comand.')

    # Create email classifier command
    create_email_classifier_parser = subparsers.add_parser(
        'create_email_classifier', help='Create an email classifier.')
    create_email_classifier_parser.add_argument(
        'path', help='Path to the email files.')

    # Change Strategy command
    change_strategy_parser = subparsers.add_parser(
        'change_strategy', help='Change strategy.')
    change_strategy_parser.add_argument(
        'strategy', help='Change strategy to bayes.')

    # Add preprocessing command
    add_pre_processing_parser = subparsers.add_parser(
        'add_preprocessing', help='Add preprocessing.')
    add_pre_processing_parser.add_argument(
        'feature', help='Add translation feature.')

    # Display Evaluation command
    subparsers.add_parser(
        'display_evaluation', help='Display the evaluation of the current positioning method.')

    # Exit command
    subparsers.add_parser('exit', help='Exit the CLI.')

    return parser


def create_completer() -> NestedCompleter:

    # Extract method names and their possible settings
    completer_dict = {
        'test': None,
        'add_emails': None,
        'classify_emails': None,
        'create_email_classifier': None,
        'change_strategy': {'bayes', 'rainforest'},
        'add_preprocessing': {'deduplication, unicode_conversion, noise_removal'},
        'display_evaluation': None,
        'exit': None
    }
    return NestedCompleter.from_nested_dict(completer_dict)


if __name__ == "__main__":
    client = Client()
    client.run_cli()
