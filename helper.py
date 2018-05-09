from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.app import App
from functools import partial
from threading import Timer
import db_ops
import json


class CustomTextInput(TextInput):

    def __init__(self, field=None, **kwargs):
        super().__init__(**kwargs)
        self.field = field


class CustomButton(Button):

    def __init__(self, name=None, addr=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.addr = addr


class Transaction(Popup):

    def __init__(self, data=None, cust_id=None, editable=True, 
                 **kwargs):
        super().__init__(**kwargs)
        self.cust_id = cust_id
        self.config = self.get_config('transaction.json')
        self._id = self.config['id']

        # add header
        add_item_in_tab(self, self.config['columns'], self.config['type'])

        # view transactions
        if not editable:
            self.fill_data(data)

        # add new or update transaction
        else:
            self.fill_fields(data)

    def get_config(self, conf_file):
        with open('configs/{}'.format(conf_file)) as f:
            config = json.load(f)
        return config

    def fill_data(self, data):
        self.content.children[0].add_new_rows(
            1, self.config['columns'], len(data), data, cust_id=self.cust_id,
            editable=False)

    def fill_fields(self, data=None):
        target = self.content.children[0]
        target.add_new_rows(1, self.config['columns'], 1, data,
                            cust_id=self.cust_id)
        add_buttons(self, self.config['buttons'])


class Table(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_new_rows(self, sno, cols, n, data=None, editable=True,
                     cust_id=None):
        for i in range(n):
            self.add_widget(Label(
                text=str(sno+i),
                size=(50, 30),
                size_hint=(None, None)))
            for col in cols[1:]:
                width = (1 if col['wid'] is 0 else None)
                
                if data and col['id'] == 'action':
                    self.add_widget(Button(
                        size=(col['wid'], 30),
                        size_hint=(width, None),
                        text='Edit',
                        on_release=partial(edit_transac, '', [data[i]],
                                           cust_id, source=self.parent)
                    ))
                elif editable is True:
                    self.add_widget(CustomTextInput(
                        size=(col['wid'], 30),
                        size_hint=(width, None),
                        field=col['id'],
                        text=(data[i].get(col['id']) if data else '')
                    ))
                elif data:
                    self.add_widget(Label(
                        size=(col['wid'], 30),
                        size_hint=(width, None),
                        text=data[i][col['id']]
                    ))

    def save_entry(self, tab, *args):
        rows = int(len(self.children)/self.cols)
        entries = []
        for i in range(rows-1):
            entry = {}
            for j in range(self.cols-1):  # ignore the S. No.
                cell = self.children[i*self.cols+j]
                # print(cell.text)
                entry[cell.field] = cell.text.strip()
                cell.text = ''
            # check if whole row is empty
            if all([v == '' for v in entry.values()]):
                continue
            entries.append(entry)
        msg = db_ops.insert_update_many(tab._id, entries, tab.cust_id)
        print(msg)
        show_msg(msg)

    def cancel(self, popup, *args):
        # this function assumes the table is in Popup widget
        popup.dismiss()


def edit_transac(transac_id, data, cust_id, *args, source=None, **kwargs):
    if source:
        source.parent.parent.parent.dismiss()
    Transaction(data=data, cust_id=cust_id, title=cust_id).open()

def add_item_in_tab(tab_widget, columns, tab_type=None, n_rows=0):
    n_cols = len(columns)
    tab_content = BoxLayout(orientation='vertical')
    table = Table(cols=n_cols)
    for col in columns:
        width = (1 if col['wid'] is 0 else None)
        table.add_widget(Label(
            text=col['text'],
            size=(col['wid'], 50),
            size_hint=(width, None)
        ))
    tab_content.add_widget(table)
    tab_widget.add_widget(tab_content)

def add_buttons(target, buttons):
    # btn id is should be same as the call function name for that button
    # and must be defined in Table class
    table = target.content.children[0]
    for btn in buttons:
        target.content.add_widget(Button(
            text=btn['text'],
            on_release=partial(getattr(table, btn['id']), target)
        ))

def calculate_bal(transacs):
    if transacs is None:
        return 0
    
    debit = 0
    credit = 0
    for t in transacs:
        debit += (int(t['debit']) if t['debit'] is not '' else 0)
        credit += (int(t['credit']) if t['credit'] is not '' else 0)
    return (credit - debit)

def clear_msg(box, a):
    box.text = ''
    
def show_msg(msg):
    msg_box = App.get_running_app().root.children[0].msg_box
    msg_box.text = msg[1]
    msg_box.color = ([0, 0.5, 0, 1] if msg[0] == 0 else [0.5, 0, 0, 1])
    Timer(3, clear_msg, (msg_box, 'x')).start()
    
