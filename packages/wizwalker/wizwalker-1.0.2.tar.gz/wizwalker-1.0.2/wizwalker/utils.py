import asyncio
import ctypes
import ctypes.wintypes
import functools
import io
import math
import struct
import subprocess

# noinspection PyCompatibility
import winreg
import zlib
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Iterable, List

import appdirs

from wizwalker.constants import Keycode, kernel32, user32, gdi32


class XYZ:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return self.distance(other)

    def __str__(self):
        return f"<XYZ ({self.x}, {self.y}, {self.z})>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def distance(self, other):
        """
        Calculate the distance between two points
        this does not account for z axis
        """
        if not isinstance(other, type(self)):
            raise ValueError(
                f"Can only calculate distance between instances of {type(self)} not {type(other)}"
            )

        return math.dist((self.x, self.y), (other.x, other.y))

    def yaw(self, other):
        """Calculate perfect yaw to reach another xyz"""
        if not isinstance(other, type(self)):
            raise ValueError(
                f"Can only calculate yaw between instances of {type(self)} not {type(other)}"
            )

        return calculate_perfect_yaw(self, other)

    def relative_yaw(self, *, x: float = None, y: float = None):
        """Calculate relative yaw to reach another x and/or y relative to current"""
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        other = type(self)(x, y, self.z)
        return self.yaw(other)


class Rectangle:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"<Rectangle ({self.x1}, {self.y1}, {self.x2}, {self.y2})>"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter((self.x1, self.x2, self.y1, self.y2))

    def scale_to_client(self, parents: List["Rectangle"], factor: float) -> "Rectangle":
        """
        Scale this rectangle base on parents and a scale factor

        Args:
            parents: List of other rectangles
            factor: Factor to scale by

        Returns:
            The scaled rectangle
        """
        x1_sum = self.x1
        y1_sum = self.y1

        for rect in parents:
            x1_sum += rect.x1
            y1_sum += rect.y1

        converted = Rectangle(
            int(x1_sum * factor),
            int(y1_sum * factor),
            int(((self.x2 - self.x1) * factor) + (x1_sum * factor)),
            int(((self.y2 - self.y1) * factor) + (y1_sum * factor)),
        )

        return converted

    def center(self):
        """
        Get the center point of this rectangle

        Returns:
            The center point
        """
        center_x = ((self.x2 - self.x1) // 2) + self.x1
        center_y = ((self.y2 - self.y1) // 2) + self.y1

        return center_x, center_y

    def paint_on_screen(self, window_handle: int, *, rgb: tuple = (255, 0, 0)):
        """
        Paint this rectangle to the screen for debugging

        Args:
            rgb: Red, green, blue tuple to define the color of the rectangle
            window_handle: Handle to the window to paint the rectangle on
        """
        paint_struct = PAINTSTRUCT()
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdc
        device_context = user32.GetDC(window_handle)
        brush = gdi32.CreateSolidBrush(ctypes.wintypes.RGB(*rgb))

        user32.BeginPaint(window_handle, ctypes.byref(paint_struct))

        # left, top = top left corner; right, bottom = bottom right corner
        draw_rect = ctypes.wintypes.RECT()
        draw_rect.left = self.x1
        draw_rect.top = self.y1
        draw_rect.right = self.x2
        draw_rect.bottom = self.y2

        # https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createrectrgnindirect
        region = gdi32.CreateRectRgnIndirect(ctypes.byref(draw_rect))
        # https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-fillrgn
        gdi32.FillRgn(device_context, region, brush)

        user32.EndPaint(window_handle, ctypes.byref(paint_struct))
        user32.ReleaseDC(window_handle, device_context)
        gdi32.DeleteObject(brush)
        gdi32.DeleteObject(region)


class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hdc", ctypes.wintypes.HDC),
        ("fErase", ctypes.wintypes.BOOL),
        ("rcPaint", ctypes.wintypes.RECT),
        ("fRestore", ctypes.wintypes.BOOL),
        ("fIncUpdate", ctypes.wintypes.BOOL),
        ("rgbReserved", ctypes.c_char * 32),
    ]


# Modified from
# https://github.com/Gorialis/jishaku/blob/f18b40d39c1700e1739b799450b8dc4532c273a5/jishaku/functools.py#L19-L64
# This license covers the below function
# MIT License
#
# Copyright (c) 2020 Devon (Gorialis) R
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
def executor_function(sync_function: Callable):
    @functools.wraps(sync_function)
    async def sync_wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        internal_function = functools.partial(sync_function, *args, **kwargs)

        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, internal_function)

    return sync_wrapper


