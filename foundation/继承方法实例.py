# 单继承与多继承
# 方法重写（Override）
# super()
# 的协作式调用
# 钻石继承（菱形继承）与
# MRO
# 抽象基类（ABC）与抽象方法
# Mixin
# 模式
# 私有属性与名称改写
# 特殊方法（如
# __str__）
# isinstance / issubclass
# 判断
# 组合优于继承的思想体现
# 🧩 场景：构建一个可扩展的
# 日志记录系统（Logging
# System）
# 我们将模拟一个企业级日志系统，支持：
#
# 多种日志级别（INFO, ERROR
# 等）
# 多种输出方式（控制台、文件、网络）
# 可组合的格式化器（带时间戳、带颜色等）
# 强制子类实现核心方法（抽象类）
# 支持插件式扩展（Mixin）
#
# ✅ 完整代码（含详细注释）

from abc import ABC, abstractmethod
import time
from typing import Any


# ==============================
# 1. 抽象基类：定义日志记录器接口
# ==============================
class LoggerBase(ABC):
    """抽象日志记录器基类，强制子类实现核心方法"""

    def __init__(self, name: str):
        self._name = name  # 单下划线：约定为“内部使用”
        self.__created_at = time.time()  # 双下划线：触发名称改写（私有）

    @abstractmethod
    def write(self, message: str, level: str = "INFO") -> None:
        """抽象方法：必须由子类实现"""
        pass

    def log(self, message: str, level: str = "INFO") -> None:
        """公共日志入口，调用 write"""
        formatted = self._format_message(message, level)
        self.write(formatted, level)

    def _format_message(self, message: str, level: str) -> str:
        """默认格式化方法，可被子类重写"""
        return f"[{level}] {self._name}: {message}"

    def __str__(self) -> str:
        """特殊方法：用于 print 或 str()"""
        return f"Logger({self._name})"

    # 提供只读访问私有属性（行业常用做法）
    @property
    def created_at(self) -> float:
        return self.__created_at


# ==============================
# 2. Mixin 类：添加功能（非独立使用）
# ==============================
class TimestampMixin:
    """Mixin：为日志添加时间戳"""

    def _format_message(self, message: str, level: str) -> str:
        # 调用父类（MRO 中的下一个）的 _format_message
        base = super()._format_message(message, level)
        return f"{time.strftime('%Y-%m-%d %H:%M:%S')} {base}"


class ColorMixin:
    """Mixin：为控制台日志添加颜色（简化版）"""
    LEVEL_COLORS = {
        "ERROR": "\033[91m",  # 红色
        "INFO": "\033[94m",  # 蓝色
        "WARNING": "\033[93m",  # 黄色
    }
    RESET = "\033[0m"

    def _format_message(self, message: str, level: str) -> str:
        base = super()._format_message(message, level)#super 只能继承输入的第一个父类
        color = self.LEVEL_COLORS.get(level, "")
        return f"{color}{base}{self.RESET}"


# ==============================
# 3. 具体实现类：单继承 + Mixin
# ==============================
class ConsoleLogger(LoggerBase):
    """控制台日志记录器"""

    def write(self, message: str, level: str = "INFO") -> None:
        print(message)


class FileLogger(LoggerBase):
    """文件日志记录器"""

    def __init__(self, name: str, filepath: str):
        super().__init__(name)
        self.filepath = filepath

    def write(self, message: str, level: str = "INFO") -> None:
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(message + '\n')


# ==============================
# 4. 多继承 + 钻石继承结构（关键！）
# ==============================
# 构建带时间戳和颜色的控制台日志器
class FancyConsoleLogger(TimestampMixin, ColorMixin, ConsoleLogger):
    """
    多继承示例：
    - TimestampMixin 和 ColorMixin 是功能 Mixin
    - ConsoleLogger 是主基类
    - LoggerBase 是抽象基类（最终祖先）

    继承结构（钻石形）：
                LoggerBase
               /          \
        ConsoleLogger     (Mixin 不直接继承 LoggerBase)
             /            /
    TimestampMixin → ColorMixin → FancyConsoleLogger
    实际 MRO 会线性化，确保 LoggerBase 只调用一次。
    """
    pass


