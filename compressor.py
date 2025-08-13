from PIL import Image

def compress_tif(input_path, output_path):
    """
    Compresses a TIF image using LZW compression.
    """
    try:
        with Image.open(input_path) as img:
            img.save(output_path, compression="tiff_lzw")
        return True, None
    except Exception as e:
        return False, str(e)
