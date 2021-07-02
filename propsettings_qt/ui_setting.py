from PySide2 import QtWidgets, QtGui


# TODO marcar como deprecated
class SettingWidget(QtWidgets.QWidget):
	"""
	Widget que tiene un label y un campo de edición para editar la configuración (Setting) de un objeto.
	"""

	def __init__(self, setting_owner, setting, parent=None):
		super(SettingWidget, self).__init__(parent)

		self.setting_owner = setting_owner
		self.setting = setting

		self.label = QtWidgets.QLabel(setting.label)
		self.edit = QtWidgets.QLineEdit()
		self.edit.editingFinished.connect(self._on_text_edited)

		self.prop_type = self.get_setting_type()
		self._validate_property_type(self.prop_type)
		self._set_edit_from_value()

		layout = QtWidgets.QHBoxLayout()
		layout.addWidget(self.label)
		layout.addWidget(self.edit)

		self.setLayout(layout)

	def _on_text_edited(self):
		"""
		Evento ejecutado cuando el valor del campo de edición es editado.
		:param text:
		:return:
		"""
		value = self._get_value_from_edit()
		self._set_value(value)

	def _validate_property_type(self, tp: type):
		"""
		Preparar el campo de edición para que pueda aceptar valores del tipo de dato de la propiedad.
		:param type:
		:return:
		"""
		if tp == int:
			self.edit.setValidator(QtGui.QIntValidator())
		elif tp == float:
			self.edit.setValidator(QtGui.QDoubleValidator())
		elif tp == list:
			pass
		elif tp == dict:
			pass
		elif tp == set:
			pass
		elif tp == object:
			pass

	def get_setting_type(self):
		"""
		Obtener el tipo de dato del parámetro configurable.
		:return:
		"""
		return self.setting.setting_value_type or type(self._get_value())

	def _get_value(self):
		"""
		Obtener el valor del parámetro configurable.
		:return:
		"""
		return self.setting.fget(self.setting_owner)

	def _set_value(self, value):
		"""

		:param value:
		:return:
		"""
		self.setting.fset(self.setting_owner, value)

	def _get_value_from_edit(self):
		"""
		Obtener valor a partir del string editado en el campo de edición
		:return:
		"""
		txt = self.edit.text()
		if self.prop_type == int:
			return int(txt)
		elif self.prop_type == float:
			return float(txt)
		else:
			return txt

	def _set_edit_from_value(self):
		"""
		Poner el valor de la propiedad en el QLineEdit (campo de edición)
		:return:
		"""
		value = self._get_value()
		self.edit.setText(str(value))


