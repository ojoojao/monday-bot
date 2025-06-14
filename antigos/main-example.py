import time

from voice_reader import pySimpleVoiceRecognition
from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics

oauth = OAuth()

while True:    

    oauth.credentials("credentials.json")
    client_id = oauth.client_id

    oauth.access_token("token.json")
    token = oauth.token

    user_info = Basics.Get_Users(client_id, token, ['pokimane'])
    broadcaster_id = user_info[0]["id"]
    sender_id = "459116718"
    
    print("::getting user id")

    print("::main while")
    
    init_voice_time = time.time()
    while True:
    
        print("::voice while")
    
        # Read voice
        rec = pySimpleVoiceRecognition.rec()
    
        print("::rec")

        # Ver como esta saindo a leitura do lucas para melhorar a chamada
        calling = pySimpleVoiceRecognition.assitent_call()

        new_voice_time = time.time()
        if (new_voice_time - init_voice_time) > 3600:
            oauth.credentials("credentials.json")
            client_id = oauth.client_id

            oauth.access_token("token.json")
            token = oauth.token

        if calling:
            Basics.Send_Chat_Message(client_id, token, broadcaster_id, sender_id, "Oi, me chamou?")

            rec = pySimpleVoiceRecognition.rec()
    
            print("::rec")
    
            # Get response
            result = pySimpleVoiceRecognition.action()

            # Break loop
            if result == True:
                msg = "Make a clip"     
                break
            else:
                Basics.Send_Chat_Message(client_id, token, broadcaster_id, sender_id, 
                                         "Tá querendo um clipe e não ta sabendo pedir")

    Basics.Send_Chat_Message(client_id, token, broadcaster_id, sender_id, "Criando clipe...")
    
    print("Criando clipe...")

    # Talvez botar um delay
    created_clip_info = Basics.Create_Clip(client_id, token, broadcaster_id)
    clip_id = created_clip_info["id"]

    clip_info = []
    init_clip_time = time.time()
    while len(clip_info) <= 0:
        clip_info = Basics.Get_Clip(client_id, token, clip_id)
        
        new_clip_time = time.time()

        if (new_clip_time - init_clip_time) > 15:
            Basics.Send_Chat_Message(client_id, token, broadcaster_id, sender_id, 
                                     "Não foi possivel criar o clipe...")
    
            print("Não foi possivel criar o clipe...")
    
            break

    if (new_clip_time - init_clip_time) < 15:
        Basics.Send_Chat_Message(client_id, token, broadcaster_id, sender_id, clip_info[0]["url"])
    
        print(clip_info[0]["url"])

    # Danny Jones me descobriu
    # https://www.twitch.tv/dannyjones/clip/CourageousSpookyFriseeTheTarFu-qCyokS5h_4KsNCDq