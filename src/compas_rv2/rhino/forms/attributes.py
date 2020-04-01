from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import compas
import ast
from compas_rv2.rhino import get_scene
from compas_rv2.rhino.forms.settings import Settings_Tab

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc
    find_object = sc.doc.Objects.Find
    import Eto.Drawing as drawing
    import Eto.Forms as forms
except Exception:
    compas.raise_if_ironpython()


__all__ = ["AttributesForm"]


class Tree_Table(forms.TreeGridView):
    def __init__(self, ShowHeader=True, sceneNode=None, table_type=None):
        self.ShowHeader = ShowHeader
        self.Height = 300
        self.last_sorted_to = None
        # self.AllowMultipleSelection=True

        # give colors to each item cells according to object settings
        color = {}
        if sceneNode and table_type:
            settings = sceneNode.settings

            # update general color settings for this table
            general_setting_key = "color.%s" % table_type
            color.update({str(key): settings.get(general_setting_key) for key in sceneNode.datastructure.vertices()})

            # gather and update subsettings
            for full_setting_key in settings:
                sub_setting_str = full_setting_key.split(":")
                if len(sub_setting_str) > 1 and sub_setting_str[0] == general_setting_key:
                    sub_setting_key = sub_setting_str[-1]
                    items_where = getattr(sceneNode.datastructure, '%s_where' % table_type)
                    color.update({str(key): settings.get(full_setting_key) for key in items_where({sub_setting_key: True})})
                    color.update({str(key): settings.get(full_setting_key) for key in items_where({'_'+sub_setting_key: True})})  # including read-only ones

        def OnCellFormatting(sender, e):
            try:
                if not e.Column.Editable:
                    e.ForegroundColor = drawing.Colors.DarkGray

                attr = e.Column.HeaderText
                if attr == 'key':
                    key = e.Item.Values[0]
                    if key in color:
                        rgb = color[key]
                        rgb = [c/255. for c in rgb]
                        e.BackgroundColor = drawing.Color(*rgb)

            except Exception as exc:
                print('formating error', exc)

        self.CellFormatting += OnCellFormatting

    @classmethod
    def create_settings_table(cls, sceneNode):
        table = cls(ShowHeader=False)
        table.add_column()
        table.add_column(Editable=True)

        treecollection = forms.TreeGridItemCollection()
        # treecollection.Add(forms.TreeGridItem(Values=('Type', sceneNode.datastructure.__class__.__name__)))
        # treecollection.Add(forms.TreeGridItem(Values=('Name', sceneNode.name)))
        # treecollection.Add(forms.TreeGridItem(Values=('Layer', sceneNode.artist.layer)))
        if hasattr(sceneNode, 'settings'):
            for key in sceneNode.artist.settings:
                treecollection.Add(forms.TreeGridItem(Values=(key, str(sceneNode.artist.settings[key]))))

        table.DataStore = treecollection
        return table

    @classmethod
    def create_vertices_table(cls, sceneNode):
        datastructure = sceneNode.datastructure
        table = cls(sceneNode=sceneNode, table_type='vertices')
        table.add_column('key')
        attributes = list(datastructure.default_vertex_attributes.keys())
        attributes.sort()
        for attr in attributes:
            editable = attr[0] != '_'
            checkbox = type(datastructure.default_vertex_attributes[attr]) == bool
            if not editable:
                attr = attr[1:]
            table.add_column(attr, Editable=editable, checkbox=checkbox)
        treecollection = forms.TreeGridItemCollection()
        for key in datastructure.vertices():
            values = [str(key)]
            for attr in attributes:
                values.append(str(datastructure.vertex_attribute(key, attr)))
            treecollection.Add(forms.TreeGridItem(Values=tuple(values)))
        table.DataStore = treecollection
        table.Activated += table.SelectEvent(sceneNode, 'guid_vertex')
        # table.CellEdited += table.EditEvent(rhinoDiagram, attributes)
        table.ColumnHeaderClick += table.HeaderClickEvent()
        return table

    @classmethod
    def create_edges_table(cls, sceneNode):
        datastructure = sceneNode.datastructure
        table = cls(sceneNode=sceneNode, table_type='edges')
        table.add_column('key')
        attributes = list(datastructure.default_edge_attributes.keys())
        attributes.sort()

        for attr in attributes:
            editable = attr[0] != '_'
            checkbox = type(datastructure.default_edge_attributes[attr]) == bool
            if not editable:
                attr = attr[1:]
            table.add_column(attr, Editable=editable, checkbox=checkbox)

        treecollection = forms.TreeGridItemCollection()
        for key, edge in enumerate(datastructure.edges()):
            values = [str(edge)]
            for attr in attributes:
                values.append(datastructure.edge_attribute(edge, attr))
            edge_item = forms.TreeGridItem(Values=tuple(values))
            treecollection.Add(edge_item)
            for key in edge:
                vertex_item = forms.TreeGridItem(Values=(str(key),))
                edge_item.Children.Add(vertex_item)
        table.DataStore = treecollection
        table.Activated += table.SelectEvent(sceneNode, 'guid_edge', 'guid_vertex')
        table.ColumnHeaderClick += table.HeaderClickEvent()
        return table

    @classmethod
    def create_faces_table(cls, sceneNode):
        datastructure = sceneNode.datastructure
        table = cls(sceneNode=sceneNode, table_type='faces')
        table.add_column('key')
        table.add_column('vertices')
        attributes = list(datastructure.default_face_attributes.keys())
        attributes.sort()
        for attr in attributes:
            editable = attr[0] != '_'
            checkbox = type(datastructure.default_face_attributes[attr]) == bool
            if not editable:
                attr = attr[1:]
            table.add_column(attr, Editable=editable, checkbox=checkbox)

        treecollection = forms.TreeGridItemCollection()
        for key in datastructure.faces():
            values = [str(key), str(datastructure.face[key])]
            for attr in attributes:
                values.append(datastructure.face_attribute(key, attr))
            face_item = forms.TreeGridItem(Values=tuple(values))
            treecollection.Add(face_item)
            for v in datastructure.face[key]:
                vertex_item = forms.TreeGridItem(Values=('', str(v)))
                face_item.Children.Add(vertex_item)
        table.DataStore = treecollection
        table.Activated += table.SelectEvent(sceneNode, 'guid_face', 'guid_vertex')
        table.ColumnHeaderClick += table.HeaderClickEvent()
        return table

    def SelectEvent(self, sceneNode, guid_field, children_guid_field=None):
        def on_selected(sender, event):
            try:
                rs.UnselectAllObjects()
                key = event.Item.Values[0]
                guid2key = getattr(sceneNode, guid_field)
                key2guid = {str(guid2key[guid]): guid for guid in guid2key}
                if key in key2guid:
                    find_object(key2guid[key]).Select(True)
                elif children_guid_field:
                    if key == '':
                        key = event.Item.Values[1]
                    guid2key = getattr(sceneNode, children_guid_field)
                    key2guid = {str(guid2key[guid]): guid for guid in guid2key}
                    find_object(key2guid[key]).Select(True)
                print('selected', key, key2guid[key])
                rs.Redraw()
            except Exception as e:
                print(e)

        return on_selected

    def EditEvent(self, rhinoDiagram, attributes):
        # TODO: need to add situations for edge and face
        def on_edited(sender, event):
            try:
                raise NotImplementedError("Editing not implemented yet")
                # key = event.Item.Values[0]
                # attr = attributes[event.Column-1]
                # value = event.Item.Values[event.Column]
                # if value != '-':
                #     try:
                #         parsed = ast.literal_eval(value)
                #     except Exception:
                #         parsed = str(value)
                #     compas_value = rhinoDiagram.diagram.vertex_attribute(key, attr)
                #     if type(compas_value) == float and type(parsed) == int:
                #         parsed = float(parsed)
                #     if parsed != compas_value:
                #         if type(parsed) == rhinoDiagram.vertex_attributes_properties[attr]['type']:
                #             rhinoDiagram.diagram.vertex_attribute(key, attr, parsed)
                #             print('updated', parsed)
                #             get_scene().update()
                #         else:
                #             print('invalid value type!')
                #             event.Item.Values[event.Column] = compas_value
                #     else:
                #         print('value not changed from', value)

            except Exception as e:
                print(e)
        return on_edited

    def HeaderClickEvent(self):
        def on_hearderClick(sender, event):
            try:
                # print(event.Column.HeaderText)
                sender.sort(event.Column.HeaderText)
            except Exception as e:
                print(e)
        return on_hearderClick

    def add_column(self, HeaderText=None, Editable=False, checkbox=False):
        column = forms.GridColumn()
        if self.ShowHeader:
            column.HeaderText = HeaderText
        column.Editable = Editable
        if not checkbox:
            column.DataCell = forms.TextBoxCell(self.Columns.Count)
        else:
            column.DataCell = forms.CheckBoxCell(self.Columns.Count)
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


