import os
import librosa
import soundfile as sf
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import tensorflow as tf

DURACAO_GRAVACAO = 60  # Duração da gravação em segundos

print("Iniciando...")


def gravar_audio(duracao=DURACAO_GRAVACAO, taxa_amostragem=44100):
    print("Gravando áudio... Fale agora!")
    audio_gravado = sd.rec(int(duracao * taxa_amostragem), samplerate=taxa_amostragem, channels=2, dtype='float32')
    sd.wait()
    print("Gravação concluída!")
    return audio_gravado, taxa_amostragem

def dividir_audio_em_trechos(y, sr, duracao_trecho=5.0, diretorio_saida="trechos"):
    amostras_por_trecho = int(duracao_trecho * sr)
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
    trechos = []
    for i, inicio in enumerate(range(0, len(y), amostras_por_trecho)):
        fim = inicio + amostras_por_trecho
        trecho = y[inicio:fim]
        nome_trecho = os.path.join(diretorio_saida, f"trecho_{i}.wav")
        sf.write(nome_trecho, trecho, sr)
        trechos.append(nome_trecho)
    return trechos

def extract_spectrograms(file_path, output_dir):
    y, sr = librosa.load(file_path, sr=None)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Espectrograma de {os.path.basename(file_path)}')
    plt.tight_layout()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_filename = os.path.join(output_dir, f"extracaoEspec{os.path.splitext(os.path.basename(file_path))[0]}.png")
    plt.savefig(output_filename)
    plt.close()

def carregar_transformada_fourier_direto(diretorio):
    transformadas = []
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.png'):
            imagem_path = os.path.join(diretorio, arquivo)
            try:
                imagem = tf.keras.preprocessing.image.load_img(imagem_path, target_size=(200, 500))
                imagem = tf.keras.preprocessing.image.img_to_array(imagem) / 255.0  # Normalização
                transformadas.append(imagem)
            except Exception as e:
                print(f"Erro ao carregar o arquivo {arquivo}: {e}")
    return np.array(transformadas)

def main(output_segments_dir, output_spectrograms_dir):
    # Gravação do áudio
    y, sr = gravar_audio()
    segmentos = dividir_audio_em_trechos(y, sr, diretorio_saida=output_segments_dir)
    for segmento in segmentos:
        extract_spectrograms(segmento, output_spectrograms_dir)

# Carregar o modelo CNN
model = tf.keras.models.load_model('/home/machine/code/EmissorReceptor/meu_modelo.h5')

output_segments_dir = '/home/machine/code/EmissorReceptor/trechos'
output_spectrograms_dir = '/home/machine/code/EmissorReceptor/espectogramas'

main(output_segments_dir, output_spectrograms_dir)

espectrogramas_capturados = carregar_transformada_fourier_direto(output_spectrograms_dir)
if espectrogramas_capturados.size == 0:
    print("Nenhum espectrograma foi carregado. Verifique o diretório e os arquivos.")
    exit()

rotulos_preditos_capturados = np.argmax(model.predict(espectrogramas_capturados), axis=-1)
frequencias = ["10kHz", "1kHz", "5kHz"]
frequencias_preditas_capturados = [frequencias[idx] for idx in rotulos_preditos_capturados]
print("Frequências detectadas nos espectrogramas capturados:", frequencias_preditas_capturados)