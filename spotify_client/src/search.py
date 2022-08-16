from authenticate import CreateAuthorization, GetToken
from args import Args
from lists import playlists

import json
import requests
from datetime import datetime, timedelta


class AuthHeader:
    def __new__(cls, auth_token=None):
        header = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        return header


class SearchPlaylist:
    def __new__(cls, header=None, search_query=None):
        list_of_playlists = list()
        for item in playlists:
            url = f"https://api.spotify.com/v1/search?type=playlist&q={item}"
            search = requests.get(url=url, headers=header)

            response = search.json()
            playlist_details = response.get('playlists').get('items')
            list_of_playlists.append(playlist_details)
        results = json.dumps(list_of_playlists, indent=4)
        # print(results)
        return results


class ParsePlaylistUrls:
    def __new__(cls, header=None, playlist_results=None):
        jsonify = json.loads(playlist_results)[0]
        playlist_urls = []
        for item in jsonify:
            playlist_urls.append(item.get('href'))
        return playlist_urls


class SearchTracks:
    def __new__(cls, playlist_urls=None, header=None):
        """
        Function checks tracks within a playlist and checks if each track was added
        within 90 days. If The playlist contains tracks added within 90 days then it
        gets appended to a list.

        :param playlist_urls:
        :param header: authentication header
        """
        playlist_added = list()
        for playlist in playlist_urls:
            results = requests.get(playlist, headers=header)
            playlist_tracks = results.json()
            playlist_name = playlist_tracks.get('name')
            tracks = json.dumps(playlist_tracks.get('tracks', {}).get('items', {}), indent=4)
            updated_tracks_in_playlist = []
            for track in json.loads(tracks):
                # playlist_name = track.get('track').get('album').get('name')
                artist_name = track.get('track').get('album').get('artists')[0].get('name')
                track_name = track.get('track').get('name')
                added_at = track.get('added_at')
                added_date = added_at.split('T')[0]
                difference_date = datetime.today() - timedelta(days=90)
                updated_track_date = DateComparison(result_date=added_date)
                if difference_date < updated_track_date:
                    updated_tracks_in_playlist.append({"track": [added_date, track_name, artist_name]},)
                    # print(playlist_name, added_date, track_name, artist_name)
                    # playlist_added.append({"track": [added_date, track_name, artist_name]},)

            if updated_tracks_in_playlist:
                playlist_added.append({"playlist_name": playlist_name})

        return playlist_added


class DateComparison:
    def __new__(cls, result_date=None):
        input_date_time = datetime.strptime(result_date, "%Y-%m-%d")
        return input_date_time


def main():
    client_id = Args().client_id
    client_secret = Args().client_secret
    authorization_token = CreateAuthorization(client_id=client_id,
                                              client_secret=client_secret)
    auth_token = GetToken(encoded_token=authorization_token)
    header = AuthHeader(auth_token=auth_token)
    playlist_results = SearchPlaylist(header=header)
    playlist_urls = ParsePlaylistUrls(header=header, playlist_results=playlist_results)
    search_tracks = SearchTracks(playlist_urls=playlist_urls, header=header)
    print(json.dumps(search_tracks, indent=4))


if __name__ == '__main__':
    main()
