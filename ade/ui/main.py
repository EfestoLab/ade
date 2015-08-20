import os
import sys
import stat
from PySide import QtGui, QtCore
from ade.manager.template import TemplateManager
from ade.manager.config import ConfigManager
from ade.manager import filesystem
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
        self.export_txt.setIcon(
            QtGui.QIcon(QtGui.QPixmap(':/%s/file-text-o' % self.icon_theme))
        )
        self.export_txt.triggered.connect(lambda: self.on_export('txt'))
        self.export_pdf = QtGui.QAction('Export as &PDF', self.file_menu)
        self.export_pdf.setIcon(
            QtGui.QIcon(QtGui.QPixmap(':/%s/file-pdf-o' % self.icon_theme))
        )
        self.export_pdf.triggered.connect(lambda: self.on_export('pdf'))
        self.file_menu.addAction(self.export_txt)
        self.file_menu.addAction(self.export_pdf)

        self.menu_bar.addMenu(self.file_menu)
        self.setMenuBar(self.menu_bar)

        # Notification area
        self.notification_area = widgets.NotificationArea(self.central_widget)
        self.central_layout.addWidget(self.notification_area)

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

        self.tree_omit_empty = QtGui.QCheckBox('Omit Empty')
        self.tree_omit_empty.stateChanged.connect(self.on_omit_empty)
        self.tree_expand_all = QtGui.QPushButton('Expand All')
        self.tree_expand_all.clicked.connect(self.tree_view.expandAll)
        self.tree_collapse_all = QtGui.QPushButton('Collapse All')
        self.tree_collapse_all.clicked.connect(self.tree_view.collapseAll)
        self.tree_utils = QtGui.QHBoxLayout()

        self.tree_utils.addWidget(self.tree_omit_empty)
        self.tree_utils.addWidget(self.tree_expand_all)
        self.tree_utils.addWidget(self.tree_collapse_all)
        self.tree_layout.addLayout(self.tree_utils)
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
        self.create_button.clicked.connect(self.create_folder_structure)
        self.update_fields(self.config_dict.get('defaults', {}))

        self.update_stylesheet()

    def report_message(self, message, level):
        self.notification_area.display_message(message, level)
        self.update_stylesheet()

    def on_omit_empty(self, state):
        self.tree_model.omit_empty = bool(state)
        self.tree_view.collapseAll()

    def on_export(self, file_type):
        destination = QtGui.QFileDialog.getSaveFileName(
            self,
            'Select Destination',
            os.path.expanduser('~'),
            'Tree File (*.%s)' % file_type
        )
        if not any(destination):
            return

        destination = destination[0]
        if not destination.endswith(file_type):
            destination += '.%s' % file_type

        items = self.extract_tree_data(self.tree_model._root)
        items.pop(0)

        if file_type == 'txt':
            data = self.data_to_txt(items)
            with file(destination, 'w') as f:
                f.write(data)
        else:
            self.data_to_pdf(items, destination)

    def extract_tree_data(self, item, indent=0):
        if self.tree_omit_empty.checkState():
            if not item._name == self.tree_model._root._name:
                alias = self.tree_model._name_map.get(item._name)
                if item.is_variable and not alias:
                    return []
        items = [
            {
                'name': self.tree_model._name_map.get(item._name) or item.name,
                'variable': item._name,
                'indent': indent,
                'folder': item.is_folder,
                'pixmap': self.tree_model.get_pixmap(item, True, 'black')
            }
        ]

        for child in item._children:
            items += self.extract_tree_data(child, indent+1)

        return items

    def get_treemodel_data(self, strip_variable=False):
        data = {}
        for key, val in self.tree_model._name_map.items():
            if val:
                if strip_variable:
                    key = key[2:-2]
                data[key] = val

        return data

    def get_txt_header(self):
        header = TXT_HEADER

        data = self.get_treemodel_data()
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
            if item['name'] == item['variable']:
                line += item['name']
            else:
                line += item['name'] + ' (%s)' % item['variable']
            txt_file.append(line)

        return '\n'.join(txt_file)

    def data_to_pdf(self, data, file_path):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setPageSize(QtGui.QPrinter.Letter)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(file_path)
        painter = QtGui.QPainter()
        painter.begin(printer)
        painter.setRenderHints(
            QtGui.QPainter.Antialiasing |
            QtGui.QPainter.TextAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform
        )

        efesto_logo = QtGui.QPixmap(':/icons/efesto')
        efesto_pos = [100, 100]
        painter.drawPixmap(
            QtCore.QPoint(*efesto_pos),
            efesto_logo.scaled(
                1500,
                1500,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
        )
        header = self.get_txt_header()
        header_items = [x for x in header.split('\n') if x]
        i = 0
        for header_item in header_items:
            header_item = header_item.strip('#')
            header_pos = [1800, 300*i + 300]
            if 'Template' in header_item:
                while len(header_item) > 85:
                    header_item_prev = header_item[:85]
                    header_item = '\t' + header_item[85:]
                    painter.drawText(QtCore.QPoint(
                        *header_pos),
                        header_item_prev
                    )
                    i += 1
                    header_pos = [1800, 300*i + 300]
            painter.drawText(QtCore.QPoint(*header_pos), header_item)
            i += 1

        i = 9
        if len(header_items) > 6:
            i += len(header_items) - 6
        for item in data:
            if i % 43 == 0 and not i == 0:
                printer.newPage()
                i = 0
            pos = [item['indent']*400, i*300]
            pixmap = item['pixmap']
            scale = 200
            pixmap_pos = [pos[0]-scale, pos[1]-(scale * 0.7)]
            painter.drawPixmap(
                QtCore.QPoint(*pixmap_pos), pixmap.scaled(scale, scale))
            pos[0] += 100
            if item['name'] == item['variable']:
                label = item['name']
            else:
                label = item['name'] + ' (%s)' % item['variable']
            painter.drawText(QtCore.QPoint(*pos), label)
            i += 1
        painter.end()

    def update_stylesheet(self):
        fileObject = QtCore.QFile(':/style/%s' % self.theme)
        fileObject.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        stream = QtCore.QTextStream(fileObject)
        styleSheetContent = stream.readAll()
        self.setStyleSheet(styleSheetContent)

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

    def create_folder_structure(self):
        mount_point = self.config_dict.get('project_mount_point')
        try:
            manager = filesystem.FileSystemManager(
                self.config_dict,
                self.manager
            )
            manager.build(
                self.build_root,
                self.get_treemodel_data(True),
                mount_point
            )
            self.report_message(
                'Folders created in %s' % mount_point,
                'success'
            )
        except Exception as e:
            self.report_message('An error ocurred: %s' % e, 'error')
            import traceback
            print traceback.format_exc()


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
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
