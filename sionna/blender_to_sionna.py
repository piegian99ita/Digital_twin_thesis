import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sionna.rt import load_scene, Transmitter, Receiver, PlanarArray

# Carica la scena
scene = load_scene("../mitsuba_export/test_scene.xml")

# Stampa i primi 10 oggetti della scena e i loro materiali radio
for i, obj in enumerate(scene.objects.values()):
    print(f"{obj.name} : {obj.radio_material.name}")
    if i >= 10:
        break

# Configura gli array di trasmissione e ricezione
scene.tx_array = PlanarArray(
    num_rows=4,
    num_cols=4,
    vertical_spacing=0.5,
    horizontal_spacing=0.5,
    pattern="tr38901",
    polarization="V"
)

scene.rx_array = PlanarArray(
    num_rows=1,
    num_cols=1,
    vertical_spacing=0.5,
    horizontal_spacing=0.5,
    pattern="dipole",
    polarization="cross"
)

# Aggiungi trasmettitore e ricevitore alla scena
tx = Transmitter("tx", [0, 0, 0], [0.0, 0.0, 0.0])
scene.add(tx)

rx = Receiver("rx", [0, 0, 0], [0.0, 0.0, 0.0])
scene.add(rx)

# Genera la mappa di copertura
cm = scene.coverage_map()
'''
# Salva la mappa di copertura come immagine
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap='viridis', origin='lower')
plt.colorbar(label="Coverage")
plt.title("Coverage Map")
plt.savefig("coverage_map.png", dpi=300)  # Salva come PNG
plt.close()

# Renderizza la scena (puoi saltare questa parte se non desideri visualizzare il rendering)
#scene.render("preview", coverage_map=cm)

# Calcola i percorsi di propagazione
paths = scene.compute_paths()

# Converti i percorsi in CIR
a, tau = paths.cir()

# Grafico del ritardo
plt.figure(figsize=(8, 6))
plt.stem(tau[0, 0, 0, :] * 1e9, np.abs(a[0, 0, 0, 0, 0, :, 0]), basefmt=" ", use_line_collection=True)
plt.xlabel("Delay [ns]")
plt.ylabel(r"$|a|$")
plt.title("Channel Impulse Response (CIR)")
plt.grid(True)
plt.savefig("cir_graph.png", dpi=300)  # Salva come PNG
plt.close()



# Salva i percorsi calcolati come immagine
# Puoi personalizzare il rendering dei percorsi in base alle tue necessità
plt.figure(figsize=(8, 6))
for path in paths.values():
    plt.plot(path[:, 0], path[:, 1], marker='o', markersize=3, linestyle='-', color='blue', alpha=0.7)
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("Propagation Paths")
plt.grid(True)
plt.savefig("propagation_paths.png", dpi=300)  # Salva come PNG
plt.close()

# Renderizza la scena con i percorsi calcolati e la mappa di copertura
scene.render("preview", paths=paths, coverage_map=cm)

# Salva l'immagine del rendering della scena (opzionale)
# Usa l'output del rendering per creare l'immagine
# scene.render("output_image.png")  # Esempio di salvataggio immagine di rendering
'''