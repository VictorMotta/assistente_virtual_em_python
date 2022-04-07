from gtts import gTTS
import os 
# from subprocess import call # MAC / LINUX
from playsound import playsound # WINDOWS

def pega_url():
    origem = os.getcwd().replace("\\","/")
    return origem

def cria_audio(audio):
    
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/bem_vindo.mp3')
    
    # call(['afplay', 'audios/hello.mp3']) # OSX
    # call(['aplay', 'audios/bem_vindo.mp3']) # LINUX 
    playsound(f'{pega_url()}/audios/bem_vindo.mp3')
    
cria_audio('Oi, eu sou a cristal, seja bem vindo!')