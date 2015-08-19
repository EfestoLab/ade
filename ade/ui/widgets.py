from PySide import QtCore, QtGui
import re

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

        self.permission = self._data.get('permission')

        for child in self._data.get('children', []):
            self._children.append(AdeItem(data=child, parent=self))

    def addChild(self, data):
        child = AdeItem(data=data, parent=self)
        self._children.append(child)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)


class AdeTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(AdeTreeModel, self).__init__(parent=parent)
        self._parent = parent
        self._root = root
        self._name_map = {}

    def update_mapping(self, key, val):
        self._name_map[key] = val
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def columnCount(self, parent=None):
        return 2

    def rowCount(self, parent=None):
        if parent.isValid():
            item = parent.internalPointer()
        else:
            item = self._root

        return len(item._children)

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

        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 1:
                return
            qApp = QtGui.QApplication.instance()
            style = qApp.style()
            if node.is_folder:
                if self._parent.isExpanded(index):
                    icon = QtGui.QStyle.StandardPixmap.SP_DirOpenIcon
                else:
                    icon = QtGui.QStyle.StandardPixmap.SP_DirClosedIcon
            else:
                icon = QtGui.QStyle.StandardPixmap.SP_FileIcon

            return style.standardIcon(icon)
