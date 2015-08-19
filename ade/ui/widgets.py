from PySide import QtCore, QtGui


class AdeItem(object):
    def __init__(self, data, parent=None, signal=None):
        self._data = data
        self._parent = parent
        self._children = []
        self._signal = signal

        self.is_folder = self._data.get('folder')
        self._name = self._data.get('name')
        self.name = self._name
        self.permissions = self._data.get('permissions')

        for child in self._data.get('children', []):
            self._children.append(
                AdeItem(
                    data=child,
                    parent=self,
                    signal=signal
                    )
                )

        if signal:
            signal.connect(self.on_name_change)

    def on_name_change(self, data):
        if data.keys()[0] == self._name:
            self.name = data.values()[0]

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

    def columnCount(self, parent=None):
        return 1

    def rowCount(self, parent=None):
        if parent.isValid():
            item = parent.internalPointer()
        else:
            item = self._root

        return len(item._children)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return 'Name'

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
            return node.name

        elif role == QtCore.Qt.DecorationRole:
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
