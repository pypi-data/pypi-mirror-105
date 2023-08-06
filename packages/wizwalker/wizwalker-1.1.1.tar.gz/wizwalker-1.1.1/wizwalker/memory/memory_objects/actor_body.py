from wizwalker.utils import XYZ
from wizwalker.memory.memory_object import PropertyClass


class ActorBody(PropertyClass):
    async def read_base_address(self) -> int:
        raise NotImplementedError()

    async def position(self) -> XYZ:
        """
        This body's position

        Returns:
            An XYZ representing the position
        """
        return await self.read_xyz(88)

    async def write_position(self, position: XYZ):
        """
        Write this body's position

        Args:
            position: The position to write
        """
        await self.write_xyz(88, position)

    async def pitch(self) -> float:
        """
        This body's pitch

        Returns:
            Float representing pitch
        """
        return await self.read_value_from_offset(100, "float")

    async def write_pitch(self, pitch: float):
        """
        Write this body's pitch

        Args:
            pitch: The pitch to write
        """
        await self.write_value_to_offset(100, pitch, "float")

    async def roll(self) -> float:
        """
        This body's roll

        Returns:
            Float representing roll
        """
        return await self.read_value_from_offset(104, "float")

    # TODO: finish docs
    async def write_roll(self, roll: float):
        await self.write_value_to_offset(104, roll, "float")

    async def yaw(self) -> float:
        return await self.read_value_from_offset(108, "float")

    async def write_yaw(self, yaw: float):
        await self.write_value_to_offset(108, yaw, "float")

    async def height(self) -> float:
        return await self.read_value_from_offset(132, "float")

    async def write_height(self, height: float):
        await self.write_value_to_offset(132, height, "float")

    async def scale(self) -> float:
        return await self.read_value_from_offset(112, "float")

    async def write_scale(self, scale: float):
        await self.write_value_to_offset(112, scale, "float")


class CurrentActorBody(ActorBody):
    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_player_base()