# ==============================
# 5. 使用示例与验证
# ==============================
if __name__ == "__main__":
    # 创建日志器实例
    logger = FancyConsoleLogger("MyApp")

    # 测试日志输出（带时间戳 + 颜色）
    logger.log("Application started")
    logger.log("User logged in", "INFO")
    logger.log("Disk space low!", "WARNING")
    logger.log("Database connection failed", "ERROR")

    # 验证继承关系
    print("\n=== 继承关系验证 ===")
    print(f"isinstance(logger, LoggerBase): {isinstance(logger, LoggerBase)}")
    print(f"issubclass(FancyConsoleLogger, ConsoleLogger): {issubclass(FancyConsoleLogger, ConsoleLogger)}")
    print(f"issubclass(FancyConsoleLogger, LoggerBase): {issubclass(FancyConsoleLogger, LoggerBase)}")

    # 查看 MRO（关键！）
    print("\n=== MRO (Method Resolution Order) ===")
    for i, cls in enumerate(FancyConsoleLogger.__mro__):
        print(f"{i}: {cls}")

    # 访问只读属性
    print(f"\nLogger created at timestamp: {logger.created_at}")

    # 尝试直接实例化抽象类（会报错）
    try:
        bad = LoggerBase("test")
    except TypeError as e:
        print(f"\n❌ 无法实例化抽象类: {e}")


# 🔍 逐项解释：覆盖了哪些知识点？
# 知识点
# 在代码中的体现
# 抽象基类（ABC）    LoggerBase
# 使用
# ABC
# 和 @ abstractmethod，不能直接实例化
# 方法重写
# ConsoleLogger.write()
# 重写抽象方法；Mixin
# 重写
# _format_message
# super()
# 协作调用
# Mixin
# 中
# super()._format_message(...)
# 按
# MRO
# 调用下一个类
# 多继承与
# Mixin
# FancyConsoleLogger
# 继承两个
# Mixin + 一个主类
# 钻石继承处理
# 所有类最终都源于
# LoggerBase，但
# MRO
# 确保其方法只调用一次
# MRO
# 查看
# FancyConsoleLogger.__mro__
# 输出线性顺序
# 私有属性
# __created_at
# 被改写为
# _LoggerBase__created_at，通过 @ property
# 安全暴露
# 特殊方法
# __str__
# 定义对象字符串表示
# isinstance / issubclass
# 验证类型关系，常用于框架或插件系统
# 组合思想体现
# Mixin
# 是“功能组合”，而非深层继承；日志器可灵活组装
# 行业实践
# 日志系统是真实场景；Mixin
# 模式广泛用于
# Django、Flask
# 等框架
# 📊 运行输出示例（颜色在终端可见）
# text
# 编辑
# 2025 - 10 - 29
# 14: 30:00[INFO]
# MyApp: Application
# started
# 2025 - 10 - 29
# 14: 30:00[INFO]
# MyApp: User
# logged in
# 2025 - 10 - 29
# 14: 30:00[WARNING]
# MyApp: Disk
# space
# low!
# 2025 - 10 - 29
# 14: 30:00[ERROR]
# MyApp: Database
# connection
# failed
#
# == = 继承关系验证 == =
# isinstance(logger, LoggerBase): True
# issubclass(FancyConsoleLogger, ConsoleLogger): True
# issubclass(FancyConsoleLogger, LoggerBase): True
#
# == = MRO(Method
# Resolution
# Order) == =
# 0: <
#
# class '__main__.FancyConsoleLogger'>
#
#
# 1: <
#
# class '__main__.TimestampMixin'>
#
#
# 2: <
#
# class '__main__.ColorMixin'>
#
#
# 3: <
#
# class '__main__.ConsoleLogger'>
#
#
# 4: <
#
# class '__main__.LoggerBase'>
#
#
# 5: <
#
# class 'abc.ABC'>
#
#
# 6: <
#
# class 'object'>
#
#
# Logger
# created
# at
# timestamp: 1730184600.123456
#
# ❌ 无法实例化抽象类: Can
# 't instantiate abstract class LoggerBase with abstract method write
# 💡 MRO
# 顺序说明：
#
# 当调用
# logger._format_message()
# 时，实际调用链是：
#
# FancyConsoleLogger → TimestampMixin → ColorMixin → ConsoleLogger → LoggerBase
#
# 每个
# Mixin
# 调用
# super()，最终汇聚到
# LoggerBase
# 的默认实现，再逐层包装。