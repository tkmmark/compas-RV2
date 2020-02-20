
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

try:
    import Rhino
    import scriptcontext
    import System
    import System.Drawing as sd
    import Rhino.UI
    import Eto.Drawing as drawing
    import Eto.Forms as forms
except Exception:
    compas.raise_if_ironpython()


# Using SampleEtoRoomNumber dialog Example as guide
class BrowserForm(forms.Form):
    def __init__(self, url=None, width=600, height=300):
        self.Title = 'RhinoVault2'
        self.Padding = drawing.Padding(0)
        # self.Resizable = True
        
        # self.DefaultButton = forms.Button(Text = 'OK')
        # self.DefaultButton.Click += self.OnOKButtonClick
        # # self.AbortButton = forms.Button(Text = 'Cancel')

        self.m_webview = forms.WebView()
        self.m_webview.Size = drawing.Size(width, height)

        if not url:
            url = os.path.join(os.path.dirname(os.path.abspath(__file__)),'index.html')
        self.m_webview.Url = System.Uri(url)

        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        layout.BeginVertical()
        layout.AddRow(self.m_webview)
        layout.EndVertical()


        # layout.AddRow(None) # spacer
        # layout.BeginVertical()
        # layout.AddRow(None, self.DefaultButton)
        # layout.EndVertical()

        self.Content = layout

    # def OnCloseButtonClick(self, sender, e):
    #     self.Close(False)

    # def OnOKButtonClick(self, sender, e):
    #     self.Close(True)
    
    # def show(self):
    #     self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


if __name__ == "__main__":
    browser = BrowserForm()
    browser.Show()

