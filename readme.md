Hello Highspot,

This console application accepts three arguments. 
batch.py \<input file name> \<change file name> \<output file name>

It is written on python 3.7 and uses json and sys packages which are parts of the python 3 standard library, so you shouldn't have to manually install them.

---

## Change File
Changes to the mixtape.json need to be in JSON format. For each playlist, it needs to have an action and approporiate identifiers.

The actions are add and delete.

#### To add one or more exisitng songs to an existing playlist:

{
    "playlists": [
        {
            "id": "3",
            "action": "add",
            "song_ids": [
                "1",
                "2"
            ]
        }
    ]
}

* You have to provide only the song you want to add to the playlist. This is a patch operation, so you do not need to know the full list of songs for the playlist.
* If the playlist id or the song id do not match, then it will not add that playlist/song.
* If the song is already in the playlist, it will adds the song again. (assuming the user wants to hear the song more often).

#### To add a new playlist for an existing user 
batch.py will check that the playlist contains at least one existing song.

{
    "playlists": [
        {
            "id": "",
            "user_id": "5", 
            "action": "add",
            "song_ids": [
                "1",
                "2"
            ]
        }
    ]
}

* playlist id should be blank, action should be "add".
* if the change file contains song that doesn't exists, it will not insert those songs into the playlist.

#### To remove an existing playlist.

{
    "playlists": [
        {
            "id": "3", 
            "action": "delete"
        }
    ]
}

* action should be "delete"

---


## Scaling

If the input file or change file are very large, there can be several approaches to alleviate the problem.

1. Instead of parsing and matching the JSON files in memory, you can flatten the JSON and store it in a relational database. If you were to have one property per column and added indexes, you should be able to dramatically speed up the processing. 

2. The easiest way would probably be just to order up a bigger virtual box (if you are running in AWS or other services) and the batch.py. 

3. I learned Python while taking data science class, and usually work with pandas dataframes in order to work with large sets of data. Pandas supports JSON normalizing and loading to dataframes. Something like this: 

    ``` df = json_normalize(inputs['playlists']) ```

    You can the use dataframe to match and process the JSON data which should be faster.
