import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *

from DictionaryUtils import DictionaryUtils

class MyForm(Form):
    def __init__(self):
        # Create child controls and initialize form
        self.Text = 'Prefix Search'

        self._dictUtils = DictionaryUtils()
        self._dictUtils.parse_from_dict_file('dict.txt')

        self._textBox = TextBox()
        self._textBox.Dock = DockStyle.Top
        self.Controls.Add(self._textBox)

        self._listView = ListView()
        self._listView.View = View.List
        self._listView.Location = Point(self._listView.Location.X, 
                                           self._textBox.Location.Y + self._textBox.Size.Height)
        self._listView.Size = Size(self._textBox.Size.Width, 
                                   self.Size.Height - self._textBox.Size.Height)
        self.Controls.Add(self._listView)

        self._textBox.TextChanged += self.handle_text_changed
        self.FormBorderStyle = FormBorderStyle.FixedToolWindow

    def handle_text_changed(self, sender, args):
        prefix = sender.Text
        self._listView.Items.Clear()
        if len(prefix) > 1:
            for word in self._dictUtils.find_all_by_prefix(prefix):
                self._listView.Items.Add(ListViewItem(word))


def create_dictionary():
    dictUtils = DictionaryUtils()
    dictUtils.parse_from_dir_list(['D:\\games',
                                   'D:\\install',
                                   'D:\\work\\reading'])
    dictUtils.save_dict_to_file('dict.txt')

def run_app():
    Application.EnableVisualStyles()
    Application.SetCompatibleTextRenderingDefault(False)
    
    form = MyForm()
    Application.Run(form)

#create_dictionary()
run_app()
