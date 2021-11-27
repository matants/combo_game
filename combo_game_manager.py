import os
from typing import Optional

import pandas as pd


class ComboGameManager:
    def __init__(self,
                 game_table_path: Optional[str] = None,
                 default_table_dir: str = "combo_data"):
        self.default_table_dir = default_table_dir
        self.player_combo_table = self._import_game_table(game_table_path)

    def _import_game_table(self, game_table_path: Optional[str] = None) -> pd.DataFrame:
        if game_table_path is None:
            game_table_path = os.path.join(self.default_table_dir, max(os.listdir(self.default_table_dir)))
        game_table = pd.read_excel(game_table_path)
        return game_table

    def increase_player_combo(self):
        pass

    def reduce_player_combo(self):
        pass
