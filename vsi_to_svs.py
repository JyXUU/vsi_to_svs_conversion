
import sys
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

    # print(f"Extracting metadata...")
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

    print(f"[Writing SVS to {output_path}")
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vsi_to_svs.py input.vsi output.svs")
        sys.exit(1)

    convert_fullres_bioformats(sys.argv[1], sys.argv[2])