from typing import Optional, Dict, Type, Any

from PySide2 import QtWidgets

from propsettings.setting import Setting
from propsettings.setting_type import SettingType
from propsettings.setting_types.range_setting_type import Range
from propsettings.setting_types.selectable_setting_type import Selectable
from propsettings_qt.input_handlers.bool_handler import BoolHandler
from propsettings_qt.input_handlers.input_handler import SettingDrawer
from propsettings_qt.input_handlers.object_handler import ObjectHandler
from propsettings_qt.input_handlers.range_handler import RangeHandler
from propsettings_qt.input_handlers.selectable_handler import SelectableHandler
from propsettings_qt.input_handlers.text_handler import TextHandler
from propsettings_qt.object_drawers.default_drawer import DefaultObjectDrawer
from propsettings_qt.object_drawers.object_drawer import ObjectDrawer


object_drawers: Dict[type, Type[ObjectDrawer]] = {
}

setting_type_drawers: Dict[Type[SettingType], Type[SettingDrawer]] = {
	Range: RangeHandler,
	Selectable: SelectableHandler,
}

setting_value_type_handlers: Dict[type, Type[SettingDrawer]] = {
	bool: BoolHandler,
	int: TextHandler,
	float: TextHandler,
	str: TextHandler,
}


def register_object_drawer(object_type: type, object_drawer_type: Type[ObjectDrawer]):
	if object_type not in object_drawers:
		if issubclass(object_drawer_type, QtWidgets.QWidget):
			object_drawers[object_type] = object_drawer_type


def register_setting_type_drawer(setting_type: Type[SettingType], handler_type: Type[SettingDrawer]):
	if setting_type not in setting_type_drawers:
		setting_type_drawers[setting_type] = handler_type


def get_object_drawer(obj) -> QtWidgets.QWidget:
	obj_type = type(obj)
	obj_drawer = None
	if obj_type in object_drawers:
		drawer_type = object_drawers[obj_type]
		if issubclass(drawer_type, QtWidgets.QWidget):
			widget = drawer_type()
			obj_drawer = widget
	if obj_drawer is None:
		obj_drawer = DefaultObjectDrawer()
	obj_drawer.draw_object(obj)
	return obj_drawer


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
		if setting_type_type in setting_type_drawers:
			handler_class = setting_type_drawers[setting_type_type]
			handler = handler_class(setting_type, obj, setting)
			widget = handler.get_widget()
			return widget
	return None


def _get_widget_by_value_type(obj, setting: Setting) -> QtWidgets.QWidget:
	setting_value_type = setting.setting_value_type or type(setting.fget(obj))
	if setting_value_type in setting_value_type_handlers:
		handler_class: type = setting_value_type_handlers[setting_value_type]
		handler: SettingDrawer = handler_class(obj, setting)
		widget = handler.get_widget()
	else:
		widget = ObjectHandler(obj, setting).get_widget()
	return widget
