import io
import imgkit
from PIL import Image

BIN = "C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe"
LIB = "/home/container/wk/lib"

def getImageBytes(html:str):
    cfg = imgkit.config(wkhtmltoimage=BIN)
    png_bytes  = imgkit.from_string(
        html, False, config=cfg,
        options={"format": "png", "encoding": "UTF-8", "enable-local-file-access": "", "zoom":"1.5", "transparent":""}
    )

    im = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    im = im.crop((0, 1, im.width, im.height))
    im = im.crop(im.getbbox())           # tight crop
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0) 

    return buf
