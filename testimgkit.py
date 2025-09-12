import imgkit
from PIL import Image
import io
import os, stat, subprocess, sys, imgkit

BIN = "C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe"   # adjust if needed
LIB = "/home/container/wk/lib"

# 5) Minimal render to disk
html = r'<div style="background-color:white; display:inline-block;"><figure class="table"><table class="gdr"><caption style="caption-side: top;"><p style="text-align: center;">Millions of Metric Tons of Copper Mined in 1995 and 2020</p></caption><thead><tr><th scope="col" style="text-align: center;vertical-align: bottom;">Country</th><th scope="col" style="text-align: center;vertical-align: bottom;">1995</th><th scope="col" style="text-align: center;vertical-align: bottom;">2020</th></tr></thead><tbody><tr><th scope="row" style="text-align: left;">Canada</th><td style="text-align: center;">0.73</td><td style="text-align: center;">0.59</td></tr><tr><th scope="row" style="text-align: left;">Indonesia</th><td style="text-align: center;">0.44</td><td style="text-align: center;">0.51</td></tr><tr><th scope="row" style="text-align: left;">Kazakhstan</th><td style="text-align: center;">0.26</td><td style="text-align: center;">0.55</td></tr><tr><th scope="row" style="text-align: left;">Chile</th><td style="text-align: center;">2.49</td><td style="text-align: center;">5.73</td></tr></tbody></table></figure>'
# html = r'<style>body {background-color: rgba(255, 255, 255, 0.5);}</style><p>sadfsdfsafd</p></div>'

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