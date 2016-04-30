import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5000
    SECRET_KEY = 'XNV1Hm5zvOrFvEST0A0fb8972v+yIrnRR27V~3*+DG4y48`H1I,o;;tm[6>PACu'

    GIPHY_BOT_USERNAME = 'giphy'
    GIPHY_BOT_ICON_URL = 'https://api.giphy.com/img/api_giphy_logo.png'
    GIPHY_BOT_RATING = 'pg'
    GIPHY_BOT_SCHEME = 'https'

    GIPHY_API_KEY = os.environ.get('GIPHY_API_KEY', 'dc6zaTOxFJmzC')

    MATTERMOST_GIPHY_TOKEN = os.environ.get('MATTERMOST_GIPHY_TOKEN', '3igxjdom5pgdbfqz6it8z4yr5h')


config = {
    'default': DevelopmentConfig,
}
