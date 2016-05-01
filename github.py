import hashlib
import json
from pprint import pprint

import requests
from flask import request
from flask.ext.restful import Resource, reqparse

from Payload import Ping, PullRequest, PullRequestComment, Issue, IssueComment, Repository, Branch, Push, Tag, CommitComment
from run import app, api

import hmac

SECRET = hmac.new(app.config['SECRET_KEY'], digestmod=hashlib.sha1) if app.config['SECRET_KEY'] else None


class GithubHook(Resource):
    def __init__(self):
        self.header_parser = reqparse.RequestParser()
        self.header_parser.add_argument('X-Hub-Signature', location='headers')
        self.header_parser.add_argument('X-GitHub-Delivery', location='headers')
        self.header_parser.add_argument('X-Github-Event', location='headers')

    def post(self):
        args = self.header_parser.parse_args()

        if SECRET:
            signature = request.headers.get('X-Hub-Signature', None)
            sig2 = SECRET.copy()
            sig2.update(request.data)

            if signature is None or sig2.hexdigest() != signature.split('=')[1]:
                return 'Invalid or missing X-Hub-Signature', 400

        data = request.get_json()
        event = request.headers['X-Github-Event']

        msg = ""
        if event == "ping":
            msg = Ping(data).ping()
        elif event == "pull_request":
            if data['action'] == "opened":
                msg = PullRequest(data).opened()
            elif data['action'] == "closed":
                msg = PullRequest(data).closed()
            elif data['action'] == "assigned":
                msg = PullRequest(data).assigned()
        elif event == "issues":
            if data['action'] == "opened":
                msg = Issue(data).opened()
            elif data['action'] == "closed":
                msg = Issue(data).closed()
            elif data['action'] == "labeled":
                msg = Issue(data).labeled()
            elif data['action'] == "assigned":
                msg = Issue(data).assigned()
        elif event == "issue_comment":
            if data['action'] == "created":
                msg = IssueComment(data).created()
        elif event == "repository":
            if data['action'] == "created":
                msg = Repository(data).created()
        elif event == "create":
            if data['ref_type'] == "branch":
                msg = Branch(data).created()
            elif data['ref_type'] == "tag":
                msg = Tag(data).created()
        elif event == "delete":
            if data['ref_type'] == "branch":
                msg = Branch(data).deleted()
        elif event == "pull_request_review_comment":
            if data['action'] == "created":
                msg = PullRequestComment(data).created()
        elif event == "push":
            if not (data['deleted'] and data['forced']):
                if not data['ref'].startswith("refs/tags/"):
                    msg = Push(data).commits()
        elif event == "commit_comment":
            if data['action'] == "created":
                msg = CommitComment(data).created()

        if msg:
            url, channel = get_hook_info(data)
            response = {}
            response['text'] = msg
            response['channel'] = channel
            response['username'] = app.config['GITHUB_BOT_USERNAME']
            response['icon_url'] = app.config['GITHUB_BOT_ICON_URL']

            pprint(response)

            headers = {'Content-Type': 'application/json'}
            r = requests.post(url, headers=headers, data=json.dumps(response), verify=False)

            if r.status_code is not requests.codes.ok:
                print 'Encountered error posting to Mattermost URL %s, status=%d, response_body=%s' % (
                url, r.status_code, r.json())
            return "Ok", 200
        else:
            return "Not implemented", 400


def get_hook_info(data):
    if 'repository' in data:
        repo = data['repository']['full_name']
        if repo in app.config['MATTERMOST_WEBHOOK_URLS']:
            return app.config['MATTERMOST_WEBHOOK_URLS'][repo]
    if 'organization' in data:
        org = data['organization']['login']
        if org in app.config['MATTERMOST_WEBHOOK_URLS']:
            return app.config['MATTERMOST_WEBHOOK_URLS'][org]
    return app.config['MATTERMOST_WEBHOOK_URLS']['default']


api.add_resource(GithubHook, '/git', endpoint='github_hook')
