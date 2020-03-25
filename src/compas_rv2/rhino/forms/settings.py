from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import compas
import ast
from compas_rv2.rhino import get_scene

try:
    import Eto.Drawing as drawing
    import Eto.Forms as forms
except Exception:
    compas.raise_if_ironpython()


__all__ = ["SettingsForm"]


class Tree_Table(forms.TreeGridView):
    def __init__(self, ShowHeader=True, table_type=None):
        self.ShowHeader = ShowHeader

    @classmethod
    def from_settings(cls, settings):
        table = cls(ShowHeader=True)
        table.settings = settings
        table.new_settings = settings.copy()
        table.settings_data_type = {key: type(settings[key]) for key in settings}

        table.add_column("Property")
        table.add_column("Value", Editable=True)
        treecollection = forms.TreeGridItemCollection()

        keys = list(settings.keys())
        keys.sort()
        for key in keys:
            treecollection.Add(forms.TreeGridItem(Values=(key,  str(settings[key]))))

        table.DataStore = treecollection
        table.CellEdited += table.EditEvent()
        return table

    def EditEvent(self):
        def on_edited(sender, event):

            try:
                key = event.Item.Values[0]
                new_value = event.Item.Values[event.Column]
                if new_value != '-':
                    # parse new input value
                    try:
                        parsed = ast.literal_eval(new_value)
                    except Exception:
                        parsed = str(new_value)

                    data_type = self.settings_data_type[key]
                    original_value = self.settings[key]

                    # convert int to float if needed
                    if data_type == float and type(parsed) == int:
                        parsed = float(parsed)

                    # final type check
                    if parsed != original_value:
                        if type(parsed) == data_type:
                            self.new_settings[key] = parsed
                            print('updated %s from %s to %s' % (key, original_value, parsed))
                            # get_scene().update()
                        else:
                            print('Invalid value type! Needs', data_type)
                            event.Item.Values[event.Column] = str(original_value)
                    else:
                        print('value not changed from', original_value)

            except Exception as e:
                print(e)
        return on_edited

    def add_column(self, HeaderText=None, Editable=False):
        column = forms.GridColumn()
        if self.ShowHeader:
            column.HeaderText = HeaderText
        column.Editable = Editable
        column.DataCell = forms.TextBoxCell(self.Columns.Count)
        column.Sortable = True
        self.Columns.Add(column)

    def apply(self):
        self.settings.update(self.new_settings)


class SettingsForm(forms.Form):

    @classmethod
    def from_scene(cls, scene):

        all_settings = {}
        for key in scene.nodes:
            node = scene.nodes[key]
            all_settings[node.name] = node.settings

        settingsForm = cls()
        settingsForm.scene = scene
        settingsForm.setup(all_settings)
        settingsForm.Show()
        return settingsForm

    def setup(self, all_settings):

        self.Title = "Settings"
        self.TabControl = self.tabs_from_settings(all_settings)
        tab_items = forms.StackLayoutItem(self.TabControl, True)
        layout = forms.StackLayout()
        layout.Spacing = 5
        layout.HorizontalContentAlignment = forms.HorizontalAlignment.Stretch
        layout.Items.Add(tab_items)

        sub_layout = forms.DynamicLayout()
        sub_layout.AddRow(None, self.ok, self.cancel)
        layout.Items.Add(forms.StackLayoutItem(sub_layout))

        self.Content = layout
        self.Padding = drawing.Padding(12)
        self.Resizable = True
        self.ClientSize = drawing.Size(400, 600)

    def tabs_from_settings(self, all_settings):
        control = forms.TabControl()
        control.TabPosition = forms.DockPosition.Top

        for object_name in all_settings:
            tab = forms.TabPage()
            tab.Text = object_name
            tab.Content = Tree_Table.from_settings(all_settings[object_name])
            control.Pages.Add(tab)

        return control

    @property
    def ok(self):
        self.DefaultButton = forms.Button(Text='OK')
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    def on_ok(self, sender, event):
        try:
            for page in self.TabControl.Pages:
                page.Content.apply()
            self.scene.update()
        except Exception as e:
            print(e)
        self.Close()

    def on_cancel(self, sender, event):
        self.Close()


if __name__ == "__main__":

    scene = get_scene()
    SettingsForm.from_scene(scene)
