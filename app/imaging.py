import cairosvg

def svg_to_png(svg_path: str, png_path: str, dpi: int = 300):
    cairosvg.svg2png(url=svg_path, write_to=png_path, dpi=dpi)