from PySide import QtGui
import sys
import widgets
import os
import stat
from ade.manager.template import TemplateManager
from ade.manager.config import ConfigManager


class AdePrevisWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(AdePrevisWindow, self).__init__(parent=parent)

        config_manager = ConfigManager(os.getenv('ADE_CONFIG_PATH'))
        self.config_mode = config_manager.get('default')
        self.manager = TemplateManager(self.config_mode)

        self.setupUi()
        self.setWindowTitle('Ade Template Preview')

    def get_root(self, build_root='@+show+@'):
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
                                ).st_mode)
                        )
                    ),
                'children': [data]
            }
        )
        return root

    def setupUi(self):
        self.central_widget = QtGui.QFrame(self)
        self.central_layout = QtGui.QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        self.tree_container = QtGui.QFrame(self.central_widget)
        self.tree_layout = QtGui.QVBoxLayout()
        self.tree_container.setLayout(self.tree_layout)

        self.central_layout.addWidget(self.tree_container)

        self.tree_view = QtGui.QTreeView(self.tree_container)
        self.tree_layout.addWidget(self.tree_view)

        self.tree_model = widgets.AdeTreeModel(
            self.get_root(),
            parent=self.tree_view
        )
        self.tree_view.setModel(self.tree_model)


def main():
    app = QtGui.QApplication('efesto-ade-previs')
    app.setStyle('plastique')
    window = AdePrevisWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
