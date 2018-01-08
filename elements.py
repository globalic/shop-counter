import kivy
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.lang import Builder
import json
import connect_db

Builder.load_file('kvs/elements.kv')

class CustomTextInput(TextInput):

    def __init__(self, field=None, **kwargs):
        super().__init__(**kwargs)
        self.field = field


class Tab(TabbedPanelItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Table(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_new_rows(self, sno, cols, n):
        for i in range(n):
            self.add_widget(Label(
                text=str(sno+i),
                size=(50, 30),
                size_hint=(None, None)))
            for col in cols[1:]:
                width = (1 if col['wid'] is 0 else None)
                self.add_widget(CustomTextInput(
                    size=(col['wid'], 30),
                    size_hint=(width, None),
                    field=col['id']
                ))


class SearchTab(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, q, box=None):
        res = ['nikhil', 'kushmiliya', 200]
        if box is not None:
            self.display_result(res, box)

    def display_result(self, res, box):
        box.add_widget(Label(text=res[0]))
        box.add_widget(Label(text=res[1]))
        box.add_widget(Label(text=str(res[2])))
        box.add_widget(Button(text='View'))
        box.add_widget(Button(text='Add New'))

            
class Elements(Widget):
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.element_file = 'configs/elements.json'
        self.elements = self.get_elements()
        self.ids.org_logo.text = self.elements['org_name']
        self.add_common_fields()
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
        for tab in self.elements['tabs']:
            if tab['visible'] == "true":
                tab_widget = Tab(text=tab['title'])

                if tab['type'] == 'entry':
                    self.add_item_in_tab(
                        tab_widget,
                        tab['columns'],
                        tab['type'],
                        tab['default_rows']
                    )

                    
                elif tab['type'] == 'search':
                    self.fill_search_tab(
                        tab_widget,
                        tab['columns'],
                        tab['type']
                    )

                self.ids.tab_panel.add_widget(tab_widget)

    def add_item_in_tab(self, tab_widget, columns, tab_type, n_rows):
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
        if tab_type == 'entry':
            table.add_new_rows(1, columns, n_rows)
        tab_content.add_widget(table)
        if tab_type == 'entry':
            tab_content.add_widget(Button(text='Add New'))
            tab_content.add_widget(Button(text='Save',
                                          on_release=self.save_entry))
        tab_widget.add_widget(tab_content)

    def fill_search_tab(self, tab_widget, columns, tab_type):
        search = SearchTab()
        results = BoxLayout()
        self.add_item_in_tab(results, columns, tab_type, 0)
        # add results
        search.search('q', results.children[0].children[0])
        tab_content = BoxLayout(orientation='vertical')
        tab_content.add_widget(search)
        tab_content.add_widget(results)
        tab_widget.add_widget(tab_content)

    def save_entry(self, btn, *args):
        table = btn.parent.children[-1]
        rows = int(len(table.children)/table.cols)
        customers = []
        for i in range(rows-1):
            cust = {}
            for j in range(table.cols-1):  # ignore the S. No.
                cell = table.children[i*table.cols+j]
                print(cell.text)
                cust[cell.field] = cell.text
                cell.text = ''
            customers.append(cust)
        ids = connect_db.insert_multi('customers', customers)
        print(ids)
                
