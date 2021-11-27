from typing import Optional

import pandas as pd


class ComboGameManager:
    def __init__(self,
                 game_table_path: Optional[str] = None,
                 default_table_dir: str = "combo_data"):
        self.player_combo_table = self._import_game_table(game_table_path)

    def _import_game_table(self, game_table_path: Optional[str] = None) -> pd.DataFrame:


    def increase_player_combo(self):
        pass

    def reduce_player_combo(self):
        pass
