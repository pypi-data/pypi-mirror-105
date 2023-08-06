from functools import cached_property

import pymem

from . import (
    CacheHandler,
    Keycode,
    MemoryReadError,
    ReadingEnumFailed,
    utils,
)
from .constants import WIZARD_SPEED
from .memory import (
    CurrentActorBody,
    CurrentClientObject,
    CurrentDuel,
    CurrentGameStats,
    CurrentQuestPosition,
    CurrentRootWindow,
    DuelPhase,
    HookHandler,
    CurrentRenderContext,
)
from .mouse_handler import MouseHandler
from .utils import XYZ, check_if_process_running


class Client:
    """
    Represents a connected wizard client

    Args:
        window_handle: A handle to the window this client connects to
    """

    def __init__(self, window_handle: int):
        self.window_handle = window_handle

        self._pymem = pymem.Pymem()
        self._pymem.open_process_from_id(self.process_id)
        self.hook_handler = HookHandler(self._pymem, self)

        self.cache_handler = CacheHandler()
        self.mouse_handler = MouseHandler(self)

        self.stats = CurrentGameStats(self.hook_handler)
        self.body = CurrentActorBody(self.hook_handler)
        self.duel = CurrentDuel(self.hook_handler)
        self.quest_position = CurrentQuestPosition(self.hook_handler)
        self.client_object = CurrentClientObject(self.hook_handler)
        self.root_window = CurrentRootWindow(self.hook_handler)
        self.render_context = CurrentRenderContext(self.hook_handler)

        self._template_ids = None
        self._is_loading_addr = None

    def __repr__(self):
        return f"<Client {self.window_handle=} {self.process_id=}>"

    @cached_property
    def process_id(self) -> int:
        """
        Client's process id
        """
        return utils.get_pid_from_handle(self.window_handle)

    def is_running(self):
        """
        If this client is still running
        """
        return check_if_process_running(self._pymem.process_handle)

    async def activate_hooks(
        self, *, wait_for_ready: bool = True, timeout: float = None
    ):
        """
        Activate all memory hooks but mouseless

        Keyword Args:
            wait_for_ready: If this should wait for hooks to be ready to use (duel exempt)
            timeout: How long to wait for hook values to be witten (None for no timeout)
        """
        await self.hook_handler.activate_all_hooks(
            wait_for_ready=wait_for_ready, timeout=timeout
        )

    async def close(self):
        """
        Closes this client; unhooking all active hooks
        """
        # if the client isn't running there isn't anything to unhook
        if not self.is_running():
            return

        await self.hook_handler.close()

    async def get_template_ids(self) -> dict:
        """
        Get a dict of template ids mapped to their value
        ids are str
        """
        if self._template_ids:
            return self._template_ids

        self._template_ids = await self.cache_handler.get_template_ids()
        return self._template_ids

    async def in_battle(self) -> bool:
        """
        If the client is in battle or not
        """
        try:
            duel_phase = await self.duel.duel_phase()
        except (ReadingEnumFailed, MemoryReadError):
            return False
        else:
            return duel_phase is not DuelPhase.ended

    async def is_loading(self) -> bool:
        """
        If the client is currently in a loading screen
        (does not apply to chacter load in)
        """
        if not self._is_loading_addr:
            mov_instruction_addr = await self.hook_handler.pattern_scan(
                b"\xC6\x05....\x00\xC6\x80.....\x48\x8B",
                module="WizardGraphicalClient.exe",
            )
            # first 2 bytes are the mov instruction and mov type (C6 05)
            rip_offset = await self.hook_handler.read_typed(
                mov_instruction_addr + 2, "int"
            )
            # 7 is the length of this instruction
            self._is_loading_addr = mov_instruction_addr + 7 + rip_offset

        # 1 -> can't move (loading) 0 -> can move (not loading)
        return await self.hook_handler.read_typed(self._is_loading_addr, "bool")

    async def is_in_dialog(self) -> bool:
        """
        If the client is in dialong
        """
        return bool(await self.root_window.get_windows_with_name("wndDialogMain"))

    async def backpack_space(self) -> tuple:
        """
        This client's backpack space used and max
        must be on inventory page to use
        """
        maybe_space_window = await self.root_window.get_windows_with_name(
            "inventorySpace"
        )

        if not maybe_space_window:
            # TODO: replace error
            raise ValueError("must open inventory screen to get")

        text = await maybe_space_window[0].maybe_text()
        text = text.replace("<center>", "")
        used, total = text.split("/")
        return int(used), int(total)

    async def current_energy(self) -> int:
        """
        Client's current energy
        energy globe must be visible to use
        """
        maybe_energy_text = await self.root_window.get_windows_with_name("textEnergy")

        if not maybe_energy_text:
            # TODO: replace error
            raise ValueError("Energy globe not on screen")

        text = await maybe_energy_text[0].maybe_text()
        text = text.replace("<center>", "")
        text = text.replace("</center>", "")
        return int(text)

    def login(self, username: str, password: str):
        """
        Login this client

        Args:
            username: The username to login with
            password: The password to login with
        """
        utils.instance_login(self.window_handle, username, password)

    async def send_key(self, key: Keycode, seconds: float = 0.5):
        await utils.timed_send_key(self.window_handle, key, seconds)

    async def goto(self, x: float, y: float):
        """
        Moves the player to a specific x and y

        Args:
            x: X to move to
            y: Y to move to
        """
        current_xyz = await self.body.position()
        # (40 / 100) + 1 = 1.4
        speed_multiplier = ((await self.client_object.speed_multiplier()) / 100) + 1
        target_xyz = utils.XYZ(x, y, current_xyz.z)
        distance = current_xyz - target_xyz
        move_seconds = distance / (WIZARD_SPEED * speed_multiplier)
        yaw = utils.calculate_perfect_yaw(current_xyz, target_xyz)

        await self.body.write_yaw(yaw)
        await utils.timed_send_key(self.window_handle, Keycode.W, move_seconds)

    async def teleport(self, xyz: XYZ, yaw: int = None):
        """
        Teleport the client

        Args:
            xyz: xyz to teleport to
            yaw: yaw to set or None to not change

        Raises:
            RuntimeError: player hook not active
        """
        await self.body.write_position(xyz)

        if yaw is not None:
            await self.body.write_yaw(yaw)
