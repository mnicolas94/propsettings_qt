from typing import List

from PySide2 import QtWidgets
from PySide2.QtWidgets import QVBoxLayout, QScrollArea, QWidget

from propsettings.setting import Setting
from propsettings import configurable
from propsettings_qt import setting_widget_retrieval


class SettingsAreaWidget(QScrollArea):
    """
    Widget que muestra las configuraciones de un objeto y permite editarlas.
    """

    def __init__(self, parent=None, layout=None):
        super(SettingsAreaWidget, self).__init__(parent=parent)
        layout = layout or QVBoxLayout()
        wgt = QWidget()
        wgt.setLayout(layout)
        self.setWidgetResizable(True)
        self.setWidget(wgt)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

        self.tittle_label = QtWidgets.QLabel('Properties')
        self.widget().layout().addWidget(self.tittle_label)
        self.widget().layout().addStretch()

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
            widgets_added = self.widget().layout().count() - 2
            pos = widgets_added + 1
            self.widget().layout().insertWidget(pos, stg_widget)

    def clear(self):
        while self.widget().layout().count() > 2:  # 2 porque el 1ro es el titulo y el 2do es el spacer
            item = self.widget().layout().itemAt(1)
            wgt = item.widget()
            if wgt:
                self.widget().layout().removeItem(item)
                wgt.deleteLater()

    def get_setting_widget(self, obj, setting: Setting):
        """
        Obtener un widget que gestione la entrada para modificar una variable de tipo Setting.
        :param obj:
        :param setting:
        :return:
        """
        setting_widget = QWidget()

        label = QtWidgets.QLabel(setting.label)
        input_widget = setting_widget_retrieval.get_setting_widget(obj, setting)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(input_widget)

        setting_widget.setLayout(layout)
        return setting_widget

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
