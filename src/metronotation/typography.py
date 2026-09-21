"""Embed the same licensed typefaces in every offline HTML and printed sheet."""

from base64 import b64encode
from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=1)
def stylesheet():
    assets = files("metronotation").joinpath("assets")
    rules = []
    for name, weights in (
        ("cabin", (("medium", 500), ("semibold", 600))),
        ("arimo", (("regular", 400),)),
    ):
        license_text = assets.joinpath(f"fonts/{name}-license.txt").read_text(encoding="utf-8")
        rules.append(f"/* {license_text} */")
        for style, weight in weights:
            font = b64encode(assets.joinpath(f"fonts/{name}-{style}.ttf").read_bytes()).decode(
                "ascii"
            )
            rules.append(
                f"@font-face {{ font-family: '{name.title()}'; font-style: normal; "
                f"font-weight: {weight}; font-display: block; "
                f"src: url(data:font/ttf;base64,{font}) format('truetype'); }}"
            )
    return "\n".join(rules) + "\n" + assets.joinpath("style.css").read_text(encoding="utf-8")
