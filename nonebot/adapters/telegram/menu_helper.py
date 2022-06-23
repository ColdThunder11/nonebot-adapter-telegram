import inspect
import uuid
from typing import Dict, List, Callable
from .adapter import Adapter
from .event import MessageEvent,CallbackQueryEvent
from .message import MessageBody
from .exception import MenuHandleFailed


class MenuManager:

    adapter: "Adapter"
    registed_menus: "List['InlineKeyboardMenuBase']" = []

    def __init__(self) -> None:
        pass

    @classmethod
    def set_adapter(adapter):
        MenuManager.adapter = adapter

    @classmethod
    def regist_menu(menu: "InlineKeyboardMenuBase"):
        MenuManager.registed_menus.append(menu)

    @classmethod
    def process_callback(event:"CallbackQueryEvent") -> bool:
        for menu in MenuManager.registed_menus:
            if menu.replyEvent.get_session_id() == event.get_session_id() and event.callback_query.data in menu.callbackHandlers.keys():
                try:
                    menu.callbackHandlers[event.callback_query.data].func(menu,event)
                    return True
                except Exception as err:
                    raise MenuHandleFailed(innerError=err)
        return False

class InlineKeyboardMenuItemData:
    def __init__(self, func: Callable, text: str, row: int, column: int, url: str = None) -> None:
        self.func = func
        self.text = text
        self.row = row
        self.column = column
        self.url = url

class InlineKeyboardMenuBase:
    previousMenu: "InlineKeyboardMenuBase"
    msgText: str

    def __init__(self, event: "MessageEvent", text: str) -> None:
        self.replyEvent = event
        self.messageId: str = None
        self.callbackHandlers: Dict[str, InlineKeyboardMenuItemData] = {}
        self.msgText = text
        # regist callback methods
        mbs = inspect.getmembers(self)
        for key, value in mbs:
            if key != "menu_item" and str(type(value)) == "<class 'method'>" and value.__func__ and "InlineKeyboardMenuBase.menu_item" in value.__func__.__qualname__:
                value.__func__(self)

    def switch_to_menu(self, target_menu: "InlineKeyboardMenuBase"):
        pass

    def regist_menu_item(self, func: Callable, text: str, row: int, column: int, url: str = None):
        self.callbackHandlers[func.__qualname__] = InlineKeyboardMenuItemData(
            func, text, row, column, url)

    @classmethod
    def menu_item(cls, text: str, row: int, column: int, url: str = None, callback_data_name: str = None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                #print("wraper called")
                self_item: InlineKeyboardMenuBase = args[0]
                self_item.regist_menu_item(func, text, row, column, url)
                # return func(*args, **kwargs)
                return None
            return wrapper
        return decorator


class WikiCallbackMenu(InlineKeyboardMenuBase):

    @InlineKeyboardMenuBase.menu_item("test", 1, 1)
    def handle_click(self,event):
        print("method_called")
        pass


if __name__ == "__main__":
    cb = WikiCallbackMenu()
    cb.build_menu_send_message()
