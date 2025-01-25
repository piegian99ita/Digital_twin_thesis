import numpy as np
import tensorflow as tf

from sionna,rt import load_scene, Transmitter, Receiver, PlanarArray, Paths2CIR

%matpltlib widget
import matplotlib.pyplot as plt

scene = load_scene("../mitsuba_export/test_scene.xml")

for i,obj in enumerate(scene.objects.values()):
    print(f"{obj.name} : {obj.radio_material.name}")
    if i>=10:
        break

scene.tx_array = PlanarArray(numrows=4,
                             numcols=4,
                             vertical_spacing=0.5,
                             horizontal_spacing=0.5,
                             pattern="tr38901",
                             polarization = "V")

scene.rx_array =PlanarArray(num_rows=1,
                            num_cols=1
                            vertical_spacing=0.5,
                            horizontal_spacing=0.5,
                             pattern="iso",
                             polarization = "V")

tx = Transmitter("tx", [0,0,0], [0.0, 0.0 0.0])
scene.add(tx)

rx = Receiver("rx", [0,0,0], [0.0, 0.0 0.0])
scene.add(rx)

cm =scene.coverage_map()

scene.preview(coverage_map=cm)

scene.render("preview",coverage_map=cm)

paths =scene.compute_paths()

p2c =  Paths2CIR(sampling_frequency=100e6, scene=scene)
a,tau = p2c(paths.as_tuple())

plt.figure()
plt.stem(tau[0,0,0,:]*1e9, np.abs(a[0,0,0,0,0,:,0]))
plt.xlabel("Delay [ns]")
plt.ylabel(r"$|a|$")

scene.preview(paths=paths)

scene.render("preview", paths=paths, coverage_map=cm)