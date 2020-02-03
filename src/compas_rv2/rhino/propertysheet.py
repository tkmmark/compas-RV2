from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import compas
import ast

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc
    find_object = sc.doc.Objects.Find
    import System
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

    @classmethod
    def from_sceneNode(cls, sceneNode):
        table = cls(ShowHeader=False)
        table.add_column()
        table.add_column()

        treecollection = forms.TreeGridItemCollection()
        treecollection.Add(forms.TreeGridItem(Values=('Type', sceneNode.diagram.__class__.__name__)))
        treecollection.Add(forms.TreeGridItem(Values=('Name', sceneNode.artist.name)))
        treecollection.Add(forms.TreeGridItem(Values=('Layer', sceneNode.artist.layer)))

        if hasattr(sceneNode.artist, 'settings'):
            settings = forms.TreeGridItem(Values=('Settings',))
            treecollection.Add(settings)
            for key in sceneNode.artist.settings:
                settings.Children.Add(forms.TreeGridItem(Values=(key, str(sceneNode.artist.settings[key]))))

        table.DataStore = treecollection
        return table

    @classmethod
    def from_vertices(cls, sceneNode):

        diagram = sceneNode.diagram
        table = cls()
        table.add_column('key')
        attributes = list(diagram.default_vertex_attributes.keys())
        attributes.sort()
        for attr in attributes:
            table.add_column(attr, Editable=True)
        treecollection = forms.TreeGridItemCollection()
        for key in diagram.vertices():
            values = [key]
            for attr in attributes:
                values.append(str(diagram.vertex_attribute(key, attr)))
            treecollection.Add(forms.TreeGridItem(Values=tuple(values)))
        table.DataStore = treecollection
        table.Activated += table.SelectEvent(diagram.guid_vertices)
        table.CellEdited += table.EditEvent(diagram, attributes)
        
        return table

    @classmethod
    def from_edges(cls, sceneNode):
        diagram = sceneNode.diagram
        table = cls()
        table.add_column('key')
        table.add_column('vertices')
        attributes = list(diagram.default_edge_attributes.keys())
        attributes.sort()
        for attr in attributes:
            table.add_column(attr)
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
        table.Activated += table.SelectEvent(diagram.guid_edges, diagram.guid_vertices)
        return table

    @classmethod
    def from_faces(cls, sceneNode):
        diagram = sceneNode.diagram
        table = cls()
        table.add_column('key')
        table.add_column('vertices')
        attributes = list(diagram.default_face_attributes.keys())
        attributes.sort()
        for attr in attributes:
            table.add_column(attr)
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
        table.Activated += table.SelectEvent(diagram.guid_faces, diagram.guid_vertices)
        return table

    def SelectEvent(self, GUIDs, GUIDs2=None):
        def on_selected(sender, event):
            try:
                rs.UnselectAllObjects()
                key = event.Item.Values[0]
                if key != '':
                    find_object(GUIDs[key]).Select(True)
                else:
                    key = event.Item.Values[1]
                    find_object(GUIDs2[key]).Select(True)
                rs.Redraw()
                print(sender)
            except Exception as e:
                print(e)

        return on_selected

    def EditEvent(self, diagram, attributes):
        def on_edited(sender, event):
            try:
                print('check0')
                key = event.Item.Values[0]
                values = event.Item.Values[1:]
                for attr, value in zip(attributes, values):
                    if value != '-':
                        try:
                            diagram.vertex_attribute(key, attr, ast.literal_eval(value))
                        except (ValueError, TypeError):
                            diagram.vertex_attribute(key, attr, value)

                # redraw diagram to update
                RV2 = sc.sticky["RV2"]
                form = RV2["data"]["form"]
                if not form:
                    return
                settings = RV2["settings"]
                rfdiagram = RhinoFormDiagram(form)
                rfdiagram.draw(settings)

            except Exception as e:
                print(e)

        return on_edited

    def add_column(self, HeaderText=None, Editable=False):
        column = forms.GridColumn()
        if self.ShowHeader:
            column.HeaderText = HeaderText
        column.Editable = Editable
        column.DataCell = forms.TextBoxCell(self.Columns.Count)
        self.Columns.Add(column)


class PropertySheet(forms.Form):

    def setup(self, sceneNode):
        self.Rnd = System.Random()
        self.Title = "Properties"
        self.TabControl = self.from_sceneNode(sceneNode)
        tab_items = forms.StackLayoutItem(self.TabControl, True)
        layout = forms.StackLayout()
        layout.Spacing = 5
        layout.HorizontalContentAlignment = forms.HorizontalAlignment.Stretch
        layout.Items.Add(tab_items)
        self.Content = layout
        self.Padding = drawing.Padding(12)
        self.Resizable = False
        self.ClientSize = drawing.Size(400, 600)

    def from_sceneNode(self, sceneNode):
        control = forms.TabControl()
        control.TabPosition = forms.DockPosition.Top

        tab = forms.TabPage()
        tab.Text = "Basic"
        tab.Content = Tree_Table.from_sceneNode(sceneNode)
        control.Pages.Add(tab)

        tab = forms.TabPage()
        tab.Text = "Vertices"
        tab.Content = Tree_Table.from_vertices(sceneNode)
        control.Pages.Add(tab)
        self.vertices_table = tab.Content

        tab = forms.TabPage()
        tab.Text = "Edges"
        tab.Content = Tree_Table.from_edges(sceneNode)
        control.Pages.Add(tab)

        tab = forms.TabPage()
        tab.Text = "Faces"
        tab.Content = Tree_Table.from_faces(sceneNode)
        control.Pages.Add(tab)

        return control


if __name__ == "__main__":

    from compas_rhino.utilities import unload_modules
    unload_modules("compas")

    import compas
    from compas_tna.diagrams import FormDiagram
    from compas_rv2.rhino import RhinoFormDiagram

    filepath = compas.get('faces.obj')
    form = FormDiagram.from_obj(filepath)

    diagram = RhinoFormDiagram(form)
    diagram.draw({})
    # form.plot()

    dialog = PropertySheet()
    dialog.setup(diagram)
    dialog.Show()
