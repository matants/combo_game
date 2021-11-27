import datetime
import os
from typing import Optional, List

import pandas as pd

NAME_FIELD = 'שם'
COMBO_FIELD = 'קומבו'
TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class ComboGameManager:
    def __init__(self,
                 game_table_path: Optional[str] = None,
                 default_table_dir: str = "combo_data"):
        self._default_table_dir = default_table_dir
        self.player_combo_table = self._import_game_table(game_table_path)
        self._players_who_arrived = []

    def _import_game_table(self, game_table_path: Optional[str] = None) -> pd.DataFrame:
        if game_table_path is None:
            game_table_path = os.path.join(self._default_table_dir, max(os.listdir(self._default_table_dir)))
        game_table = pd.read_excel(game_table_path)
        return game_table

    def increase_player_combo(self, player_name: str):
        if player_name in list(self.player_combo_table[NAME_FIELD]):
            self.player_combo_table.loc[
                self.player_combo_table.index[self.player_combo_table[NAME_FIELD] == player_name],
                COMBO_FIELD] += 1
        else:
            self.player_combo_table = self.player_combo_table.append({NAME_FIELD: player_name, COMBO_FIELD: 1},
                                                                     ignore_index=True)
        self._players_who_arrived.append(player_name)

    def reduce_player_combo(self, player_name: str):
        if player_name in list(self.player_combo_table[NAME_FIELD]):
            self.player_combo_table.loc[
                self.player_combo_table.index[self.player_combo_table[NAME_FIELD] == player_name],
                COMBO_FIELD] //= 2
        else:
            raise RuntimeError("Can't reduce combo of nonexistent player")

    def find_players_to_remove_scores_from(self) -> List[str]:
        players_to_remove_scores_from = []
        for player_name in list(self.player_combo_table[NAME_FIELD]):
            if player_name not in self._players_who_arrived:
                players_to_remove_scores_from.append(player_name)
        return players_to_remove_scores_from

    def final_format_table(self):
        self.player_combo_table = self.player_combo_table.drop(self.player_combo_table.index[self.player_combo_table[
                                                                                                 COMBO_FIELD] == 0])
        self.player_combo_table = self.player_combo_table.sort_values(COMBO_FIELD, ascending=False, ignore_index=True)

    def export_table(self):
        self.player_combo_table.to_excel(os.path.join(self._default_table_dir,
                                                      datetime.datetime.now().strftime(TIME_FORMAT) +
                                                      '.xlsx'), index=False)


if __name__ == '__main__':
    names_list_str = input('אנא הכנס שמות הפסגותניקים שהגיעו היום והפרד בפסיקים:')
    names_list = [name for name in [name.strip() for name in names_list_str.split(',')] if name != '']
    game_manager = ComboGameManager()
    for name in names_list:
        game_manager.increase_player_combo(name)
    no_shows = game_manager.find_players_to_remove_scores_from()
    for name in no_shows:
        game_manager.reduce_player_combo(name)
    game_manager.final_format_table()
    game_manager.export_table()
