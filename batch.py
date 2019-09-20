import json
import sys

with open(sys.argv[1], 'r') as f1:
    inputs = json.load(f1)

with open(sys.argv[2], 'r') as f2:
    changes = json.load(f2)

# converts playlist, users, and songs to dictionary for easy look ups
mixtape_dict = {item['id']: item for item in inputs['playlists']}
users_dict = {item['id']: item for item in inputs['users']}
songs_dict = {item['id']: item for item in inputs['songs']}

# maxkey for adding new playlist
maxkey = max(int(k) for k in mixtape_dict)

for change in changes['playlists']:
    # Playlist ids match
    if mixtape_dict.get(change['id']) and change.get('id') != '':

        # Remove an existing playlist
        if change.get('action') == 'delete':
            del mixtape_dict[change.get('id')]

        # Add an existing song to an existing playlist
        if change.get('action') == 'add':
            for song in change.get('song_ids'):
                if songs_dict.get(song):
                    mixtape_dict[change['id']]['song_ids'].extend(song)

    # Add a new playlist for an existing user
    # the playlist should contain at least one existing song.
    elif change.get('action') == 'add' and change.get('id') == '':

        # Existing user
        if users_dict.get(change.get('user_id')):
            existingSongs = []
            for song in change.get('song_ids'):
                if songs_dict.get(song):
                    existingSongs.append(song)

            # playlist should contain at least one existing song
            if existingSongs != []:
                change['song_ids'] = existingSongs
                # Remove the action when adding a new playlist
                del change['action']
                maxkey = maxkey + 1
                change['id'] = maxkey
                mixtape_dict[maxkey] = change

outlist = []

# Convert the dictionary back to list
for key, value in mixtape_dict.items():
    outlist.append(value.copy())

# replace playlist with the modified list
inputs['playlists'] = outlist

with open(sys.argv[3], 'w') as f3:
    json.dump(inputs, f3, indent=4)
