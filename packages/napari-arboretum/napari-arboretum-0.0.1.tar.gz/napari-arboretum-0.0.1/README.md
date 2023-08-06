# Arboretum

### Overview

A dockable widget for [Napari](https://github.com/napari) for visualizing cell lineage trees.


Features:
+ Lineage tree plot widget
+ Integration with [btrack](https://github.com/quantumjot/BayesianTracker)

[![LineageTree](./examples/napari.png)](http://lowe.cs.ucl.ac.uk/cellx.html)  
*Automated cell tracking and lineage tree reconstruction*.

---  

 :construction:  **WORK IN PROGRESS**  :construction:

 This project has changed considerably. The `Tracks` layer, originally developed for this plugin, is now an official layer type in napari. Read the napari documentation here:  
 https://napari.org/api/stable/napari.layers.Tracks.html#napari.layers.Tracks


 To view the legacy version of this plugin, visit the legacy branch:  
 https://github.com/quantumjot/arboretum/tree/v1-legacy

---

#### TODO:
+ [x] Refactor for Napari 0.4.0 (now including `napari.layers.Tracks`!)
+ [ ] Highlight cells in the viewer from the lineage tree view
+ [ ] Visualize merges
+ [ ] Color trees by properties

---

### Installation

We recommend that you first install napari. Detailed instructions are here: https://github.com/napari/napari.

```sh
pip install napari[all]
```

then install arboretum:

```sh
git clone https://github.com/quantumjot/arboretum.git
cd arboretum
pip install -e .
```

Once installed, Arboretum will be visible in the `Plugins > Add Dock Widget > arboretum` menu in napari.
