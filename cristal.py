from gtts import gTTS
import speech_recognition as sr
import os
from playsound import playsound # WINDOWS
# from subprocess import call # MAC / LINU
import requests
from bs4 import BeautifulSoup
import re
import webbrowser as browser
import json

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
    
    elif 'fechar' and 'assistente' in trigger:
        fechar_assistente()
    
    elif ('dividir' in trigger or 'divide' in trigger or 'dividido' in trigger or '/' in trigger ):
        numeros = filtrar_numeros(trigger)
        calculo = Calculadora(numeros[0],numeros[1])
        calculo.dividir()
        
    elif ('multiplica' in trigger or 'multiplicado' in trigger or 'vezes' in trigger or '*' in trigger ):
        numeros = filtrar_numeros(trigger)
        calculo = Calculadora(numeros[0],numeros[1])
        calculo.multiplicar()
       
    elif ('subitrai' in trigger or 'subtrai' in trigger or '-' in trigger or 'menos' in trigger ):
        numeros = filtrar_numeros(trigger)
        calculo = Calculadora(numeros[0],numeros[1])
        calculo.subtrair()
    
    elif ('soma' in trigger or 'mais' in trigger or "+" in trigger):
        numeros = filtrar_numeros(trigger)
        calculo = Calculadora(numeros[0],numeros[1])
        calculo.somar()
        
    elif ('toca' and 'rock' in trigger ):
        playlist('rock') 
           
    elif ('tocar' and 'sertanejo universitário' in trigger):
        playlist('sertanejo_universitario')

    elif ('previsão do tempo' in trigger):
        previsao_do_tempo(previsao=True)
    
    elif ('temperatura' and 'agora' in trigger):
        previsao_do_tempo(tempo=True)
    
    elif ('temperatura' and 'hoje' in trigger):
        previsao_do_tempo(min_max=True)
    
        
    else:
        try:
            comando_invalido(trigger)
        except:
            print("erro") 


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
    responde('erro')
      


def filtrar_numeros(mensagem):
    msg = mensagem
    msg = re.sub('[^0-9]', ' ', msg)
    msg_filtrada = msg.split()
    print(msg_filtrada)
    
    return msg_filtrada

def playlist(album):
    if (album == 'rock'):
        browser.open('https://www.youtube.com/watch?v=kXYiU_JCYtU&list=PL6Lt9p1lIRZ311J9ZHuzkR5A3xesae2pk')
    if (album == 'sertanejo_universitario'):
        browser.open('https://www.youtube.com/watch?v=rTJSWmgbVwA&list=PL3oW2tjiIxvRrvtGzZmaH6eK1QqAJKeTi')


def previsao_do_tempo(tempo=False, min_max=False, previsao=False):
    site = requests.get('https://api.openweathermap.org/data/2.5/weather?id=3464374&appid=e1417d56b463423faa6f26d73c86f61d&lang=pt_br&units=metric')
    clima = site.json()
    
    temperatura = int(clima['main']['temp'])
    temperatura_minima = int(clima['main']['temp_min'])
    temperatura_maxima = int(clima['main']['temp_max'])
    descricao = clima['weather'][0]['description']
    
    if (tempo):
        cria_audio_e_responde(f'A temperatura atual de sua cidade é de {temperatura} graus')
    elif(min_max):
        cria_audio_e_responde(f'A temperatura mínima da sua cidade é de {temperatura_minima} e a máxima é de {temperatura_maxima} graus')
    elif(previsao):
        cria_audio_e_responde(f'A temperatura na sua cidade é de {temperatura} graus, a temperatura mínima é de {temperatura_minima} graus e a máxima é de {temperatura_maxima} graus e o céu está {descricao}')
    
class Calculadora:
    def __init__(self, numero_um, numero_dois):
        self.numero_um = int(numero_um)
        self.numero_dois = int(numero_dois)
    
    def somar(self):
        resultado =  self.numero_um + self.numero_dois
        print(resultado)
        cria_audio_e_responde(f'{self.numero_um} mais {self.numero_dois} é igual a {resultado}')
    
    def subtrair(self):
        resultado =  self.numero_um - self.numero_dois
        cria_audio_e_responde(f'{self.numero_um} menos {self.numero_dois} é igual a {resultado}')
    
    def dividir(self):
        resultado =  self.numero_um / self.numero_dois
        cria_audio_e_responde(f'{self.numero_um} dividido por {self.numero_dois} é igual a {resultado}')
        
    def multiplicar(self):
        resultado =  self.numero_um * self.numero_dois
        cria_audio_e_responde(f'{self.numero_um} vezes {self.numero_dois} é igual a {resultado}')
        
  
    
def cria_audio_e_responde(mensagem):
    
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('audios/msg.mp3')
    print(f"Cristal: {mensagem}")
    playsound(f'{pega_url()}/audios/msg.mp3')
    os.remove(f'{pega_url()}/audios/msg.mp3')

    
    
def main():
    while True:
        monitora_audio()

main()
