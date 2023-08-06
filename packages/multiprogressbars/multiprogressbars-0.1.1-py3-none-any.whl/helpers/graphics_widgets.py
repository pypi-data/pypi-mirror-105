from time import time
from datetime import timedelta
from os import cpu_count
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui


class LabeledProgressBar(QtWidgets.QProgressBar):
    createMenuSignal = QtCore.pyqtSignal(int, object, bool)
    unit_conv = {3: 'k', 6: 'M', 9: 'G', 12: 'T'}

    ColorException = '#d40a00'
    ColorCancelled = '#aaaaaa'

    def __init__(self, total=100, name=" ", units_symbol="", max_update_freq=0.02, pid=None, parent=None):
        super(LabeledProgressBar, self).__init__(parent)
        self.total = total
        self.units_symbol = units_symbol
        self.pid = pid
        self.paused = False

        self.task_name = f"{name}"
        self.full_name = self.get_full_name(self.task_name)  # with 'Task {pid}: ' prefix

        self.min_update_increment = total // 500
        self.max_update_frequency = max_update_freq

        self.last_updated = self.get_time()
        self.recent_iteration_speeds = []
        self.elapsed_time = 0
        self.remaining_time = 0

        self.total_str = self.get_formatted_number(total, self.units_symbol)
        self.progress_str = self.get_progress_str(0)
        self.frequency_str = self.get_frequency_str()
        self.elapsed_time_str = self.get_elapsed_time_str()
        self.remaining_time_str = self.get_remaining_time_str()

        self.prefix_label = QtWidgets.QLabel(self.full_name)
        self.progress_label = QtWidgets.QLabel(self.progress_str)
        self.frequency_label = QtWidgets.QLabel(self.frequency_str)
        self.elapsed_time_label = QtWidgets.QLabel(self.elapsed_time_str)
        self.remaining_time_label = QtWidgets.QLabel(self.remaining_time_str)

        self.prefix_label.setEnabled(False)
        self.progress_label.setEnabled(False)
        self.frequency_label.setEnabled(False)
        self.elapsed_time_label.setEnabled(False)
        self.remaining_time_label.setEnabled(False)

        self.setMinimumSize(200, 20)
        self.setRange(0, total)
        self.setMouseTracking(False)
        self.setTextVisible(False)

        self.show()

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.MouseButton.RightButton:
            pos = a0.globalPos()
            self.createMenuSignal.emit(self.pid, pos, self.paused)

    def set_max_update_frequency(self, value):
        self.max_update_frequency = value

    def set_color(self, hex_str):
        style_str = """QProgressBar::chunk{background-color : """ + hex_str + """;}"""
        self.setStyleSheet(style_str)

    @classmethod
    def get_formatted_number(cls, value, symbol):
        factor, unit_prefix = cls.get_units_prefix(value)
        if factor == 0:
            fmt_value = f' {value}'
        else:
            fmt_value = '{:.2f}'.format(round(value / (10 ** factor), 2))
        return "  {} {}{}".format(fmt_value, unit_prefix, symbol)

    @classmethod
    def get_units_prefix(cls, num):
        # uses base10 location of digits to get units prefix, i.e. not equivlant to byte conversion if units are bytes
        digits = len(str(int(num))) - 2
        factor = 3 * round(digits / 3)
        if factor not in cls.unit_conv.keys():
            if factor > 2:
                factor = max(cls.unit_conv.keys())
            else:
                return 0, ''
        return factor, cls.unit_conv[factor]

    def get_progress_str(self, value):
        value_str = self.get_formatted_number(value, self.units_symbol)
        out = ' / '.join([value_str, self.total_str])
        return f'  {out}'

    def get_frequency_str(self):
        its_suffix = 'it/s'
        self.mean_speed = 1

        if len(self.recent_iteration_speeds) == 0:
            return f'  {its_suffix}'

        self.recent_iteration_speeds = self.recent_iteration_speeds[-10:]
        self.mean_speed = round(sum(self.recent_iteration_speeds) / len(self.recent_iteration_speeds), 1)
        return f'  {self.mean_speed} {its_suffix}'

    def get_elapsed_time_str(self):
        return f'  {timedelta(seconds=round(self.elapsed_time))}'

    def get_remaining_time_str(self):
        its_remaining = self.total - self.value()
        if self.mean_speed == 0:
            self.remaining_time = 0
        else:
            self.remaining_time = its_remaining / self.mean_speed
        return f'  {timedelta(seconds=round(self.remaining_time))}'

    @staticmethod
    def get_time():
        return time()

    def allowed_to_set_value(self, value):
        freq_cond = self.get_time() - self.last_updated >= self.max_update_frequency
        value_cond = value - self.value() >= self.min_update_increment
        return freq_cond and value_cond

    def set_value(self, value):
        value_difference = value - self.value()
        self.setValue(value)

        update_time = self.get_time()
        time_difference = update_time - self.last_updated
        self.last_updated = update_time
        self.elapsed_time += time_difference

        if time_difference > 0:
            self.recent_iteration_speeds.append(value_difference / time_difference)

        self.frequency_str = self.get_frequency_str()
        self.frequency_label.setText(self.frequency_str)

        self.elapsed_time_str = self.get_elapsed_time_str()
        self.elapsed_time_label.setText(self.elapsed_time_str)

        self.remaining_time_str = self.get_remaining_time_str()
        self.remaining_time_label.setText(self.remaining_time_str)

        self.progress_str = self.get_progress_str(value)
        self.progress_label.setText(self.progress_str)

    def get_full_name(self, name):
        if self.pid is None:
            return name
        else:
            return f"Task {self.pid}: {name}"

    def set_name(self, name):
        self.task_name = name
        self.full_name = self.get_full_name(name)
        self.prefix_label.setText(self.full_name)

    def set_total(self, total):
        self.total = total
        progress = self.value()
        self.setRange(progress, self.total)
        self.total_str = self.get_formatted_number(total, self.units_symbol)
        self.progress_str = self.get_progress_str(progress)
        self.progress_label.setText(self.progress_str)