def get_wiz_install() -> Path:
    """
    Get the game install root dir
    """
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

    try:
        key = winreg.OpenKey(
            reg,
            r"Software\Microsoft\Windows\CurrentVersion\Uninstall\{A9E27FF5-6294-46A8-B8FD-77B1DECA3021}",
            0,
            winreg.KEY_READ,
        )
    except OSError:
        raise Exception("Wizard101 install not found.")

    install_location = Path(winreg.QueryValueEx(key, "InstallLocation")[0]).absolute()
    return install_location


def start_instance():
    """
    Starts a wizard101 instance
    """
    location = get_wiz_install()
    subprocess.Popen(
        rf"{location}\Bin\WizardGraphicalClient.exe -L login.us.wizard101.com 12000",
        cwd=rf"{location}\Bin",
    )


def instance_login(window_handle: int, username: str, password: str):
    """
    Login to an instance on the login screen

    Args:
        window_handle: Handle to window
        username: Username to login with
        password: Password to login with
    """

    def send_chars(chars: str):
        for char in chars:
            user32.SendMessageW(window_handle, 0x102, ord(char), 0)

    send_chars(username)
    # tab
    user32.SendMessageW(window_handle, 0x102, 9, 0)
    send_chars(password)
    # enter
    user32.SendMessageW(window_handle, 0x102, 13, 0)


# TODO: use login window for this
# -- [LoginWindow] GameLoginWindow
# --- [title1 shadow] ControlText
# --- [loginPassword] ControlEdit
# --- [passwordText] ControlText
# --- [accountText] ControlText
# --- [okButton] ControlButton
# --- [cancelButton] ControlButton
# --- [title1] ControlText
# --- [loginName] ControlEdit
async def start_instances_with_login(instance_number: int, logins: Iterable):
    """
    Start a number of instances and login to them with logins

    Args:
        instance_number: number of instances to start
        logins: logins to use
    """
    start_handles = set(get_all_wizard_handles())

    for _ in range(instance_number):
        start_instance()

    # TODO: have way to properly check if instances are on login screen
    # waiting for instances to start
    await asyncio.sleep(7)

    new_handles = set(get_all_wizard_handles()).difference(start_handles)

    for handle, username_password in zip(new_handles, logins):
        username, password = username_password.split(":")
        instance_login(handle, username, password)


def calculate_perfect_yaw(current_xyz: XYZ, target_xyz: XYZ) -> float:
    """
    Calculates the perfect yaw to reach an xyz in a stright line

    Args:
        current_xyz: Starting position xyz
        target_xyz: Ending position xyz
    """
    target_line = math.dist(
        (current_xyz.x, current_xyz.y), (target_xyz.x, target_xyz.y)
    )
    origin_line = math.dist(
        (current_xyz.x, current_xyz.y), (current_xyz.x, current_xyz.y - 1)
    )
    target_to_origin_line = math.dist(
        (target_xyz.x, target_xyz.y), (current_xyz.x, current_xyz.y - 1)
    )
    # target_angle = math.cos(origin_line / target_line)
    target_angle = math.acos(
        (pow(target_line, 2) + pow(origin_line, 2) - pow(target_to_origin_line, 2))
        / (2 * origin_line * target_line)
    )

    if target_xyz.x > current_xyz.x:
        # outside
        target_angle_degres = math.degrees(target_angle)
        perfect_yaw = math.radians(360 - target_angle_degres)
    else:
        # inside
        perfect_yaw = target_angle

    return perfect_yaw


def get_cache_folder() -> Path:
    """
    Get the wizwalker cache folder
    """
    app_name = "WizWalker"
    app_author = "StarrFox"
    cache_dir = Path(appdirs.user_cache_dir(app_name, app_author))

    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    return cache_dir


