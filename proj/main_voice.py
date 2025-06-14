import time
from playsound import playsound
from random import randint

from vosk_transcrib import Transcrib
from mytwitchapi.creds_flow import OAuth
from mytwitchapi.twich_api_client import Basics

len_chatters = 0
oauth = OAuth()
tc = Transcrib()

while True:  
    oauth.credentials("credentials.json")
    client_id = oauth.client_id

    oauth.access_token("token.json")
    token = oauth.token
    scopes = oauth.scopes

    api = Basics(client_id, token, scopes)
    
    user_info = api.Get_Users(['ASegundaFeira'])
    mod_id = user_info[0]["id"]
    broadcaster_id = "459116718"
        
    make_clip = False
    calling = False
    sent_oi = [{"is_sent" : False}]
    sent_clip = [{"is_sent" : False}]
    cred_time = time.time()
    while True:
        # Read voice
        tc.listen_bigbrain()
        pvd = tc.partial

        if not calling:
            #if not calling:
            if ("segunda" in pvd["partial"]['list'][1] and
                "feira" in pvd["partial"]['list'][1]):
                print(pvd["partial"]['str'])
                calling = True
                tc.reset()
            calling_time = time.time()

        #if (time.time() - cred_time) > 3600:
        #    oauth.credentials("credentials.json")
        #    client_id = oauth.client_id
        #
        #    oauth.access_token("token.json")
        #    token = oauth.token

        if calling:
            if not sent_oi[0]["is_sent"]:
                sent_oi = api.Send_Chat_Message(broadcaster_id, mod_id, 
                                        "Oi, me chamou?")
                n = randint(1, 2)
                playsound(f'./audios/chamou_{n}.mp3')
                
            if ("faça" in tc.text["text"]['list'][1] or
                "faz" in tc.text["text"]['list'][1]): 
                
                if ("clipe" in tc.text["text"]['list'][1]):
                    print(tc.text["text"]['str'])

                    make_clip = True
                    tc.reset()
                    calling = False    
                    break
                    
                else:       
                    if not sent_clip[0]["is_sent"]:
                        sent_clip = api.Send_Chat_Message(broadcaster_id, mod_id, 
                                                "Tá querendo um clipe e não ta sabendo pedir") 
                        n = randint(1, 3)
                        playsound(f'./audios/pedido_{n}.mp3')
                        

            if (("esquece" in tc.text["text"]['list'][1]) or 
                ("deixa" in tc.text["text"]['list'][1] and 
                 "pra" in tc.text["text"]['list'][1] and 
                 "lá" in tc.text["text"]['list'][1])):
                print(tc.text["text"]['str'])

                api.Send_Chat_Message(broadcaster_id, mod_id, 
                                        "Ok. Já esqueci...")
                n = randint(1, 4)
                playsound(f'./audios/esqueca_{n}.mp3')
                make_clip = False
                calling = False
                break 
    
        if (time.time() - cred_time) > 60:
                make_clip = False
                calling = False
                break        

    if make_clip:            
        api.Send_Chat_Message(broadcaster_id, mod_id, 
                                "Criando clipe...")
        playsound(f'./audios/criando_1.mp3')

        # Talvez botar um delay
        created_clip_info = api.Create_Clip(broadcaster_id)
        clip_id = created_clip_info[0]["id"]

        clip_info = []
        init_clip_time = time.time()
        while len(clip_info) <= 0:
            clip_info = api.Get_Clip(clip_id)
            
            new_clip_time = time.time()

            if (new_clip_time - init_clip_time) > 15:
                api.Send_Chat_Message(broadcaster_id, mod_id, 
                                        "Não foi possivel criar o clipe...")
                playsound(f'./audios/impossivel_1.mp3', True)
                break

        if (new_clip_time - init_clip_time) < 15:
            api.Send_Chat_Message(broadcaster_id, mod_id, 
                                    clip_info[0]["url"])
            playsound(f'./audios/pronto_1.mp3')
        
            print(clip_info[0]["url"])

    # Danny Jones me descobriu
    # https://www.twitch.tv/dannyjones/clip/CourageousSpookyFriseeTheTarFu-qCyokS5h_4KsNCDq