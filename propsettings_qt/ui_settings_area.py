from typing import List

from PySide2 import QtWidgets

from propsettings.setting import Setting
from propsettings import configurable
from propsettings_qt import setting_widget_retrieval


class SettingsAreaWidget(QtWidgets.QFrame):
    """
    Widget que muestra las configuraciones de un objeto y permite editarlas.
    """

    def __init__(self, parent=None):
        super(SettingsAreaWidget, self).__init__(parent=parent)
        self._layout = QtWidgets.QFormLayout()
        self.setLayout(self._layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

    def populate_configurations(self, obj):
        """
        Quitar todos los elementos existentes e incializar los widgets de cada Setting de un objeto.
        :param obj:
        :return:
        """
        self.clear()
        settings = configurable.get_settings(obj)
        settings = self._sort_settings(settings)
        for stg in settings:
            stg_widget = self.get_setting_widget(obj, stg)
            self._layout.addRow(stg.label, stg_widget)

        if len(settings) > 0:
            self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        else:
            self.setFrameStyle(QtWidgets.QFrame.NoFrame)

    def clear(self):
        while self._layout.count() > 0:
            item = self._layout.itemAt(0)
            wgt = item.widget()
            if wgt:
                self._layout.removeItem(item)
                wgt.deleteLater()

    def get_setting_widget(self, obj, setting: Setting):
        """
        Obtener un widget que gestione la entrada para modificar una variable de tipo Setting.
        :param obj:
        :param setting:
        :return:
        """
        input_widget = setting_widget_retrieval.get_setting_widget(obj, setting)
        return input_widget

    def _sort_settings(self, settings: List[Setting]):
        """
        Ordenar una lista de Settings según los tipos de datos.
        :param settings:
        :return:
        """
        settings_by_sort_order = {}
        for stg in settings:
            settings_by_sort_order.setdefault(stg.sort_order, []).append(stg)

        settings_by_sort_order = sorted(settings_by_sort_order.items(), key=lambda x: x[0])

        sorted_settings = []
        for _, settings in settings_by_sort_order:
            settings.sort(key=lambda stg: stg.label)
            for stg in settings:
                sorted_settings.append(stg)

        return sorted_settings