def get_logs_folder() -> Path:
    """
    Get the wizwalker log folder
    """
    app_name = "WizWalker"
    app_author = "StarrFox"
    log_dir = Path(appdirs.user_log_dir(app_name, app_author))

    if not log_dir.exists():
        log_dir.mkdir(parents=True)

    return log_dir


def check_if_process_running(handle: int) -> bool:
    """
    Checks if a process is still running
    True = Running
    False = Not
    """
    # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodeprocess
    exit_code = ctypes.wintypes.DWORD()
    kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
    # 259 is the value of IS_ALIVE
    return exit_code.value == 259


def get_pid_from_handle(handle: int) -> int:
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid
    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(handle, ctypes.byref(pid))
    return pid.value


def get_all_wizard_handles() -> list:
    """
    Get handles to all currently open wizard clients
    """
    target_class = "Wizard Graphical Client"

    def callback(handle):
        class_name = ctypes.create_unicode_buffer(len(target_class))
        user32.GetClassNameW(handle, class_name, len(target_class) + 1)
        if target_class == class_name.value:
            return True

    return get_windows_from_predicate(callback)


def get_windows_from_predicate(predicate: Callable) -> list:
    """
    Get all windows that match a predicate

    Args:
        predicate: the predicate windows should pass

    Examples:
        .. code-block:: py

            def predicate(window_handle):
                if window_handle == 0:
                    # handle will be returned
                    return True
                else:
                    # handle will not be returned
                    return False
    """
    handles = []

    def callback(handle, _):
        if predicate(handle):
            handles.append(handle)

        # iterate all windows, (True)
        return 1

    enumwindows_func_type = ctypes.WINFUNCTYPE(
        ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
    )

    callback = enumwindows_func_type(callback)
    user32.EnumWindows(callback, 0)

    return handles


def pharse_template_id_file(file_data: bytes) -> dict:
    """
    Pharse a template id file's data
    """
    if not file_data.startswith(b"BINd"):
        raise RuntimeError("No BINd id string")

    data = zlib.decompress(file_data[0xD:])

    total_size = len(data)
    data = io.BytesIO(data)

    data.seek(0x24)

    out = {}
    while data.tell() < total_size:
        size = ord(data.read(1)) // 2

        string = data.read(size).decode()
        data.read(8)  # unknown bytes

        # Little endian int
        entry_id = struct.unpack("<i", data.read(4))[0]

        data.read(0x10)  # next entry

        out[entry_id] = string

    return out


def pharse_node_data(file_data: bytes) -> dict:
    """
    Converts data into a dict of node nums to points
    """
    entry_start = b"\xFE\xDB\xAE\x04"

    node_data = {}
    # no nodes
    if len(file_data) == 20:
        return node_data

    # header
    file_data = file_data[20:]

    last_start = 0
    while file_data:
        start = file_data.find(entry_start, last_start)
        if start == -1:
            break

        # fmt: off
        entry = file_data[start: start + 48 + 2]

        cords_data = entry[16: 16 + (4 * 3)]
        x = struct.unpack("<f", cords_data[0:4])[0]
        y = struct.unpack("<f", cords_data[4:8])[0]
        z = struct.unpack("<f", cords_data[8:12])[0]

        node_num = entry[48: 48 + 2]
        unpacked_num = struct.unpack("<H", node_num)[0]
        # fmt: on

        node_data[unpacked_num] = (x, y, z)

    return node_data


async def timed_send_key(window_handle: int, key: Keycode, seconds: float):
    """
    Send a key for a number of seconds

    Args:
        window_handle: Handle to window to send key to
        key: The key to send
        seconds: Number of seconds to send the key
    """
    keydown_task = asyncio.create_task(_send_keydown_forever(window_handle, key))
    await asyncio.sleep(seconds)
    keydown_task.cancel()
    user32.SendMessageW(window_handle, 0x101, key.value, 0)


async def _send_keydown_forever(window_handle: int, key: Keycode):
    while True:
        user32.SendMessageW(window_handle, 0x100, key.value, 0)
        await asyncio.sleep(0.05)
