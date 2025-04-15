import sys
import os
import numpy as np
from tqdm import tqdm
from large_image import getTileSource
import tifffile
import json

def convert_fullres_bioformats(input_path, output_path):
    print(f"Opening VSI with Bioformats: {input_path}")
    ts = getTileSource(input_path, sourceName="bioformats")

    width, height = ts.sizeX, ts.sizeY
    tile_size = 256

    metadata = ts.getMetadata()
    metadata_str = json.dumps(metadata, indent=2)
    metadata_comment = f"large_image metadata:\n{metadata_str}"

    print(f"VSI full resolution: {width} x {height}")
    img = np.zeros((height, width, 3), dtype=np.uint8)

    print(f"[INFO] Reading and tiling full WSI...")
    for y in tqdm(range(0, height, tile_size), desc="Rows"):
        for x in range(0, width, tile_size):
            tile = ts.getRegion(
                region={"left": x, "top": y, "width": tile_size, "height": tile_size},
                format="numpy", level=0
            )
            if isinstance(tile, tuple):
                tile = tile[0]

            h, w = tile.shape[:2]
            img[y:y+h, x:x+w] = tile[:, :, :3]

    print(f"[INFO] Writing SVS to {output_path}")
    tifffile.imwrite(
        output_path,
        img,
        tile=(tile_size, tile_size),
        photometric='rgb',
        compression='jpeg',
        bigtiff=True,
        description=metadata_comment
    )
    print("Conversion completed.")

def batch_convert(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    vsi_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.vsi')]
    if not vsi_files:
        print(f"No .vsi files found in {input_folder}.")
        return

    print(f"Found {len(vsi_files)} .vsi files. Starting conversion...")

    for file in vsi_files:
        input_path = os.path.join(input_folder, file)
        output_filename = os.path.splitext(file)[0] + ".svs"
        output_path = os.path.join(output_folder, output_filename)

        print(f"\nProcessing {file} ...")
        try:
            convert_fullres_bioformats(input_path, output_path)
        except Exception as e:
            print(f"[ERROR] Failed to process {file}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vsi_to_svs_batch.py input_folder/ output_folder/")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    batch_convert(input_folder, output_folder)