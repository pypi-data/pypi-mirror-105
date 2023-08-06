import os
import configparser

user_dir = os.path.expanduser("~")
cache_location = os.path.join( user_dir, '.config/rofify/rofi_spotify_token.cache')

class Config:
    """
    Class used for conveying configuration settings
    """
    def __init__(self):
        self._config = configparser.ConfigParser()
        config_dir = os.path.join(user_dir,'.config/rofify/config')
        if not self._config.read(config_dir):
            raise FileNotFoundError(f"Cannot find config file at {config_dir}")

    formatting_defaults = {
        'playlist-track-label':'<name><album><artists>',
        'search-track-label':'<name><artists><type>',
        'header-playback-label':'<isplaying><name><artists><shuffle><repeat>',
        'playlist-item-label':'<name><number_of_tracks>',
        'active-item-colour':'#1f782c',
    }

    icon_defaults = {
        'playlist-menu-icon':'蘿',
        'track-item-icon':'',
        'device-menu-icon':'',
        'recently-played-menu-icon':'',
        'saved-tracks-menu-icon':'',
        'search-tracks-menu-icon':'',
        'playlist-item-icon':'蘿',
    }

    state_defaults = {
        'shuffle-off':'劣',
        'shuffle-on':'列',

        'repeat-off':'稜',
        'repeat-context':'凌',
        'repeat-track':'綾',

        'playing':'Playing:',
        'paused':'Paused:',
        'nothing-playing':'Nothing Playing',
    }

    def get_format(self, option):
        return self._config.get(
            section="formatting",
            option=option,
            fallback=self.formatting_defaults.get(option)
        )

    def get_icon(self, option):
        return self._config.get(
            section="formatting",
            option=option,
            fallback=self.icon_defaults.get(option)
        )

    def get_state(self, option):
        return self._config.get(
            section="formatting",
            option=option,
            fallback=self.state_defaults.get(option),
        )

    def check_credentials(self, credential):
        if 'credentials' not in self._config.sections():
            raise KeyError(
        "The credentials section does not exist in the config file. username could not be retrieved"
        )
        else:
            creds = [self._config.get(section='credentials', option=cred, fallback="Not found")
            for cred in ['username','client_id','client_secret','redirect_uri']]

            err_string = f" \
                {credential} credential not found \n \
                settings parsed from the config file: \n \
                username:      {creds[0]}, \n \
                client_id:     {creds[1]}, \n \
                client_secret: {creds[2]}, \n \
                redirect_uri:  {creds[3]}"
            raise KeyError(err_string)

    @property
    def username(self):
        try:
            return self._config['credentials']['username']
        except KeyError:
            self.check_credentials('username')

    @property
    def client_id(self):
        try:
            return self._config['credentials']['client_id']
        except:
            self.check_credentials('client_id')
    
    @property
    def client_secret(self):
        try:
            return self._config['credentials']['client_secret']
        except:
            self.check_credentials('client_secret')

    @property
    def redirect_uri(self):
        try:
            return self._config['credentials']['redirect_uri']
        except:
            self.check_credentials('redirect_uri')


    def playlist_track_label(self, track):
        """
        Parse the config and return a string for the provided track,
        formatted according to the config
        for the playlist-track-label option.
        """

config = Config()

# get client width, prioritise environment variable
width = os.getenv("rofi_width")
if width is not None\
and width[1:].isnumeric():
    width = -int(width)

# then check config
elif config._config.get(section='formatting',option='formatting_width'):
    width = config._config['formatting']['formatting_width']

# Not much else to do than assume the defualt width of 90 characters
else:
    width = 90

# Dictionary for parsing the playlist features
playlist_features = {
    '<collaborative>'    : lambda x : "collaborative" if x['collaborative'] else "non-collaborative",
    '<description>'      : lambda x : x['description'],
    '<name>'             : lambda x : x['name'],
    '<owner_name>'       : lambda x : x['owner']['display_name'],
    '<public>'           : lambda x : "public" if x['public'] else "private",
    '<number_of_tracks>' : lambda x : str(x['tracks']['total']) + " tracks",
}

# used in order to traverse the track dictionary structure
track_directory = {
    '<album>'           : lambda x : x['album']['name'],
    '<artists>'         : lambda x : ', '.join([artist['name'] for artist in x['artists']]),
    '<disc_number>'     : lambda x : x['disc_number'],
    '<duration>'        : lambda x : "{:0.0f}:{:0.0f}".format(*divmod(x['duration_ms']/1000,60)),
    '<episode>'         : lambda x : str(x['episode']),
    '<name>'            : lambda x : x['name'],
    '<track_number>'    : lambda x : str(x['track_number']),
    '<type>'            : lambda x : x['type'],
}
