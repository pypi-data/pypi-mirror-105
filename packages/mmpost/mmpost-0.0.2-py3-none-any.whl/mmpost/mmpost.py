#!/usr/bin/env python3
import argparse
import sys

import caep


from typing import Text

from mattermostdriver import Driver


class Mattermost:
    """ Mattermost helper class """

    def __init__(
        self,
            token: Text,
            server: Text,
            port: int,
            team_name: Text,
            no_verify: bool = False,
            ) -> None:

        self.api = Driver({
            'url': server,
            'scheme': 'https',
            'token': token,
            'port': port,
            'basepath': '/api/v4',
            'verify': not no_verify,
            'timeout': 30,
            'request_timeout': 30,
        })

        self.team_name = team_name
        self.api.login()

    def get_channel_by_name(self, channel_name: Text):
        return self.api.channels.get_channel_by_name_and_team_name(
            self.team_name, channel_name)['id']

    def create_post(self, channel_name: Text, message: Text) -> None:
        channel_id = self.get_channel_by_name(channel_name)
        self.api.posts.create_post(options={
            'channel_id': channel_id,
            'message': message
        })




def parse_args() -> argparse.Namespace:
    """ Parse default arguments """
    parser = argparse.ArgumentParser(description="mmpost")

    parser.add_argument("--port", type=int, default=443, help="Server port")
    parser.add_argument("--server", help="Mattermost server")
    parser.add_argument("--team", help="Mattermost team")
    parser.add_argument("--channel", help="Mattermost channel to post to")
    parser.add_argument("--token", help="Mattermost token")
    parser.add_argument("--no-verify", action="store_true", help="Skip SSL-verify on Mattermost connection")
    parser.add_argument("--message", help="Message to post (read from stdin if not set)")

    args = caep.config.handle_args(parser, "mmpost", "config", "post")

    if not (args.server and args.team and args.channel and args.token):
        sys.stderr.write("server, team, channel and token must be specified\n")
        sys.exit(1)

    if not args.message:
        args.message = sys.stdin.read().strip()

        if not args.message:
            sys.stderr.write("No message on stdin\n")
            sys.exit(0)


    return args


def post() -> None:
    args = parse_args()

    api = Mattermost(args.token, args.server, args.port, args.team, args.no_verify)

    api.create_post(args.channel, args.message.strip())



if __name__ == "__main__":
    post()
