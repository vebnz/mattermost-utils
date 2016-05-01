import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5090
    SECRET_KEY = 'XNV1Hm5zvOrFvEST0A0fb8972v+yIrnRR27V~3*+DG4y48`H1I,o;;tm[6>PACu'

    GIPHY_BOT_USERNAME = 'giphy'
    GIPHY_BOT_ICON_URL = 'giphy.png'
    GIPHY_BOT_RATING = 'pg'
    GIPHY_BOT_SCHEME = 'https'

    GIPHY_API_KEY = os.environ.get('GIPHY_API_KEY', 'dc6zaTOxFJmzC')

    MATTERMOST_GIPHY_TOKEN = ['1iih9fzu3p88pmhka4hctdtnjh', 'i5tyfc316pdfjmawbcpk3wt1or']

    GITHUB_BOT_USERNAME = 'github'
    GITHUB_BOT_ICON_URL = 'https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png'

    MATTERMOST_WEBHOOK_URLS = {
        'default': ("http://actualbrain.com:8065/hooks/ej8jcebawtbwtecpoe6kqzywja", "town-square"),
    }


config = {
    'default': DevelopmentConfig,
}
