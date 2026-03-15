from openai import OpenAI
from dataclasses import dataclass
from enum import Enum
import logging
import json
from datetime import datetime
from sys import exit

from confg import OPENAI_API_KEY, BASE_URL, MODEL, DEFAULT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class Role(Enum):
    SYSTEM = 'system'
    USER = 'user'
    AGENT = 'assistant'

@dataclass
class Message:
    role: str
    message: str

@dataclass
class Dialog:
    user_id: int
    messages: list[Message]

# TODO Implement class for storage
class ChatsInMemory:
    def __init__(self, dialogs:str=''):
        self.dialogs = self.get_dialogs_from_json(dialogs) if dialogs else dict()

# TODO implement paring pfom JSON
    def get_dialogs_from_json(self, dialogs:str) -> dict:
        logger.warning(f"Not implemented <ChatsInMemoty.get_dialogs_from_json()>. \
            Can't parse JSON {dialogs[:20]}")
        return {}
    
    def add_message(self, message: Message, user_id:int) -> Dialog:
        self.dialogs[user_id].messages.append(message)
        return self.get_messages(user_id)

    def get_messages(self, user_id:int) -> Dialog:
        return self.dialogs[user_id]
    
    def is_system_prompt(self, user_id:int) -> bool:
       ##  print(self.get_messages(user_id))
        return True if self.get_messages(user_id).messages[0] else False

    def set_system_prompt(self, user_id:int, prompt:str) -> None:
        try:
            self.get_messages(user_id)
        except KeyError:
            self.dialogs[user_id] = Dialog(user_id, [Message(Role.SYSTEM.value, prompt)])
        else:
            self.dialogs[user_id].messages[0] = Dialog(user_id, [Message(Role.SYSTEM.value, prompt)])

    def dump_dialogs(self) -> None:
        with open(f'{datetime.now()}-messages.json', 'w') as f:
            f.writelines(json.dumps(self.dialogs))


class Messaging:
    def __init__(self, api_key:str, model:str, base_url:str, storage=ChatsInMemory, dialogs:str='') -> None:
        self.storage = storage(dialogs=dialogs)
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    def set_system_promt(self, user_id:int, prompt:str='') -> None:
        if prompt:
            self.storage.set_system_prompt(user_id, prompt)
        else:
            self.storage.set_system_prompt(user_id, DEFAULT_SYSTEM_PROMPT)


    def send_message(self, message:str, user_id:int) -> str:
        if not self.storage.is_system_prompt(user_id):
            logging.error("Не уставновлен системный промпт")
            exit(1) 
    
        messages = self.storage.add_message(Message(Role.USER.value, message), user_id).messages
        messages = [{'role': m.role, 'content': m.message,} for m in messages]
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            
        completion = client.chat.completions.create(

                model=self.model,
                store=True,
                messages=messages
        )
        res = completion.choices[0].message
        if res.content:
            self.storage.add_message(Message(Role.AGENT.value, res.content), user_id)
            return res.content
        else:
            return "Что-то пошло не так"

if __name__ == '__main__':
    prompt = input('Введите системный промпт или оставьте пустым, exit для выхода: ')
    if prompt == 'exit':
        exit(0)
    user_id = input('Введите ваше имя или набор цифр для идентификации: ')
    chat = Messaging(api_key=OPENAI_API_KEY, model=MODEL, base_url=BASE_URL)
    chat.set_system_promt(user_id, f"{prompt} Собеседника зовут {user_id}. Если здесь \
что-то непохожее на имя, значит это просто ID")
    
    from rich.console import Console
    import readline
    from rich.markdown import Markdown
    console = Console()
    while True:
        lines = []
        print("===================================\n\nВведите собщение, для выхода \
Exit (Enter на пустой строке для завершения):")
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        message = "\n".join(lines)
        if message.strip() == 'exit':
            # TODO implement dumping chats
            exit(0)
        print("\n==== Ждем ответа агента! ====\n")
        responce = chat.send_message(message, user_id)
        print(f"=================================\n{datetime.now()}\nAGENT says: ")
        console.print(Markdown(responce))

