import shutil

from typing import Callable


class Loader:
    _width: int

    percent = "{:6.2f}%"

    def __init__(self, console, value: float = 0, desc: str = None, done=''):
        self.console = console

        self.desc = desc
        self.value = value
        self.done = done

        # syntax from line is used when in plain mode
        # so why not just just line itself
        self.line = self.console.line(self.desc, self.done)

        if self.console.plain:
            self.update = lambda *args, **kwargs: None
        else:
            if desc:
                self._update(0)
            self.update = self._update

    def __enter__(self):
        if self.console.plain:
            self.line.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.console.plain:
            self.line.__exit__(exc_type, exc_val, exc_tb)
            return

        if exc_type is None:
            self.update(1.0)
        
        self.console.write(self.done + '\n')
        self.console.flush()

    def print(self, *args, func: Callable, end='\n', sep=' '):
        if self.console.plain:
            self.console.print(*args, end=end, sep=sep)
            return

        # remove current progress bar and print
        self.console.write(f'\033[2K\r')
        func(*args, end=end, sep=sep)

        # re draw progressbar
        self.update()

    def _update_width(self):
        self._width, _ = shutil.get_terminal_size((80, 20))

    def _update(self, value: float = None, desc: str = None):
        self._update_width()

        if value is not None:
            self.value = value
        if desc is not None:
            self.desc = desc

        # Standard progress bar desc and label
        desc_length = max(15, self._width)
        desc_str = self.desc_str(desc_length).format(self.value * 100)

        self.console.write(f'\r{desc_str}')
        self.console.flush()

    def desc_str(self, width: int) -> str:
        width = width - 1

        if not self.desc:
            return ' ' * width
        if len(self.desc) <= width:
            return self.desc
        elif len(self.desc) > width:
            return '…' + self.desc[len(self.desc) - width:]
