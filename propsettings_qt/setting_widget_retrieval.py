from typing import Optional, Dict, Type

from PySide2 import QtWidgets

from propsettings.setting import Setting
from propsettings.setting_type import SettingType
from propsettings.setting_types.range_setting_type import Range
from propsettings.setting_types.selectable_setting_type import Selectable
from propsettings_qt.input_handlers.bool_handler import BoolHandler
from propsettings_qt.input_handlers.input_handler import InputHandler
from propsettings_qt.input_handlers.object_handler import ObjectHandler
from propsettings_qt.input_handlers.range_handler import RangeHandler
from propsettings_qt.input_handlers.selectable_handler import SelectableHandler
from propsettings_qt.input_handlers.text_handler import TextHandler


setting_type_handlers: Dict[Type[SettingType], Type[InputHandler]] = {
	Range: RangeHandler,
	Selectable: SelectableHandler,
}

setting_value_type_handlers: Dict[type, Type[InputHandler]] = {
	bool: BoolHandler,
	int: TextHandler,
	float: TextHandler,
	str: TextHandler,
}


def get_setting_widget(obj, setting: Setting) -> QtWidgets.QWidget:
	"""
	Obtener el QWidget apropiado para editar una setting.
	:param obj:
	:param setting:
	:return:
	"""
	widget = _get_widget_by_setting_type(obj, setting)

	# if it hasn't setting type, get widget by value type
	if widget is None:
		widget = _get_widget_by_value_type(obj, setting)

	# decorate widget with setting's decorators
	# TODO

	return widget


def _get_widget_by_setting_type(obj, setting: Setting) -> Optional[QtWidgets.QWidget]:
	setting_type = setting.setting_type
	if setting_type is not None:
		setting_type_type = type(setting_type)
		if setting_type_type in setting_type_handlers:
			handler_class = setting_type_handlers[setting_type_type]
			handler = handler_class(setting_type, obj, setting)
			widget = handler.get_widget()
			return widget
	return None


def _get_widget_by_value_type(obj, setting: Setting) -> QtWidgets.QWidget:
	setting_value_type = setting.setting_value_type or type(setting.fget(obj))
	if setting_value_type in setting_value_type_handlers:
		handler_class: type = setting_value_type_handlers[setting_value_type]
		handler: InputHandler = handler_class(obj, setting)
		widget = handler.get_widget()
	else:
		widget = ObjectHandler(obj, setting).get_widget()
	return widget
