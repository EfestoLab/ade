import os
import sys
import stat
from PySide import QtGui
from ade.manager.template import TemplateManager
from ade.manager.config import ConfigManager
import widgets
import time


style_white = ''
TXT_HEADER = '''
# @Copyright(c) 2015 EfestoLab
# Created using Efesto Ade Preview tools on {date}
# Settings:
#   * Template path: {template_search_path}
#   * Root template: {root_template}
#   * Data:
{data}
'''


class AdePrevisWindow(QtGui.QMainWindow):

    def __init__(
            self, build_root=None, theme='white', initial_data=None,
            parent=None, config_path=None, config_mode=None):
        super(AdePrevisWindow, self).__init__(parent=parent)

        self.themes = {
            'white': style_white
        }
        self.theme = theme
        self.icon_theme = 'black' if self.theme == 'white' else 'white'

        self.build_root = build_root or '@+show+@'

        self.config_path = config_path or os.getenv('ADE_CONFIG_PATH')
        self.config_mode = config_mode or 'default'
        config_manager = ConfigManager(self.config_path)
        self.config_dict = config_manager.get(self.config_mode)
        self.manager = TemplateManager(self.config_dict)

        self.setupUi()
        if initial_data:
            self.update_fields(initial_data)
        self.setWindowTitle('Ade Template Preview')
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/icons/hades')))

    def get_root(self):
        data = self.manager.resolve_template(self.build_root)
        root = widgets.AdeItem(
            data={
                'name': self.build_root,
                'folder': True,
                'permissions': str(
                    oct(
                        stat.S_IMODE(
                            os.stat(
                                self.config_dict['template_search_path']
                            ).st_mode
                        )
                    )
                ),
                'children': [data]
            },
        )
        return root

    def setupUi(self):
        self.resize(900, 500)

        self.central_widget = QtGui.QFrame(self)
        self.central_layout = QtGui.QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # Menu
        self.menu_bar = QtGui.QMenuBar(self.central_widget)
        self.file_menu = QtGui.QMenu('&File')
        self.export_txt = QtGui.QAction('Export as &TXT', self.file_menu)
        self.export_txt.triggered.connect(lambda: self.on_export('txt'))
        self.export_pdf = QtGui.QAction('Export as &PDF', self.file_menu)
        self.export_pdf.triggered.connect(lambda: self.on_export('pdf'))
        self.file_menu.addAction(self.export_txt)
        self.file_menu.addAction(self.export_pdf)

        self.menu_bar.addMenu(self.file_menu)
        self.setMenuBar(self.menu_bar)

        # Mount Point
        self.mount_layout = QtGui.QHBoxLayout()
        self.mount_label = QtGui.QLabel('Current Mount Point:')
        self.mount_text = QtGui.QLineEdit(
            self.config_dict.get('project_mount_point', 'Undefined'),
        )
        self.mount_text.setEnabled(False)

        self.config_label = QtGui.QLabel('Current Config:')
        self.config_text = QtGui.QLineEdit(
            os.path.join(self.config_path, self.config_mode+'.json'),
        )
        self.config_text.setEnabled(False)
        self.mount_layout.addWidget(self.mount_label)
        self.mount_layout.addWidget(self.mount_text)
        self.mount_layout.addWidget(self.config_label)
        self.mount_layout.addWidget(self.config_text)
        self.central_layout.addLayout(self.mount_layout)

        self.main_layout = QtGui.QHBoxLayout()
        # Names
        self.format_container = QtGui.QFrame(self.central_widget)
        self.format_layout = QtGui.QVBoxLayout()
        self.format_container.setLayout(self.format_layout)

        self.format_box = QtGui.QGroupBox('Format Variables:')
        self.format_box_layout = QtGui.QVBoxLayout()
        self.format_box.setLayout(self.format_box_layout)
        self.format_layout.addWidget(self.format_box)

        self.format_list = QtGui.QFrame(self.format_container)
        self.format_list_layout = QtGui.QGridLayout()
        self.format_list.setLayout(self.format_list_layout)

        self.format_box_layout.addWidget(self.format_list)
        self.format_box_layout.addItem(
            QtGui.QSpacerItem(1, 1, vData=QtGui.QSizePolicy.Expanding)
        )

        # Tree
        self.tree_container = QtGui.QFrame(self.central_widget)
        self.tree_layout = QtGui.QVBoxLayout()
        self.tree_container.setLayout(self.tree_layout)

        self.tree_view = QtGui.QTreeView(self.tree_container)
        self.tree_layout.addWidget(self.tree_view)

        self.tree_model = widgets.AdeTreeModel(
            self.get_root(),
            parent=self.tree_view,
            theme=self.icon_theme
        )
        self.tree_view.setModel(self.tree_model)

        self.tree_view.resizeColumnToContents(1)
        self.tree_view.resizeColumnToContents(0)
        self.tree_view.setColumnWidth(0, self.tree_view.columnWidth(0)*2)

        # Add both widgets
        self.main_layout.addWidget(self.tree_container)
        self.main_layout.addWidget(self.format_container)
        self.central_layout.addLayout(self.main_layout)

        # Fill variables
        for i in self.manager._register:
            name = i['name']
            if name.startswith('@+'):
                self.create_format_widget(name)

        self.create_button = QtGui.QPushButton('Create Folder Structure')
        self.central_layout.addWidget(self.create_button)
        # self.create_button.clicked.connect(self.on_print_to_pdf)
        self.update_fields(self.config_dict.get('defaults', {}))

        self.update_stylesheet()

    def on_export(self, file_type):
        destination = QtGui.QFileDialog.getSaveFileName(
            self,
            'Select Destination',
            os.path.expanduser('~'),
            'Tree File (*.%s)' % file_type
        )
        destination = destination[0]
        if not destination.endswith(file_type):
            destination += '.%s' % file_type

        items = self.extract_tree_data(self.tree_model._root)
        items.pop(0)

        if file_type == 'txt':
            data = self.data_to_txt(items)
            with file(destination, 'w') as f:
                f.write(data)

    def extract_tree_data(self, item, indent=0):
        items = [
            {
                'name': self.tree_model._name_map.get(item._name) or item.name,
                'indent': indent,
                'folder': item.is_folder,
                'icon': self.tree_model.get_icon(item, True)
            }
        ]

        for child in item._children:
            items += self.extract_tree_data(child, indent+1)

        return items

    def get_txt_header(self):
        header = TXT_HEADER
        data = {}
        for key, val in self.tree_model._name_map.items():
            if val:
                data[key] = val

        formated_data = []
        for key, val in data.items():
            formated_data.append('#          - %s: %s' % (key, val))

        header = header.format(
            date=time.strftime("%c"),
            template_search_path=self.config_dict.get(
                'template_search_path', 'Unknown'
            ),
            root_template=self.build_root,
            data='\n'.join(formated_data)
        )
        return header

    def data_to_txt(self, data):
        txt_file = [self.get_txt_header()]
        for item in data:
            line = '    ' * (item['indent'] - 1)
            line += '+ ' if item['folder'] else '* '
            line += item['name']
            txt_file.append(line)

        return '\n'.join(txt_file)

    def data_to_pdf(self, data):
        pass

    def update_stylesheet(self):
        self.setStyleSheet(self.themes[self.theme])

    def create_format_widget(self, key):
        label = QtGui.QLabel(key)
        text = QtGui.QLineEdit()

        index = self.format_list_layout.count() / 2

        self.format_list_layout.addWidget(label, index, 0)
        self.format_list_layout.addWidget(text, index, 1)

        text.textChanged.connect(self.on_name_changed)
        text.textChanged.connect(self.update_stylesheet)
        mapping = self.config_dict.get('regexp_mapping', {})

        text.setProperty('valid', True)
        for variable, regex in mapping.items():
            if variable in key:
                regex_val = widgets.AdeValidator(regex, parent=text)
                text.setValidator(regex_val)

    def on_name_changed(self, name):
        index = self.format_list_layout.indexOf(self.sender())
        label = self.format_list_layout.itemAt(index-1).widget()
        text = self.sender()
        key = label.text()
        if name.strip() and text.property('valid'):
            self.tree_model.update_mapping(key, name)
        else:
            self.tree_model.update_mapping(key, None)

    def update_fields(self, data):
        for key, val in data.items():
            for i in range(self.format_list_layout.count() / 2):
                label = self.format_list_layout.itemAtPosition(i, 0).widget()
                text = self.format_list_layout.itemAtPosition(i, 1).widget()
                if label.text() == '@+%s+@' % key:
                    text.setText(os.path.expandvars(val))


def main(
        build_root=None, config_path=None, config_mode=None,
        initial_data=None):
    app = QtGui.QApplication('efesto-ade-previs')
    app.setStyle('plastique')
    window = AdePrevisWindow(
        build_root=build_root,
        config_path=config_path,
        config_mode=config_mode,
        initial_data=initial_data
    )
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
