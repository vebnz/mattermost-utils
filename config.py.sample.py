import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5090
    SECRET_KEY = '<something sekrit>'

    GIPHY_BOT_USERNAME = 'giphy'
    GIPHY_BOT_ICON_URL = 'giphy.png'
    GIPHY_BOT_RATING = 'pg'
    GIPHY_BOT_SCHEME = 'https'

    # giphy demo api key
    GIPHY_API_KEY = os.environ.get('GIPHY_API_KEY', 'dc6zaTOxFJmzC')

    MATTERMOST_GIPHY_TOKEN = ['<outgoing webhook token>', '<slash command token>']

    GITHUB_BOT_USERNAME = 'github'
    GITHUB_BOT_ICON_URL = 'https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png'

    MATTERMOST_WEBHOOK_URLS = {
        'default': ("<incoming webhook url>", "town-square"),
    }


config = {
    'default': DevelopmentConfig,
}
