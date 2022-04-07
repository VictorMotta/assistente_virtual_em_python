from gtts import gTTS
import speech_recognition as sr
import os
from playsound import playsound # WINDOWS
# from subprocess import call # MAC / LINU
import requests
from bs4 import BeautifulSoup

##### CONFIGURAÇÕES #####
hotword = 'cristal'
with open('cristal-assistent-fc8228478e8a.json') as credenciais_google:
    credenciais_google = credenciais_google.read()

##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
        
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
                trigger = trigger.lower()
                
                if hotword in trigger:
                    print('Comando: {}'.format(trigger))   
                    responde('feedback')  
                    executa_comandos(trigger)
                    break      
                    
            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    
    return trigger

def pega_url():
    origem = os.getcwd().replace("\\","/")
    return origem

def responde(arquivo):
    playsound(f'{pega_url()}/audios/{arquivo}.mp3')
    # call(['afplay', 'audios/hello.mp3']) # OSX
    # call(['aplay', 'audios/bem_vindo.mp3']) # LINUX 
 
    
def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    if 'fechar' and 'assistente' in trigger:
        fechar_assistente()
    else:
        comando_invalido(trigger)


def ultimas_noticias():
    site = requests.get ("https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419")
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:2]:
        mensagem = item.title.text + ".\n"
        cria_audio_e_responde(mensagem)
        


def fechar_assistente():
    print('Encerrando...')
    responde('fechar')
    exit()
    
def comando_invalido(trigger):
    mensagem = trigger.strip(hotword)
    cria_audio_e_responde(mensagem)
    print('Comando Inválido', mensagem)
    responde('erro_comando')
      
def cria_audio_e_responde(mensagem):
    
    tts = gTTS(mensagem, lang='pt-br')
    tts.save(f'audios/mensagem.mp3')
    print(f"Cristal: {mensagem}")
    playsound(f'{pega_url()}/audios/mensagem.mp3')


    
def main():
    while True:
        monitora_audio()

main()