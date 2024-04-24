import numpy as np
import sounddevice as sd
import time
import random

DURACAO_SINAL = 10.0  
FREQUENCIAS = [5000] 
TAXA_AMOSTRAGEM = 44100 
TEMPO_TOTAL = 90.0  

def gera_senoide(frequencia, duracao=DURACAO_SINAL, taxa_amostragem=TAXA_AMOSTRAGEM):
    t = np.linspace(0, duracao, int(taxa_amostragem * duracao), endpoint=False)
    return np.sin(2 * np.pi * frequencia * t)

def toca_aleatoriamente():
    frequencias_tocadas = []
    inicio = time.time()
    while time.time() - inicio < TEMPO_TOTAL:
        freq = random.choice(FREQUENCIAS)
        frequencias_tocadas.append(freq)
        sinal = gera_senoide(freq)
        sd.play(sinal, samplerate=TAXA_AMOSTRAGEM)
        time.sleep(DURACAO_SINAL)
    return frequencias_tocadas

if __name__ == "__main__":
    frequencias = toca_aleatoriamente()
    print("Frequências tocadas em ordem:")
    for freq in frequencias:
        print(f"{freq} Hz")