class ZoomingScrollArea(QtWidgets.QScrollArea):
    adjustFontSignal = QtCore.pyqtSignal(object)
    pauseAllSignal = QtCore.pyqtSignal()

    def __init__(self, fontname=None, fontsize=None):
        super().__init__()
        font = QtGui.QFont()
        if fontname is None:
            fontname = font.defaultFamily()
        if fontsize is None:
            fontsize = font.pointSize()

        self.fontname = fontname
        self.fontsize = fontsize

        self.adjust_font(1)
        self.adjustFontSignal.connect(self.adjust_font)

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key.Key_Space:
            self.pauseAllSignal.emit()
        else:
            super().keyPressEvent(a0)

    def wheelEvent(self, a0: QtGui.QWheelEvent):
        mods = a0.modifiers()
        if mods == QtCore.Qt.KeyboardModifier.ControlModifier:
            delta = a0.angleDelta()
            incr = delta.y() // abs(delta.y())
            self.adjustFontSignal.emit(incr)
        else:
            super().wheelEvent(a0)

    def adjust_font(self, incr):
        if incr < 0:
            self.fontsize = max(1, self.fontsize + incr)
        else:
            self.fontsize = min(100, self.fontsize + incr)
        self.setFont(QtGui.QFont(self.fontname, self.fontsize))


class Menu(QtWidgets.QMenu):
    autoscrollSignal = QtCore.pyqtSignal(bool)
    pauseAllSignal = QtCore.pyqtSignal()
    cancelTaskSignal = QtCore.pyqtSignal(int)
    pauseTaskSignal = QtCore.pyqtSignal(int)
    setNumProcessesSignal = QtCore.pyqtSignal(int)

    def __init__(self, autoscroll, pid, pid_paused):
        super(Menu, self).__init__()
        self.autoscroll = autoscroll
        self.pid = pid
        self.pid_paused = pid_paused

        self.create_menu()

    def create_menu(self):
        # global menu options
        autoscroll_str = 'Turn autoscrolling {}'.format('off' if self.autoscroll else 'on')
        autoscroll_act = self.addAction(autoscroll_str)
        autoscroll_act.triggered.connect(self.send_autoscroll_signal)

        pause_all_act = self.addAction('Pause / Unpause all (spacebar)')
        pause_all_act.triggered.connect(self.pauseAllSignal.emit)

        # global set num processes menu
        set_num_processes_menu = self.addMenu('Set number of processes')
        self.set_num_process_acts = []
        for i in range(cpu_count()):
            process_act = QtWidgets.QAction(f'{i + 1}')
            process_act.triggered.connect(partial(self.send_set_num_processes, i + 1))
            self.set_num_process_acts.append(process_act)
            set_num_processes_menu.addAction(process_act)
        self.addSeparator()

        # individual menu options
        cancel_task_act = self.addAction(f'Cancel task {self.pid}')
        cancel_task_act.triggered.connect(self.send_cancel_task_signal)

        pause_str = f'Unpause task {self.pid}' if self.pid_paused else f'Pause task {self.pid}'
        pause_task_act = self.addAction(pause_str)
        pause_task_act.triggered.connect(self.send_pause_task_signal)

    def send_autoscroll_signal(self):
        self.autoscrollSignal.emit(not self.autoscroll)

    def send_cancel_task_signal(self):
        self.cancelTaskSignal.emit(self.pid)

    def send_pause_task_signal(self):
        self.pauseTaskSignal.emit(self.pid)

    def send_set_num_processes(self, num):
        self.setNumProcessesSignal.emit(num)

    @staticmethod
    def confirm_remove_task(pid, task_name):
        confirm = QtWidgets.QMessageBox()
        confirm.addButton('Cancel task', QtWidgets.QMessageBox.AcceptRole)
        confirm.addButton('Resume task', QtWidgets.QMessageBox.RejectRole)
        confirm.setWindowTitle('Confirm cancelling task:')
        confirm.setText(f'Cancel task {pid}?\n {task_name}')
        confirm.exec()

        return confirm.result() == QtWidgets.QMessageBox.AcceptRole
