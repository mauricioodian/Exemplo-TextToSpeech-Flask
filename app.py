from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk

# Carregar as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configurações do Serviço de Fala do Azure
speech_key = os.getenv('SPEECH_KEY')
speech_region = os.getenv('SPEECH_REGION')
speech_voice = 'pt-BR-AntonioNeural'


def speech(texto):

    # Define configuracoes de chave e regiao da aplicacao
    # Também define a linguagem e voz de fala
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name=speech_voice

    # Aplica configuracoes definidas
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Inicializa processo de fala do texto
    speech_synthesis_result = speech_synthesizer.speak_text_async(texto).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Texto sintetizado [{}]".format(texto))
        message = "Texto sintetizado com sucesso!"

    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Sintese de fala cancelada: {}".format(cancellation_details.reason))
        message = "Sintese de fala cancelada!!! Detalhes: {}".format(cancellation_details.reason)
        
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Detalhes do Erro: {}".format(cancellation_details.error_details))
                print("Você definiu os valores da chave e da região do recurso de fala?")
                message = "Erro ao sintetizar texto!!! Detalhes: {}".format(cancellation_details.error_details)

    return message


# --------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exemplo')
def exemplo():
    return render_template('exemplo.html')


# Função que inicia 
@app.route('/start_speech', methods=['POST'])
def start_speech():
    dados = request.get_json()
    texto = dados.get('texto', '')
    
    message = speech(texto)
    print(f"Mensagem: {message}")
    print("---------------------------------------------------")
    return jsonify({'message': message})


if __name__ == '__main__':
    app.run()

