
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import compas

try:
    import System
    import Eto.Drawing as drawing
    import Eto.Forms as forms
except Exception:
    compas.raise_if_ironpython()


class BrowserForm(forms.Form):

    def __init__(self, url=None, width=600, height=300):
        self.Title = 'RhinoVault2'
        self.Padding = drawing.Padding(0)

        self.m_webview = forms.WebView()
        self.m_webview.Size = drawing.Size(width, height)

        if not url:
            url = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'index.html')
        self.m_webview.Url = System.Uri(url)
        self.m_webview.BrowserContextMenuEnabled = True

        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        layout.BeginVertical()
        layout.AddRow(self.m_webview)
        layout.EndVertical()
        self.Content = layout


if __name__ == "__main__":
    browser = BrowserForm()
    browser.Show()
