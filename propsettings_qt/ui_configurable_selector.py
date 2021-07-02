from PySide2 import QtWidgets
from uix.settings.ui_settings_area import SettingsAreaWidget
from utils import inspection
from pypegraph.action import Action


class ConfigurableSelector(QtWidgets.QWidget):
	"""
	Widget para cargar clases que hereden de una clase base especificada
	e inicializar un combobox con instancias de dichas clases. Consta de dos elementos agrupados en un vertical layout.
	El primero es el combobox. El segundo es un area para configurar las uiproperties del objeto seleccionado.
	"""

	def __init__(self, objects_dir, objects_class, parent=None):
		super(ConfigurableSelector, self).__init__(parent)
		self.objects_dir = objects_dir
		self.objects_class = objects_class

		self.objects = []
		self.current_index = 0

		self.eventObjectSelected = Action()

		layout = QtWidgets.QVBoxLayout(self)
		self.setLayout(layout)

		self.combobox = QtWidgets.QComboBox(self)
		self.combobox.currentIndexChanged.connect(self._selection_changed)
		self.combobox.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
		self.layout().addWidget(self.combobox)

		self.conf_properties = SettingsAreaWidget()
		self.conf_properties.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
		self.layout().addWidget(self.conf_properties)

		self._populate_objects()

	def populate_class(self, class_dir, clazz):
		"""
		Inicializar el combobox con una nueva clase.
		:param class_dir:
		:param clazz:
		:return:
		"""
		self.objects_dir = class_dir
		self.objects_class = clazz
		self._populate_objects()

	def _populate_objects(self):
		"""
		Inicializar el combobox.
		:return:
		"""
		# cargar objetos
		classes = inspection.import_dir_classes(self.objects_dir, self.objects_class, recursive=True)
		classes = sorted(classes, key=lambda cls: str(cls))
		for cls in classes:
			instance = cls()
			self.objects.append(instance)
			self.combobox.addItem(str(instance))
		self.eventObjectSelected.invoke(self.current_object())

	def _selection_changed(self, index):
		self.current_index = index
		self.conf_properties.populate_configurations(self.current_object())
		self.eventObjectSelected.invoke(self.current_object())

	def current_object(self):
		if len(self.objects) > 0:
			return self.objects[self.current_index]
		else:
			return None
