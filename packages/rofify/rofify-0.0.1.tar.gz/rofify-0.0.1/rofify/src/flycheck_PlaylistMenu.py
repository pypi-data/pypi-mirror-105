from rofi_menu import NestedMenu, Menu, Operation, constants, BackItem
from rofify.src.DynamicNestedMenu import DynamicNestedMenu
from rofify.src.TrackMenu import TrackMenu
from rofify.src.SpotifyAPI import spotify
from rofify.src.config import config, playlist_features
from rofify.src.utils import truncate, substitute_pango_escape, width
import re

def playlist_item_label(playlist, config):
    """
    Parse the config and return a string representing a playlist,
    formmated according to the user entry in the config.
    """
    active_playlist = lambda x: \
        "<span foreground='{}'>".format(
            config.get_format('active-item-colour'))\
        + str(x) + " (playing)</span>"

    structure = config.get_format('playlist-item-label')
    playlist_feature_pattern = re.compile("(" + "|".join(playlist_features.keys()) + ")")
    matches = re.findall(playlist_feature_pattern, structure)
    playlist_label = config.get_icon('playlist-item-icon') + " "
    for index,match in enumerate(matches):
        field_text = playlist_features.get(match)(playlist) if playlist_features.get(match) else ''
        margin = 0 if index+1 == len(matches) else 2
        playlist_label += substitute_pango_escape(
            truncate(field_text, (width-1)//len(matches)-3, margin)
        )

    return playlist_label

class PlaylistMenu(Menu):
    """
    Menu the provides the user the option to select from their playlists.
    Should be accessible from the main menu.
    """

    def __init__(self, prompt=None):
        super().__init__()
        self.prompt="Playlists"

    async def generate_menu_items(self,meta):
        """ All playlists from the current user as nested menus
        """
        nested_playlist_menus = [BackItem()]
        for playlist in (await spotify.async_all_playlists()):
            nested_playlist_menus.append(
                DynamicNestedMenu(
                    sub_menu_type=TrackMenu.from_playlist,
                    playlist=playlist,
                    text=playlist_item_label(playlist,config),
                )
            )
        return nested_playlist_menus
