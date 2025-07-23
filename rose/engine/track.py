import random
from typing import Union
import os
import random
from rose.engine import config
from rose.common import obstacles
from rose.engine import csv_file_handler


class Track(object):
    """
    Initialize the Track object.

    Args:
        is_track_random (bool): Whether the track should be generated randomly per player.
    """
    def __init__(self, is_track_random: bool = False) -> None:
        self._matrix: Union[list[list[str]], None] = None
        self.is_track_random: bool = is_track_random
        self.reset()
        self.custom_index: int = 0
        self.custom_map: list[list[str]] = csv_file_handler.CsvFileHandler.read_as_matrix("map/custom_map.csv")

        # Game state interface
    def update(self) -> None:
        """
        Advance the game state by one step:
        - If a valid custom map exists and is enabled, generate a row from it.
        - Otherwise, generate a random row.
        """
        self._matrix.pop()
        map_name: str = "map/custom_map.csv"
        if os.path.exists(map_name) and self.custom_map != [] and ("disabled" not in map_name):
            self.custom_map = self.check_obstacle(self.custom_map)
            self._matrix.insert(0, self.generate_custom_map(self.custom_map))
        else:
            self._matrix.insert(0, self._generate_row())

    def state(self) -> list[dict[str, Union[str, int]]]:
        """Return read only serialize-able state for sending to client"""
        items: list[dict[str, Union[str, int]]] = []
        for y, row in enumerate(self._matrix):
            for x, obs in enumerate(row):
                if obs != obstacles.NONE:
                    items.append({"name": obs, "x": x, "y": y})
        return items

    def matrix(self) -> list[list[str]]:
        """Return the track matrix"""
        return self._matrix

    # Track interface

    def get(self, x: int , y: int) -> str:
        """Return the obstacle in position x, y"""
        return self._matrix[y][x]

    def set(self, x: int, y: int, obstacle: str) -> None:
        """Set obstacle in position x, y"""
        self._matrix[y][x] = obstacle

    def clear(self, x: int, y: int) -> None:
        """Clear obstacle in position x, y"""
        self._matrix[y][x] = obstacles.NONE

    def reset(self) -> None:
        self._matrix = [
            [obstacles.NONE] * config.matrix_width for x in range(config.matrix_height)
        ]

    # Private

    def _generate_row(self) -> list[str]:
        """
        Generates new row with obstacles

        Try to create fair but random obstacle stream. Each player get the same
        obstacles, but in different cells if 'is_track_random' is True.
        Otherwise, the tracks will be identical.
        """

        # Create initial empty row
        row: list[str] = [obstacles.NONE] * config.matrix_width

        # Get a random obstacle
        obstacle: str = obstacles.get_random_obstacle()

        if self.is_track_random:
            for lane in range(config.max_players):
                # Get a random cell for each player
                cell: int = random.choice(range(0, config.cells_per_player))

                row[cell + lane * config.cells_per_player] = obstacle
        else:
            # Get a random cell, and use it for all players
            cell: int = random.choice(range(0, config.cells_per_player))

            for lane in range(config.max_players):
                row[cell + lane * config.cells_per_player] = obstacle

        return row

    def check_obstacle(self, custom_map:list[list[str]]) -> list[list[str]]:
        """
        Validates that all obstacles in the custom map are valid.
        Replaces any invalid obstacle with a random one.

        Args:
            custom_map (list[list[str]]): The loaded map as strings.

        Returns:
            list[list[str]]: Validated map with corrected obstacles.
        """


        for row in range(len(custom_map)-1):
            for col in range(len(custom_map[row])-1):
                if custom_map[row][col] not in obstacles.ALL:
                    print(custom_map[row][col])
                    custom_map[row][col] = obstacles.get_random_obstacle()
        return custom_map

    def generate_custom_map(self, custom_map: list[list[str]]) -> list[str]:
        """
        Returns the next row from the custom map as a list of obstacle objects.

        Args:
            custom_map (list[list[str]]): The full custom map as strings.

        Returns:
            list: A row of obstacles for insertion into the matrix.
        """

        if self.custom_index >= len(custom_map):
            self.custom_index = 0

        row: list[str] = custom_map[self.custom_index]
        self.custom_index += 1

        return [
            getattr(obstacles, value.upper(), obstacles.NONE) if value else obstacles.NONE
            for value in row
        ]

