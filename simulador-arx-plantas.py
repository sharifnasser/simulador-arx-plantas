import tkinter as tk
import threading 
import matplotlib.pyplot as plt
import math

# Global Variables
GRAPOINTS = 30
# Primer Orden
gananciaK = 0.0
tiempoTau = 0.0
tiempoTheta = 0.0
periodoT = 0.0
# Variables para calculos
d = 0
aux = 0.0
m = 0.0
# Arreglos importantes
A = [0.0 for _ in range(4)]
B = [0.0 for _ in range(5)]
M = []
C = [0.0 for _ in range(5)]
archivoEntrada = ""
Mo = []
Po = [0.0, 0.0]
punto = 0

# Entradas Tkinter
entradaPrimerOrden = [None for _ in range(4)]
labelPrimerOrden = [None for _ in range(4)]
entradaA = [None for _ in range(4)]
labelA = [None for _ in range(4)]
entradaB = [None for _ in range(5)]
labelB = [None for _ in range(5)]
entradaO = [None for _ in range(3)]
labelO = [None for _ in range(3)]
entradaD = None
labelD = None

continuePlotting = False

def close_window():
    global continuePlotting, gui, figure
    continuePlotting = False
    gui.destroy()
    plt.close()
    #exit()

def change_state():
    global continuePlotting, start_stop_button
    if continuePlotting:
        continuePlotting = False
        start_stop_button.config(bg="green")
    else:
        continuePlotting = True
        start_stop_button.config(bg="red")
    print("Start/Stop Pressed")

def plotter(): 
    global punto, C, M, Po, Mo
    while continuePlotting:
        print(f"Punto: {punto}")
        print(f"A: {A}")
        print(f"B: {B}")
        print(f"M: {M}")
        print(f"C: {C}")
        print(f"Retraso d: {d}")
        if len(Mo) > 0:
            M[0] = Mo.pop(0)

        C[0] = 0
        for i in range(4):
            C[0] += A[i]*C[i+1]
            C[0] += B[i]*M[i+d-1]
        C[0] += B[4]*M[4+d-1]
        C[0] += Po[0]

        ax1.set_xlim([max(0, punto-GRAPOINTS), max(GRAPOINTS+2, punto+2)])
        ax1.plot([punto-1, punto], [C[1], C[0]], '-', markersize=3, c="blue") # Salida
        ax2.step([punto-1, punto], [M[1], M[0]], '-', markersize=3, c="blue") # Entrada
        ax2.step([punto-1, punto], [Po[1], Po[0]], '-', markersize=3, c="green") # Perturbacion
        ax1.legend(labels=['Salida'], loc="best")
        ax2.legend(labels=['Entrada', 'Perturbacion'], loc="best")
        plt.pause(1)

        for i in range(len(C)-1, 0, -1):
            C[i] = C[i-1]

        for i in range(len(M)-1, 0, -1):
            M[i] = M[i-1]

        Po[1] = Po[0]

        punto += 1

def reset():
    global gananciaK, tiempoTau, tiempoTheta, periodoT, d, aux, m, A, B, M, C, archivoEntrada, Mo, Po, punto, ax1, ax2
    gananciaK = 0.0
    tiempoTau = 0.0
    tiempoTheta = 0.0
    periodoT = 0.0
    d = 0
    aux = 0.0
    m = 0.0
    # Arreglos importantes
    A = [0.0 for _ in range(4)]
    B = [0.0 for _ in range(5)]
    M = []
    C = [0.0 for _ in range(5)]
    archivoEntrada = ""
    Mo = []
    Po = [0.0, 0.0]
    punto = 0
    ax1.cla()
    ax2.cla()
    ax1.grid(True)
    ax2.grid(True)

def gui_handler(): 
    change_state() 
    threading.Thread(target=plotter).start()

def usePrimerOrden():
    for i in range(4):
        entradaPrimerOrden[i].config(state="normal")
        entradaA[i].config(state="disabled")
        entradaB[i].config(state="disabled")
    entradaB[-1].config(state="disabled")
    entradaD.config(state="disabled")
    print("Primer Orden Mode Chosen")

def useARX():
    for i in range(4):
        entradaPrimerOrden[i].config(state="disabled")
        entradaA[i].config(state="normal")
        entradaB[i].config(state="normal")
    entradaB[-1].config(state="normal")
    entradaD.config(state="normal")
    print("ARX Mode Chosen")

def setPrimerOrden(event):
    global gananciaK, tiempoTau, tiempoTheta, periodoT, d, aux, m, M, A, B
    gananciaK = float(entradaPrimerOrden[0].get()) if entradaPrimerOrden[0].get() != "" else 0.0
    tiempoTau = float(entradaPrimerOrden[1].get()) if entradaPrimerOrden[1].get() != "" else 0.0
    tiempoTheta = float(entradaPrimerOrden[2].get()) if entradaPrimerOrden[2].get() != "" else 0.0
    periodoT = float(entradaPrimerOrden[3].get()) if entradaPrimerOrden[3].get() != "" else 0.0
    d = int(math.trunc(tiempoTheta / periodoT))
    aux = tiempoTheta - d * periodoT
    m = 1 - ( aux / periodoT )
    A[0] = math.exp(-1.0*periodoT/tiempoTau)
    B[1] = gananciaK * (1 - math.exp(-1.0*m*periodoT/tiempoTau))
    B[2] = gananciaK * (math.exp(-1*m*periodoT/tiempoTau) - math.exp(-1*periodoT/tiempoTau))
    while len(M) < (4+d):
        M.append(0.0)
    while len(M) > (4+d):
        M.pop()
    print("Primer Orden Changed")    