class AttributesForm(forms.Form):

    @classmethod
    def from_sceneNode(cls, sceneNode):
        attributesForm = cls()
        attributesForm.setup(sceneNode)
        attributesForm.Show()
        return attributesForm

    def setup(self, sceneNode):
        self.Title = "Property - " + sceneNode.name
        self.sceneNode = sceneNode

        control = forms.TabControl()
        control.TabPosition = forms.DockPosition.Top

        tab = Settings_Tab.from_settings("Settings", sceneNode.settings)
        control.Pages.Add(tab)

        tab = forms.TabPage()
        tab.Text = "Vertices"
        tab.Content = Tree_Table.create_vertices_table(sceneNode)
        control.Pages.Add(tab)
        self.vertices_table = tab.Content

        tab = forms.TabPage()
        tab.Text = "Edges"
        tab.Content = Tree_Table.create_edges_table(sceneNode)
        control.Pages.Add(tab)
        self.edges_table = tab.Content

        if hasattr(sceneNode, 'guid_face'):
            if len(sceneNode.guid_face.keys()) > 0:
                tab = forms.TabPage()
                tab.Text = "Faces"
                tab.Content = Tree_Table.create_faces_table(sceneNode)
                control.Pages.Add(tab)
                self.faces_table = tab.Content

        self.TabControl = control

        tab_items = forms.StackLayoutItem(self.TabControl, True)
        layout = forms.StackLayout()
        layout.Spacing = 5
        layout.HorizontalContentAlignment = forms.HorizontalAlignment.Stretch
        layout.Items.Add(tab_items)

        sub_layout = forms.DynamicLayout()
        sub_layout.Spacing = drawing.Size(5, 0)
        sub_layout.AddRow(None, self.ok, self.cancel, self.apply)
        layout.Items.Add(forms.StackLayoutItem(sub_layout))

        self.Content = layout
        self.Padding = drawing.Padding(12)
        self.Resizable = True
        self.ClientSize = drawing.Size(400, 600)

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

    @property
    def apply(self):
        self.ApplyButton = forms.Button(Text='Apply')
        self.ApplyButton.Click += self.on_apply
        return self.ApplyButton

    def on_ok(self, sender, event):
        try:
            for page in self.TabControl.Pages:
                if hasattr(page, 'apply'):
                    page.apply()
            get_scene().update()
        except Exception as e:
            print(e)
        self.Close()

    def on_apply(self, sender, event):
        try:
            for page in self.TabControl.Pages:
                if hasattr(page, 'apply'):
                    page.apply()
            get_scene().update()
        except Exception as e:
            print(e)

    def on_cancel(self, sender, event):
        self.Close()

if __name__ == "__main__":

    # from compas_rhino.utilities import unload_modules
    # unload_modules("compas")

    from compas_rv2.datastructures import FormDiagram
    from compas_rv2.datastructures import Pattern

    # pattern = Pattern.from_obj(compas.get('faces.obj'))
    # form = FormDiagram.from_pattern(pattern)
    scene = get_scene()

    # scene.clear()
    # node = scene.add(form, name='form', settings=scene.settings)
    # scene.update()

    # print(node.datastructure.default_vertex_attributes)
    # print(node.datastructure.default_edge_attributes)
    # print(node.datastructure.default_face_attributes)


    node = scene.get("form")[0]
    AttributesForm.from_sceneNode(node)
