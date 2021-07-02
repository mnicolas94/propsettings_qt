from propsettings.setting import Setting
from project_settings import ProjectSettings
from uix.settings.input_handlers.input_handler import InputHandler


class ObjectHandler(InputHandler):
	"""
	InputHandler que se encarga de las configuraciones que sean de tipo object.
	Estas solo se podrán modificar si tienen miembros de tipo Setting o si son de algún tipo de dato que se puede cargar.
	"""

	def __init__(self, setting_owner, setting: Setting):
		from uix.settings.ui_configurable_selector import ConfigurableSelector
		from uix.settings.ui_settings_area import SettingsAreaWidget

		super().__init__(setting_owner=setting_owner, setting=setting)
		folder = ProjectSettings.instance().get_folder_by_type(self._setting_type)
		if folder is not None:
			base_class = ProjectSettings.instance().get_loadable_base_class(self._setting_type)
			self.widget = ConfigurableSelector(folder, base_class)
			self.widget.eventObjectSelected += self._on_configurable_object_selected
			self._on_configurable_object_selected(self.widget.current_object())
			self._set_value(self.widget.current_object())
		else:
			self.widget = SettingsAreaWidget()
			self.widget.populate_configurations(setting.fget(self._setting_owner))  # TODO probar esta vía

	def get_widget(self):
		return self.widget

	def _on_configurable_object_selected(self, obj):
		"""
		Capturar evento de selección de objeto en combobox. Solo se usa cuando el objeto que se está configurando se
		puede cargar desde memoria externa y por tanto se puede seleccionar en un combobox.
		:param obj:
		:return:
		"""
		self._set_value(obj)

