import os
from kabaret.app import resources
from kabaret.app.ui.gui.widgets.widget_view import DockedView, QtWidgets, QtGui, QtCore


class SubprocessOutput(QtWidgets.QPlainTextEdit):
    
    def __init__(self, parent, view):
        super(SubprocessOutput, self).__init__(parent)
        self.view = view
        self._log_mtime = 0
        
        self.setReadOnly(True)
        
        # Set up timer to periodically update
        # running process output
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.setInterval(10)
    
    def _write(self, text):
        doc = self.document()
        cursor = QtGui.QTextCursor(doc)
        cursor.clearSelection()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ensureCursorVisible()
    
    def update(self):
        log_path = self.view.current_log_path()
        if log_path is None:
            return
        
        self.clear()
        
        with open(log_path, 'r') as log_file:
            log = log_file.read()
            self._write(log)
    
    def refresh(self):
        log_path = self.view.current_log_path()
        if log_path is None:
            return

        # Check if log file has been modified
        mtime = os.path.getmtime(log_path)
        
        if mtime > self._log_mtime:
            self.update()
            self._log_mtime = mtime


class SubprocessListItem(QtWidgets.QTreeWidgetItem):
    
    def __init__(self, tree, process):
        super(SubprocessListItem, self).__init__(tree)
        self.process = None
        # self.args = ()
        # self.kwargs = {}
        self._match_str = ''
        self.set_process(process)
    
    def set_process(self, process):
        self.process = process
        self._match_str = ''
        self._update()
    
    def _update(self):
        self.setText(0, str(self.index()))
        self.setText(1, str(self.pid()))
        self.setText(2, self.name())
        # self.setText(3, self.version())
        self.setText(3, self.is_running() and 'Running...' or 'Finished')
    
    def name(self):
        return self.process['name']
    
    def version(self):
        return self.process['version']
    
    def index(self):
        return self.process['index']
    
    def pid(self):
        return self.process['pid']
    
    def is_running(self):
        return self.process['is_running']
    
    def log_path(self):
        return self.process['log_path']
    
    def matches(self, filter):
        return filter in self._match_str


class SubprocessList(QtWidgets.QTreeWidget):
    
    def __init__(self, parent, view, session):
        super(SubprocessList, self).__init__(parent)
        self.view = view
        self.session = session
        
        columns = (
            'Index', 'PID',
            'Name',# 'Version',
            'Status',
        )
        self.setHeaderLabels(columns)
        
        self.itemSelectionChanged.connect(self.view.update_output)

        self._filter = None
    
    def refresh(self):
        #TODO: intelligent refresh: remove deleted runners, add created runners
        self.clear()
        for sp in self.session.cmds.SubprocessManager.list_runner_infos():
            item = SubprocessListItem(self, sp)
            # TODO: manage item filtering
            # if self._filter and not item.matches(self._filter):
            #     item.setHidden(True)
        self.sortItems(0, QtCore.Qt.DescendingOrder)


class SubprocessView(DockedView):
    
    def __init__(self, session, view_id=None, hidden=False, area=None):
        super(SubprocessView, self).__init__(session, view_id, hidden=hidden, area=area)

    def _build(self, top_parent, top_layout, main_parent, header_parent, header_layout):
        self.splitter = QtWidgets.QSplitter(main_parent)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        
        self._subprocess_list = SubprocessList(self.splitter, self, self.session)
        self._subprocess_output = SubprocessOutput(self.splitter, self)
        
        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        lo.addWidget(self.splitter)

        main_parent.setLayout(lo)
        
        self.view_menu.setTitle('Options')
        self.view_menu.addAction('Refresh', self.refresh_list)
        
        self.set_view_title('Processes')

    def refresh_list(self):
        self._subprocess_list.refresh()
    
    def update_output(self):
        current_item = self._subprocess_list.currentItem()
        
        if current_item is None:
            # Clear output if no runner is selected
            self._subprocess_output.timer.stop()
            self._subprocess_output.clear()
        else:
            # Update stopped runner only if its output
            # isn't already displayed
            self._subprocess_output.timer.stop()
            self._subprocess_output.update()
            
            if current_item.is_running():
                self._subprocess_output.timer.start()
    
    def current_log_path(self):
        current_item = self._subprocess_list.currentItem()
        if current_item is None:
            return None
        
        return current_item.log_path()
    
    def on_show(self):
        self.refresh_list()

    def receive_event(self, event_type, data):
        # TODO: Manage events sent from actor
        # (e.g. when a runner is instanciated ?)
        pass
