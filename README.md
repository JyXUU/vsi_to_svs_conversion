# VSI to SVS Converter

This repository converts `.vsi` WSIs into `.svs` format at using the `large_image` library with the Bioformats tilesource.

---

## Features

- Converts Olympus `.vsi` WSIs to `.svs`
- Preserves full resolution (no downsampling)
- Extracts and embeds metadata into the TIFF description tag
- Tiled read/write to handle large files efficiently

---

## Dependencies

Make sure the following packages are installed:

- `large_image[source_bioformats]`
- `tifffile`
- `tqdm`
- `numpy`
- `javabridge`
- `bioformats`
- Java (JDK, e.g., version 11+)

### Conda Setup Example:

conda create -n vsi_bio_env python=3.10
conda activate vsi_bio_env
pip install large-image[source_bioformats] tifffile tqdm numpy
