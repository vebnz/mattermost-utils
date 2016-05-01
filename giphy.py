from pprint import pprint
from urlparse import urlsplit
from urlparse import urlunsplit

import requests
import logging

from flask import url_for
from flask.ext.restful import Resource, reqparse

from run import app, api


@app.route('/')
def root():
    return 'OK'


def giphy_translate(text):
    """
    Giphy translate method, uses the Giphy API to find an appropriate gif url
    """
    try:
        params = {}
        params['s'] = text
        params['rating'] = app.config['GIPHY_BOT_RATING']
        params['api_key'] = app.config['GIPHY_API_KEY']

        resp = requests.get('{}://api.giphy.com/v1/gifs/translate'.format(app.config['GIPHY_BOT_SCHEME']), params=params, verify=True)

        if resp.status_code is not requests.codes.ok:
            logging.error('Encountered error using Giphy API, text=%s, status=%d, response_body=%s' % (
            text, resp.status_code, resp.json()))
            return None

        resp_data = resp.json()

        url = list(urlsplit(resp_data['data']['images']['original']['url']))
        url[0] = app.config['GIPHY_BOT_SCHEME'].lower()

        return urlunsplit(url)
    except Exception as err:
        logging.error('unable to translate giphy :: {}'.format(err))
        return None


class NewGiphyPost(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token')
        self.parser.add_argument('text')
        self.parser.add_argument('trigger_word', required=False)
        self.parser.add_argument('command', required=False)

    def post(self):
        try:
            slash_command = False
            response = {}
            response['username'] = app.config['GIPHY_BOT_USERNAME']
            response['icon_url'] = url_for('static', filename=app.config['GIPHY_BOT_ICON_URL'], _external=True)

            args = self.parser.parse_args()

            if args['token'] not in app.config['MATTERMOST_GIPHY_TOKEN']:
                raise Exception(
                    'Tokens did not match, it is possible that this request came from somewhere other than Mattermost')

            if args['command']:
                slash_command = True
                response['response_type'] = 'in_channel'

            translate_text = args['text']
            if not slash_command:
                translate_text = args['text'][len(args['trigger_word']):]

            gif_url = giphy_translate(translate_text)
            if not gif_url:
                raise Exception('No gif url found for `{}`'.format(translate_text))

            response['text'] = gif_url

        except Exception as err:
            msg = err.message
            logging.error('unable to handle new post :: {}'.format(msg))
            response['text'] = msg

        finally:
            return response, 200


api.add_resource(NewGiphyPost, '/new_post', endpoint='new_giphy_post')
