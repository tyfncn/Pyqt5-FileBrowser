import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, init_dir):
        super().__init__()
        print(os.getcwd(),resource_path("FileBrowser.ui"))
        self.init_dir = init_dir
        uic.loadUi(resource_path("FileBrowser.ui"), self)
        #  vscode autocomplete için gerekiyor ama runtime'da gerek yok
        self.treeView = self.findChild(QtWidgets.QTreeView, "treeView")
        self.lineEdit = self.findChild(QtWidgets.QLineEdit,"lineEdit")

        self.treeView.expanded.connect(self.populateItem)

        self.model = QtGui.QStandardItemModel(0,1)
        self.model.setHorizontalHeaderLabels(["Adı"])
        root_item = QtGui.QStandardItem(self.init_dir)
        root_item.full_path = self.init_dir
        root_item.appendRow(QtGui.QStandardItem("Yükleniyor"))
        self.model.appendRow(root_item)

        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.filter_proxy_model.setRecursiveFilteringEnabled(True)

        self.lineEdit.textChanged.connect(self.filter_proxy_model.setFilterWildcard)
        self.treeView.setModel(self.filter_proxy_model)
    


        
    
    def populateItem(self, b=None, c=None):
        real_parent = self.filter_proxy_model.mapToSource(b)
        parent = self.model.itemFromIndex(real_parent)
        print("Parent fullpath:",parent.full_path)
        if not parent.hasChildren(): 
            return
        if parent.child(0,0).text() == "Yükleniyor":
            parent.removeRows(0, 1)
            for x in os.listdir(parent.full_path):
                new_item = QtGui.QStandardItem(x)
                new_item.full_path = os.path.join(parent.full_path, x)
                if os.path.isdir(new_item.full_path):
                    new_item.appendRow(QtGui.QStandardItem("Yükleniyor"))
                parent.appendRow(new_item)
        






if __name__ == "__main__":
    init_dir = "/"
    if sys.platform == "nt":
        init_dir = "C:/"

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow(init_dir)
    window.show()
    app.exec_()