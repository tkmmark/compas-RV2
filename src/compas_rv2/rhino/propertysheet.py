from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import compas
import ast

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc
    find_object = sc.doc.Objects.Find
    import Eto.Drawing as drawing
    import Eto.Forms as forms
except Exception:
    compas.raise_if_ironpython()

from compas_rv2.rhino import RhinoFormDiagram


__all__ = ["PropertySheet"]


class Tree_Table(forms.TreeGridView):
    def __init__(self, ShowHeader=True):
        self.ShowHeader = ShowHeader
        self.Height = 300
        self.last_sorted_to = None

    @classmethod
    def from_rhinoDiagram(cls, rhinoDiagram):
        table = cls(ShowHeader=False)
        table.add_column()
        table.add_column()

        treecollection = forms.TreeGridItemCollection()
        treecollection.Add(forms.TreeGridItem(Values=('Type', rhinoDiagram.diagram.__class__.__name__)))
        treecollection.Add(forms.TreeGridItem(Values=('Name', rhinoDiagram.artist.name)))
        treecollection.Add(forms.TreeGridItem(Values=('Layer', rhinoDiagram.artist.layer)))

        if hasattr(rhinoDiagram.artist, 'settings'):
            settings = forms.TreeGridItem(Values=('Settings',))
            treecollection.Add(settings)
            for key in rhinoDiagram.artist.settings:
                settings.Children.Add(forms.TreeGridItem(Values=(key, str(rhinoDiagram.artist.settings[key]))))

        table.DataStore = treecollection
        return table

    @classmethod
    def from_vertices(cls, rhinoDiagram):

        diagram = rhinoDiagram.diagram
        table = cls()
        table.add_column('key')
        attributes = list(diagram.default_vertex_attributes.keys())
        attributes.sort()
        for attr in attributes:
            table.add_column(attr, Editable=rhinoDiagram.vertex_attribute_editable(attr))
        treecollection = forms.TreeGridItemCollection()
        for key in diagram.vertices():
            values = [key]
            for attr in attributes:
                values.append(str(diagram.vertex_attribute(key, attr)))
            treecollection.Add(forms.TreeGridItem(Values=tuple(values)))
        table.DataStore = treecollection
        table.Activated += table.SelectEvent(rhinoDiagram, 'guid_vertices')
        table.CellEdited += table.EditEvent(rhinoDiagram, attributes)
        table.ColumnHeaderClick += table.HeaderClickEvent()
        return table

    @classmethod
    def from_edges(cls, rhinoDiagram):
        diagram = rhinoDiagram.diagram
        table = cls()
        table.add_column('key')
        table.add_column('vertices')
        attributes = list(diagram.default_edge_attributes.keys())
        attributes.sort()
        for attr in attributes:
            table.add_column(attr, Editable=rhinoDiagram.edge_attribute_editable(attr))
        treecollection = forms.TreeGridItemCollection()
        for key, edge in enumerate(diagram.edges()):
            values = [key, str(edge)]
            for attr in attributes:
                values.append(diagram.edge_attribute(edge, attr))
            edge_item = forms.TreeGridItem(Values=tuple(values))
            treecollection.Add(edge_item)
            for key in edge:
                vertex_item = forms.TreeGridItem(Values=('', key))
                edge_item.Children.Add(vertex_item)
        table.DataStore = treecollection
        table.Activated += table.SelectEvent(rhinoDiagram, 'guid_edges', 'guid_vertices')
        table.ColumnHeaderClick += table.HeaderClickEvent()
        return table

    @classmethod
    def from_faces(cls, rhinoDiagram):
        diagram = rhinoDiagram.diagram
        table = cls()
        table.add_column('key')
        table.add_column('vertices')
        attributes = list(diagram.default_face_attributes.keys())
        attributes.sort()
        for attr in attributes:
            table.add_column(attr, Editable=rhinoDiagram.face_attribute_editable(attr))
        treecollection = forms.TreeGridItemCollection()
        for key in diagram.faces():
            values = [key, str(diagram.face[key])]
            for attr in attributes:
                values.append(diagram.face_attribute(key, attr))
            face_item = forms.TreeGridItem(Values=tuple(values))
            treecollection.Add(face_item)
            for v in diagram.face[key]:
                vertex_item = forms.TreeGridItem(Values=('', v))
                face_item.Children.Add(vertex_item)
        table.DataStore = treecollection
        table.Activated += table.SelectEvent(rhinoDiagram, 'guid_faces', 'guid_vertices')
        table.ColumnHeaderClick += table.HeaderClickEvent()
        return table

    def SelectEvent(self, rhinoDiagram, guid_field1, guid_field2=None):
        def on_selected(sender, event):
            try:
                rs.UnselectAllObjects()
                key = event.Item.Values[0]
                if key != '':
                    GUIDs = getattr(rhinoDiagram, guid_field1)
                    find_object(GUIDs[key]).Select(True)
                else:
                    key = event.Item.Values[1]
                    GUIDs2 = getattr(rhinoDiagram, guid_field2)
                    find_object(GUIDs2[key]).Select(True)
                rs.Redraw()
            except Exception as e:
                print(e)

        return on_selected

    def EditEvent(self, rhinoDiagram, attributes):
        def on_edited(sender, event):
            # import traceback
            try:
                # raise NotImplementedError("still in dev")
                key = event.Item.Values[0]
                values = event.Item.Values[1:]
                for attr, value in zip(attributes, values):
                    if value != '-':
                        try:
                            rhinoDiagram.diagram.vertex_attribute(key, attr, ast.literal_eval(value))
                        except (ValueError, TypeError):
                            rhinoDiagram.diagram.vertex_attribute(key, attr, value)
                # redraw upaded diagram
                RV2 = sc.sticky["RV2"]
                settings = RV2["settings"]
                rhinoDiagram.draw(settings)
            except Exception as e:
                print(e)
            # traceback.print_exc()

        return on_edited

    def HeaderClickEvent(self):
        def on_hearderClick(sender, event):
            try:
                # print(event.Column.HeaderText)
                sender.sort(event.Column.HeaderText)
            except Exception as e:
                print(e)
        return on_hearderClick

    def add_column(self, HeaderText=None, Editable=False):
        column = forms.GridColumn()
        if self.ShowHeader:
            column.HeaderText = HeaderText
        column.Editable = Editable
        column.DataCell = forms.TextBoxCell(self.Columns.Count)
        column.Sortable = True
        self.Columns.Add(column)

    def sort(self, key):
        headerTexts = [column.HeaderText for column in self.Columns]
        index = headerTexts.index(key)
        print(key, index)

        def getValue(item):
            try:
                value = ast.literal_eval(item.Values[index])
            except (ValueError, TypeError):
                value = item.Values[index]
            return value

        items = sorted(self.DataStore, key=getValue, reverse=True)
        if self.last_sorted_to == key:
            items.reverse()
            self.last_sorted_to = None
        else:
            self.last_sorted_to = key

        self.DataStore = forms.TreeGridItemCollection(items)


