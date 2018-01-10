import kivy
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty
import json
import db_ops
import helper
from helper import CustomButton, CustomTextInput

Builder.load_file('kvs/elements.kv')

class Tab(TabbedPanelItem):

    def __init__(self, tab_id, cust_id=None, **kwargs):
        super().__init__(**kwargs)
        self._id = tab_id
        self.cust_id = cust_id


class SearchTab(BoxLayout):

    def __init__(self, box, **kwargs):
        super().__init__(**kwargs)
        self.box = box

    def search(self):
        res = db_ops.find('customers', 'name', self.ids.search_box.text)
        self.display_result(res)

    def display_result(self, results):
        if self.box is None or len(results) == 0:
            return
        self.box.clear_widgets()        
        for res in results:
            balance = helper.calculate_bal(res.get('transactions'))
            self.box.add_widget(Label(text=res['name']))
            self.box.add_widget(Label(text=res['addr']))
            self.box.add_widget(Label(text=str(balance) ))
            self.box.add_widget(CustomButton(text='View', name=res['name'],
                on_release=self.view_transac))
            self.box.add_widget(CustomButton(text='Add New', name=res['name'],
                on_release=self.add_transac))

    def view_transac(self, btn, *args):
        transacs = db_ops.find('customers', 'name', btn.name, 'transactions')
        popup = Transaction('transaction.json', data=transacs, title=btn.name)
        popup.open()

    def add_transac(self, btn, *args):
        popup = Transaction('transaction.json', cust_id=btn.name,
            title=btn.name)
        popup.open()




class Transaction(Popup):

    def __init__(self, conf_file, data=None, cust_id=None, **kwargs):
        super().__init__(**kwargs)
        self.cust_id = cust_id
        self.config = self.get_config(conf_file)
        self._id = self.config['id']

        # add header
        helper.add_item_in_tab(self, self.config['columns'],
                               self.config['type'])
        # view transactions
        if data is not None:
            self.fill_data(data)
        # add new transaction
        if cust_id is not None:
            self.fill_fields()

    def get_config(self, conf_file):
        with open('configs/{}'.format(conf_file)) as f:
            config = json.load(f)
        return config

    def fill_data(self, data):
        self.content.children[0].add_new_rows(
                1, self.config['columns'], len(data), data)

    def fill_fields(self):
        target = self.content.children[0]
        target.add_new_rows(1, self.config['columns'], 1)
        helper.add_buttons(self, self.config['buttons'])


class Elements(Widget):

    msg_box = ObjectProperty()

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.element_file = 'configs/elements.json'
        self.elements = self.get_elements()
        self.ids.org_logo.text = self.elements['org_name']
        #self.add_common_fields()
        self.add_tabs()

    def get_elements(self):
        with open(self.element_file) as f:
            elements = json.load(f)
        return elements

    def add_common_fields(self):
        for field in self.elements['common_fields']:
            self.ids.common_fields.add_widget(
                Label(text=field))
            self.ids.common_fields.add_widget(
                TextInput(multiline=False))

    def add_tabs(self):
        need_default = True
        for tab in self.elements['tabs']:
            if tab['visible'] == "true":
                tab_widget = Tab(tab['tab_id'], text=tab['title'])

                # add header
                helper.add_item_in_tab(tab_widget, tab['columns'],
                    tab['type'], tab['default_rows'])

                # add text fields and buttons for entry type tabs
                if tab['type'] == 'entry':
                    tab_widget.content.children[0].add_new_rows(
                        1, tab['columns'], tab['default_rows'])
                    helper.add_buttons(tab_widget,
                        tab['buttons'])

                # add search box and results header
                if tab['type'] == 'search':
                    self.fill_search_tab(
                        tab_widget,
                        tab['columns'],
                        tab['type']
                    )
                if need_default:
                    self.ids.tab_panel.default_tab = tab_widget
                    need_default = False
                self.ids.tab_panel.add_widget(tab_widget)

    def fill_search_tab(self, tab_widget, columns, tab_type):
        results = BoxLayout()
        # fill results with columns header
        helper.add_item_in_tab(results, columns, tab_type, 0)
        # add search box
        search = SearchTab(results.children[0].children[0])
        tab_content = BoxLayout(orientation='vertical')
        tab_content.add_widget(search)
        tab_content.add_widget(results)
        tab_widget.add_widget(tab_content)
