from langchain.prompts import MessagesPlaceholder


class CustomMessagesPlaceholder(MessagesPlaceholder):

    def __init__(self, variable_name, **kwargs):
        return super().__init__(variable_name=variable_name, **kwargs)

    def format_messages(self, **kwargs):
        list = super().format_messages(**kwargs)
        return list[-10:]