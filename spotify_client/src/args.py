import argparse


"""
CLI arguments for Spotify Client.
"""


class Args:
    def __new__(cls, *args, **kwargs):
        """
        Portable and extensible class for CLI arguments.
        :param args:
        :param kwargs:
        """
        args = argparse.ArgumentParser('Spotify Client CLI commands')
        args.add_argument('--token', '-t', type=str, help="Authentication token")
        args.add_argument('--client_id', '-cid', type=str,
                          help='Spotify app client ID that can be created or found at'
                               'https://developer.spotify.com')
        args.add_argument('--client_secret',  '-cs', type=str,
                          help='Client secret that can be found with Client ID'
                               'in your app dashboard at https://developer.spotify.com')
        args.add_argument('--url', type=str, help='URL you are trying to reach')
        parser = args.parse_args()

        return parser
