from PySide import QtCore, QtGui
import re
import resource

VARIABLE_REGEX = re.compile('@\+(.+)\+@')
CONTAINER_REGEX = re.compile('@(.+)@')


class AdeItem(object):
    def __init__(self, data, parent=None):
        self._data = data
        self._parent = parent
        self._children = []

        self.is_folder = self._data.get('folder')
        self._name = self._data.get('name')
        self.name = self._name
        self.is_variable = False
        self.is_container = False
        variable_result = VARIABLE_REGEX.match(self.name)
        container_result = CONTAINER_REGEX.match(self.name)

        if variable_result:
            self.is_variable = True
        elif container_result:
            self.is_container = True
            self.name = container_result.group(1)

        self.permission = self._data.get('permission')

        for child in self._data.get('children', []):
            self._children.append(AdeItem(data=child, parent=self))

    def children(self):
        return self._children

    def addChild(self, data):
        child = AdeItem(data=data, parent=self)
        self._children.append(child)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)


class AdeTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None, theme='black'):
        super(AdeTreeModel, self).__init__(parent=parent)
        self.omit_empty = False
        self._parent = parent
        self._root = root
        self._name_map = {}
        self.theme = theme
        self.icon_map = {
            'folder': {
                'expanded': ':/{theme}/folder-open-o',
                'normal': ':/{theme}/folder-o'
            },
            'file': {
                'default': ':/{theme}/file-o',
                'pdf': ':/{theme}/file-pdf-o',
                'code': ':/{theme}/file-code-o',
                'image': ':/{theme}/file-image-o',
                'archive': ':/{theme}/file-archive-o',
                'audio': ':/{theme}/file-audio-o',
                'text': ':/{theme}/file-text-o',
            }
        }
        self.file_map = {
            'pdf': ['pdf'],
            'code': ['py', 'mel', 'sh'],
            'image': ['png', 'jpg', 'jpeg', 'bmp', 'gif'],
            'archive': ['zip', 'rar', 'tar', 'gz2'],
            'audio': ['mp3', 'wav'],
            'text': ['txt', 'rst', 'md', 'rtf']
        }

    def update_mapping(self, key, val):
        self._name_map[key] = val
        self.refresh_view()

    def refresh_view(self):
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def columnCount(self, parent=None):
        return 2

    def rowCount(self, parent=None):
        if parent.isValid():
            item = parent.internalPointer()
        else:
            item = self._root

        if self.omit_empty and not item._name == self._root._name:
            if item.is_variable and not self._name_map.get(item._name):
                return 0
        return len(item.children())

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return 'Name'
            else:
                return 'Permissions'

    def index(self, row, column, parent):
        '''Return index for *row* and *column* under *parent*.'''
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            item = self._root
        else:
            item = parent.internalPointer()

        try:
            child = item._children[row]
        except IndexError:
            return QtCore.QModelIndex()
        else:
            return self.createIndex(row, column, child)

    def parent(self, index):
        '''Return parent of *index*.'''
        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self._root:
            return QtCore.QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._root

    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 1:
                return node.permission
            mapped_name = self._name_map.get(node._name)
            if mapped_name:
                return mapped_name
            return node.name

        elif role == QtCore.Qt.ToolTipRole:
            if node.is_container or node.is_variable:
                return node._name

        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 1:
                return
            is_expanded = self._parent.isExpanded(index)
            return QtGui.QIcon(self.get_pixmap(node, is_expanded))

    def get_pixmap(self, node, is_expanded=False, theme=None):
        if node.is_folder:
            icon = self.icon_map['folder']
            if is_expanded and node.children():
                icon = icon['expanded']
            else:
                icon = icon['normal']
            if node.is_container or node.is_variable:
                icon = icon[:-2]
        else:
            icon = self.icon_map['file']
            ext = node.name.split('.')
            if len(ext) == 1:
                icon = icon['default']
            else:
                ext = ext[-1]
                found = False
                for key, val in self.file_map.items():
                    if ext in val:
                        icon = icon[key]
                        found = True
                        break

                if not found:
                    icon = icon['default']

        icon = icon.format(theme=theme or self.theme)
        return QtGui.QPixmap(icon)


class AdeValidator(QtGui.QRegExpValidator):
    def __init__(self, regex, parent=None):
        self.regex = re.compile(regex)
        super(AdeValidator, self).__init__(parent=parent)

    def validate(self, string, pos):
        _invalid = QtGui.QValidator.Invalid
        _valid = QtGui.QValidator.Acceptable

        match = self.regex.match(string)
        if not string:
            state = _valid
        elif match:
            name = match.groupdict().values()[0]
            if not string == name:
                state = _invalid
            else:
                state = _valid
        else:
            state = _invalid

        is_valid = False if state == _invalid else True
        self.parent().setProperty('valid', is_valid)
        return _valid, string, pos


class NotificationArea(QtGui.QFrame):
    def __init__(self, parent=None):
        super(NotificationArea, self).__init__(parent=parent)
        self.main_layout = QtGui.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.notification_frame = QtGui.QFrame(self)
        self.notification_frame.setObjectName('notification-area')

        self.notification_frame_layout = QtGui.QHBoxLayout()
        self.notification_frame.setLayout(self.notification_frame_layout)
        self.main_layout.addWidget(self.notification_frame)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.text_area = QtGui.QLabel('Welcome', self.notification_frame)
        self.close_button = QtGui.QPushButton('x')
        self.close_button.setMaximumSize(20, 20)

        self.notification_frame_layout.addWidget(self.text_area)
        self.notification_frame_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.dismiss)
        self.dismiss()

    def display_message(self, message, level='info'):
        self.notification_frame.show()
        self.text_area.setText(message)
        self.notification_frame.setProperty('level', level)

    def dismiss(self):
        self.notification_frame.hide()