class PropertySheet(forms.Form):

    @classmethod
    def from_diagram(cls, rhinoDiagram):
        propertySheet = cls()
        propertySheet.setup(rhinoDiagram)
        propertySheet.Show()
        return propertySheet

    def setup(self, rhinoDiagram):
        self.Title = "Property - " + rhinoDiagram.__class__.__name__
        self.TabControl = self.from_rhinoDiagram(rhinoDiagram)
        tab_items = forms.StackLayoutItem(self.TabControl, True)
        layout = forms.StackLayout()
        layout.Spacing = 5
        layout.HorizontalContentAlignment = forms.HorizontalAlignment.Stretch
        layout.Items.Add(tab_items)
        self.Content = layout
        self.Padding = drawing.Padding(12)
        self.Resizable = False
        self.ClientSize = drawing.Size(400, 600)

    def from_rhinoDiagram(self, rhinoDiagram):
        control = forms.TabControl()
        control.TabPosition = forms.DockPosition.Top

        tab = forms.TabPage()
        tab.Text = "Basic"
        tab.Content = Tree_Table.from_rhinoDiagram(rhinoDiagram)
        control.Pages.Add(tab)

        tab = forms.TabPage()
        tab.Text = "Vertices"
        tab.Content = Tree_Table.from_vertices(rhinoDiagram)
        control.Pages.Add(tab)
        self.vertices_table = tab.Content

        tab = forms.TabPage()
        tab.Text = "Edges"
        tab.Content = Tree_Table.from_edges(rhinoDiagram)
        control.Pages.Add(tab)
        self.edges_table = tab.Content

        if hasattr(rhinoDiagram, 'guid_faces'):
            tab = forms.TabPage()
            tab.Text = "Faces"
            tab.Content = Tree_Table.from_faces(rhinoDiagram)
            control.Pages.Add(tab)
            self.faces_table = tab.Content

        return control


if __name__ == "__main__":

    from compas_rhino.utilities import unload_modules
    unload_modules("compas")

    import compas
    from compas_tna.diagrams import FormDiagram
    from compas_rv2.rhino import RhinoFormDiagram

    filepath = compas.get('faces.obj')
    form = FormDiagram.from_obj(filepath)

    rhinoDiagram = RhinoFormDiagram(form)
    rhinoDiagram.draw({})

    dialog = PropertySheet()
    dialog.setup(rhinoDiagram)
    dialog.Show()
