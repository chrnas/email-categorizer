from abc import ABC, abstractmethod


class Client:
    def __init__(self):
        self.email_service = EmailService()
        self.email_client = EmailClient()

    def classify_email(self):
        classify_command = ClassifyEmailCommand(self.email_service)
        self.email_client.execute_command(classify_command)

    def mark_as_spam(self):
        spam_command = MarkAsSpamCommand(self.email_service)
        self.email_client.execute_command(spam_command)


# Receiver class with methods for email classification and marking as spam
class EmailService:
    used: bool

    def __init__(self):
        self.used = False

    def classify_email(self):
        print(f"Classifying email as, used{self.used}")

    def mark_as_spam(self):
        print(f"Marking email as spam, used: {self.used}")


# Abstract Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# Concrete Command to classify an email
class ClassifyEmailCommand(Command):
    def __init__(self, email_service):
        self.email_service = email_service

    def execute(self):
        self.email_service.classify_email()
        self.email_service.used = True


# Concrete Command to mark an email as spam
class MarkAsSpamCommand(Command):
    def __init__(self, email_service):
        self.email_service = email_service

    def execute(self):
        self.email_service.mark_as_spam()
        self.email_service.used = True


# Invoker class to execute commands
class EmailClient:
    def __init__(self):
        self.history = []  # to keep track of commands executed

    def execute_command(self, command):
        command.execute()
        self.history.append(command)  # keep a history of executed commands


# Usage example
if __name__ == "__main__":
    email_service = EmailService()
    email_client = EmailClient()

    # Create and execute a classify email command
    classify_command = ClassifyEmailCommand(email_service)
    email_client.execute_command(classify_command)
    print(f"used,changed in main?:  {email_service.used}")
    # Create and execute a mark as spam command
    spam_command = MarkAsSpamCommand(email_service)
    email_client.execute_command(spam_command)
