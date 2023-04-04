import os
import sys
import logging
import inspect
from typing import TypeVar

T = TypeVar('T')


def import_package_all_module__force(package_file_path: str, package_import_path: str) -> None:
    """
    | 在一个 package 没有把需要暴露的类注册到 __init__.py 中时 暴力的按照文件目录进行扫描。

    :param package_file_path: package 的文件系统目录
    :param package_import_path: package 的 import 路径
    :return: None
    """
    assert os.path.isdir(package_file_path)

    file_list = os.listdir(package_file_path)
    for f in file_list:
        if f[0] != "_" and f.endswith(".py"):
            __import__(package_import_path + "." + f[0:-3])


def scan_all_impl_class(interface_class: type[T]) -> list[type[T]]:
    """
    | important: 对于实现的子类,必须在 __init__.py 中 from import 出来!
    |
    | import interface_class 所在的 module 的 package
    | 导入成功后，从各个 module 中筛出 class
    | 收集继承了 interface_class 的子类，并返回包含这些类的列表

    :param interface_class: 接口类、基类
    :return: interface_class的子类构成的列表
    """
    module_list: list[tuple[str, type]]
    target_class_list: list[type[T]] = []

    file_path: str = __import__(interface_class.__module__).__file__.replace("\\__init__.py", "")

    module_path: str = interface_class.__module__[:interface_class.__module__.rfind('.')]

    if os.path.exists(file_path + "\\impl"):
        module_path += ".impl"
    else:
        logging.warning("file_path:\"" + file_path + "\"not exist, This will cause the program to try to find the "
                                                     "implementing class from the same directory as the interface "
                                                     "class")
    del file_path
    __import__(module_path)

    target_class_list.extend(
        [clazz for ret, clazz in inspect.getmembers(sys.modules[module_path], inspect.isclass) if
         clazz is not interface_class and issubclass(clazz, interface_class)])

    if len(target_class_list) == 0:
        raise RuntimeError(
            "There are no implementation class for " + interface_class.__module__ + " in the scanned modules.")

    return target_class_list


def scan_all_impl(interface_class: type[T], *args, **kwargs) -> list[T]:
    """
    | 按 scan_all_impl_class 规则，所扫描到的类进行实例化，返回实例的列表

    :param interface_class: 接口类、基类
    :param args: 实例化子类所需的参数 (所有子类都保持一致的参数)
    :param kwargs: 实例化子类所需的参数 (所有子类都保持一致的参数)
    :return: interface_class的子类的实例构成的列表
    """
    return [cls(*args, **kwargs) for cls in scan_all_impl_class(interface_class)]


# noinspection PyPep8Naming
def scanAllImpl4Parameterized(interface_class: type[T], *args, **kwargs) -> list[tuple[T]]:
    """
    | 按 scan_all_impl_class 规则，所扫描到的类进行实例化
    | 按照 parameterized 库的 parameterized.expand 方法对其进行包装并返回

    :param interface_class: 接口类、基类
    :param args: 实例化子类所需的参数 (所有子类都保持一致的参数)
    :param kwargs: 实例化子类所需的参数 (所有子类都保持一致的参数)
    :return: 按 parameterized.expand 入参(单参数 impl)包装的 interface_class 子类的实例列表
    """
    return [(cls(*args, **kwargs),) for cls in scan_all_impl_class(interface_class)]


def dynamic_load_impl_class(interface_class: type[T], target_subclass_prefix: str) -> type[T]:
    """
    | 按 scan_all_impl_class 规则，所扫描到的类
    | 以目标子类名的前缀为标准，返回名称相同的类

    :param interface_class: 接口类、基类
    :param target_subclass_prefix: 目标子类名的前缀，配置与类名相互对应
    :return: target subclass
    """
    for clazz in scan_all_impl_class(interface_class):
        if clazz.__name__.lower().startswith(target_subclass_prefix.lower()):
            return clazz
    raise TypeError(
        "The implementation class which prefix is \"" + target_subclass_prefix + "\" was not found or does not exist.")


def dynamic_load_impl(interface_class: type[T], target_subclass_prefix: str, *args, **kwargs) -> T:
    """
    | 按 scan_all_impl_class 规则，所扫描到的类
    | 以目标子类名的前缀为标准，返回名称相同的类的实例

    :param interface_class: 接口类、基类
    :param target_subclass_prefix: 目标子类名的前缀，配置与类名相互对应
    :param args: 实例化目标类所需的参数
    :param kwargs: 实例化目标类所需的参数
    :return: target subclass instance
    """
    return dynamic_load_impl_class(interface_class, target_subclass_prefix)(*args, **kwargs)
