import os
import sys
import inspect


def import_package_all_module(package_file_path: str, package_import_path: str) -> None:
    file_list = os.listdir(package_file_path)
    for f in file_list:
        if f[0] != "_" and f.endswith(".py"):
            __import__(package_import_path + "." + f[0:-3])


def scan_all_impl_class(interface_class: type) -> list[tuple[type]]:
    module_list: list[tuple[str, type]]
    target_class_list: list[type] = []

    if os.path.exists("./impl"):
        assert os.path.isdir("./impl")
        import_package_all_module("./impl", "impl")
        module_list = inspect.getmembers(sys.modules["impl"], inspect.ismodule)
    else:
        import_package_all_module(".", interface_class.__module__)
        module_list = inspect.getmembers(sys.modules[interface_class.__module__], inspect.ismodule)

    if len(module_list) == 0:
        raise TypeError("There are no modules in the default directory.")

    for ret, mod in module_list:
        class_list: list[tuple[str, type]] = inspect.getmembers(mod, inspect.isclass)

        target_class_list.extend(
            [clazz for ret, clazz in class_list if
             clazz is not interface_class and issubclass(clazz, interface_class)])

    if len(target_class_list) == 0:
        raise TypeError("There are no implementation class in the scanned modules.")

    return [(cls(),) for cls in target_class_list]
