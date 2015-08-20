import os
import sys
import stat
from PySide import QtGui, QtCore
from ade.manager.template import TemplateManager
from ade.manager.config import ConfigManager
import widgets


style_white = ''


class AdePrevisWindow(QtGui.QMainWindow):

    def __init__(
            self, build_root=None, config=None, initial_data=None,
            theme='white', parent=None):
        super(AdePrevisWindow, self).__init__(parent=parent)

        self.themes = {
            'white': style_white
        }
        self.theme = theme
        self.icon_theme = 'black' if self.theme == 'white' else 'white'

        self.build_root = build_root

        config_manager = ConfigManager(os.getenv('ADE_CONFIG_PATH'))
        self.config_mode = config or config_manager.get('default')
        self.manager = TemplateManager(self.config_mode)

        self.setupUi()
        if initial_data:
            self.update_fields(initial_data)
        self.setWindowTitle('Ade Template Preview')
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(':/icons/hades')))

    def get_root(self, build_root):
        build_root = build_root or '@+show+@'
        data = self.manager.resolve_template(build_root)
        root = widgets.AdeItem(
            data={
                'name': build_root,
                'folder': True,
                'permissions': str(
                    oct(
                        stat.S_IMODE(
                            os.stat(
                                self.config_mode['template_search_path']
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

        self.mount_layout = QtGui.QHBoxLayout()
        self.mount_label = QtGui.QLabel('Current Mount Point:')
        self.mount_text = QtGui.QLineEdit(
            self.config_mode.get('project_mount_point', 'Undefined'),
        )
        self.mount_text.setEnabled(False)
        self.mount_layout.addWidget(self.mount_label)
        self.mount_layout.addWidget(self.mount_text)
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
            self.get_root(self.build_root),
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
        self.create_button.clicked.connect(self.on_print_to_pdf)
        self.update_fields(self.config_mode.get('defaults', {}))

        self.update_stylesheet()

    def on_print_to_pdf(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName('/home/salva/Desktop/print.pdf')

        painter = QtGui.QPainter()
        painter.begin(printer)
        self.tree_view.render(painter, QtCore.QPoint(0, 0))
        painter.end()

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
        mapping = self.config_mode.get('regexp_mapping', {})

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


def main(build_root=None, config=None, initial_data=None):
    app = QtGui.QApplication('efesto-ade-previs')
    app.setStyle('plastique')
    window = AdePrevisWindow(
        build_root=build_root,
        config=config,
        initial_data=initial_data
    )
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
