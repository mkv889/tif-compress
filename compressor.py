import logging
from typing import Tuple, Optional
from PIL import Image

logger = logging.getLogger(__name__)

def compress_tif(input_path: str, output_path: str) -> Tuple[bool, Optional[str]]:
    """
    Compresses a TIF image using LZW compression.
    """
    try:
        logger.info(f"Starting compression: {input_path} -> {output_path}")
        with Image.open(input_path) as img:
            img.save(output_path, compression="tiff_lzw")
        logger.info(f"Successfully compressed: {input_path}")
        return True, None
    except Exception as e:
        logger.error(f"Error compressing {input_path}: {str(e)}")
        return False, str(e)
