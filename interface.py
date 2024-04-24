import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import subprocess
import threading

def execute_script(script_name):
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True, check=True)
        log_text.insert(tk.END, result.stdout)
        if result.stderr:
            log_text.insert(tk.END, result.stderr)
        log_text.see(tk.END)
        return True
    except subprocess.CalledProcessError as e:
        log_text.insert(tk.END, f"Erro ao executar {script_name}:\n{e.stdout}\n{e.stderr}\n")
        log_text.see(tk.END)
        return False

def emissor():
    threading.Thread(target=execute_script, args=('emissor.py',)).start()

def receptor():
    def run_and_show_image():
        print('receptor.py')
        if execute_script('receptor.py'):
            show_image('/home/machine/EmissorReceptor/espectogramas/extracaoEspectrecho_0.png')
    threading.Thread(target=run_and_show_image).start()

def show_image(image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    
    img_label = tk.Label(root, image=photo)
    img_label.image = photo 
    img_label.pack(pady=20)

root = tk.Tk()
root.title("DETECTOR DE FREQUENCIA")

btn_emissor = tk.Button(root, text="Emissor", command=emissor)
btn_emissor.pack(pady=20)
btn_receptor = tk.Button(root, text="Receptor", command=receptor)
btn_receptor.pack(pady=20)

log_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)
log_text.pack(pady=20)

root.mainloop()
