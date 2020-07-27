# -*- coding: utf-8 -*-



import os
from os import path
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from oauth2client import file, client, tools
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

scopes = ["https://www.googleapis.com/auth/youtube.readonly","https://www.googleapis.com/auth/youtube.force-ssl"]
nomPlaylist = "ToDownload"
def fichierVideo(): # on creer le dossier video
    if os.path.isdir('./video') == False: # si il n existe pas de dossier video on le cree
        os.system("mkdir video")
def fileServer():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
    authorizer.add_anonymous("./video")

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 2121)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    store = file.Storage('credentials.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secrets_file, scopes)
        credentials = tools.run_flow(flow, store)

    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=99,
        mine=True
    )
    response = request.execute()
    response = response.get("items")
    for truc in response:
        if truc["snippet"]["title"] == nomPlaylist:
            print(truc["snippet"]["title"])
            print(truc["id"])
            requestvideo = youtube.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=9999,
                playlistId=truc["id"]
            )
            responsevideo = requestvideo.execute()
            responsevideo = responsevideo.get("items")
            for video in responsevideo: # pour chaque video dans la playlist
                
                # on télécharge la video 
                os.system("youtube-dl  --ignore-config -o ./video/"+"'"+video["snippet"]["title"]+"'"+".mp4 " + "https://youtu.be/" + video["snippet"]["resourceId"]["videoId"]) 
                # puis on la supprime de la playlist
                requestdelete = youtube.playlistItems().delete(
                    id=video["id"]
                )
                requestdelete.execute()
            
            
    #print(response.get("title"))

if __name__ == "__main__":
    fichierVideo()
    main()
    #fileServer()
