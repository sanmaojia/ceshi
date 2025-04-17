import os,platform

#改变字体颜色可以直接调用

"""

调用方式为
ColorPrinter.print("这是紫色文字", color="magenta")
ColorPrinter.print("这是粗体紫色", color="magenta", bold=True)

"""
class ColorPrinter:
    #使用ANSI转义序列来设置文本颜色
    # 终端支持的颜色列表
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'default': '\033[39m',
    }

    STYLE_BOLD = '\033[1m'
    STYLE_RESET = '\033[0m'

    @classmethod
    def print(cls, text, color='default', bold=False):
        color_code = cls.COLORS.get(color.lower(), cls.COLORS['default'])
        bold_code = cls.STYLE_BOLD if bold else ''
        reset_code = cls.STYLE_RESET
        print(f"{bold_code}{color_code}{text}{reset_code}")