def setAB(event):
    global A, B, M, d
    for i in range(4):
        if entradaA[i].get() == "":
            A[i] = 0.0
        else:
            A[i] = float(entradaA[i].get())
    print("As Changed")
    for i in range(5):
        if entradaB[i].get() == "":
            B[i] = 0.0
        else:
            B[i] = float(entradaB[i].get())
    print("Bs Changed")

    if entradaD.get() == "":
        d = 0
    else:
        d = int(entradaD.get())    
    print("d Changed")

    while len(M) < (4+d):
        M.append(0.0)
    while len(M) > (4+d):
        M.pop()

def setMo(event):
    global M
    M[0] = float(entradaO[0].get()) if entradaO[0].get() != "" else 0.0
    print("Mo Changed")

def setPo(event):
    global Po
    Po[0] = float(entradaO[2].get()) if entradaO[2].get() != "" else 0.0
    print("Po Changed")

def loadFile(event):
    with open(str(entradaO[1].get())+".txt", 'r') as file:
        for line in file.readlines():
            Mo.append(float(line))
    print(f"File read {Mo}")

# Create Window
gui = tk.Tk() # where m is the name of the main window object
gui.title("Simulador de Plantas con Filtro ARX")
gui.geometry("200x600")
gui.protocol("WM_DELETE_WINDOW", close_window)

# Create Widgets
modo_simulacion = tk.StringVar() 
tk.Label(gui, text="Modo de Operacion").pack(anchor="w")
tk.Radiobutton(gui, text='Primer Orden', variable=modo_simulacion, value="Primer Orden", command=usePrimerOrden).pack(anchor="w")
tk.Radiobutton(gui, text='Filtro ARX', variable=modo_simulacion, value="Filtro ARX", command=useARX).pack(anchor="w")
print(modo_simulacion)

tk.Label(gui, text="Primer Orden").pack(anchor="w")
primer_orden = tk.Frame()
primer_orden.pack(anchor="w")
for i, name in enumerate(["K", "Tau", "Theta", "Ts"]):
    labelPrimerOrden[i] = tk.Label(primer_orden, text=f"{name}")
    labelPrimerOrden[i].grid(row=i, column=0)
    entradaPrimerOrden[i] = tk.Entry(primer_orden)
    entradaPrimerOrden[i].grid(row=i, column=1)
    entradaPrimerOrden[i].bind("<Return>", setPrimerOrden)

tk.Label(gui, text="Ecuación de diferencias").pack(anchor="w")
# Entradas de A
entradas_ab = tk.Frame()
entradas_ab.pack(anchor="w")
for i in range(4):
    labelA[i] = tk.Label(entradas_ab, text=f"A{i+1}")
    labelA[i].grid(row=i, column=0)
    entradaA[i] = tk.Entry(entradas_ab)
    entradaA[i].grid(row=i, column=1)
    entradaA[i].bind("<Return>", setAB)

for i in range(4, 9):
    labelB[i-4] = tk.Label(entradas_ab, text=f"B{i-4}")
    labelB[i-4].grid(row=i, column=0)
    entradaB[i-4] = tk.Entry(entradas_ab)
    entradaB[i-4].grid(row=i, column=1)
    entradaB[i-4].bind("<Return>", setAB)

labelD = tk.Label(entradas_ab, text=f"Retraso d")
labelD.grid(row=9, column=0)
entradaD = tk.Entry(entradas_ab)
entradaD.grid(row=9, column=1)
entradaD.bind("<Return>", setAB)

tk.Label(gui, text="Entradas Mo y Po").pack(anchor="w")
# Entrada escalon y perturbacion
entradas_o = tk.Frame()
entradas_o.pack(anchor="w")
for i, name in enumerate(["Mo", "Archivo", "Po"]):
    labelO[i] = tk.Label(entradas_o, text=f"{name}")
    labelO[i].grid(row=i, column=0)
    entradaO[i] = tk.Entry(entradas_o)
    entradaO[i].grid(row=i, column=1)
entradaO[0].bind("<Return>", setMo)
entradaO[1].bind("<Return>", loadFile)
entradaO[2].bind("<Return>", setPo)

# Start Stop Button
start_stop_button = tk.Button(gui, text='Start/Stop', width=25, bg="green", fg="white", command=gui_handler) 
start_stop_button.pack(anchor="w", pady=5, padx=5) 
# Reset Button
reset_button = tk.Button(gui, text='Reset', width=25, bg="green", fg="white", command=reset) 
reset_button.pack(anchor="w", pady=5, padx=5) 

# Graficas
figure, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6), tight_layout=True, num="Graficas")
ax1.grid(True)
ax2.grid(True)
ax1.set_title('Salida')
ax2.set_title('Entrada y Perturbacion')
plt.xticks(rotation=45, fontsize=8)
plt.show(block=True)