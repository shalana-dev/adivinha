"""Captura screenshots e GIF do jogo Adivinhe o Número."""
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
URL = "http://127.0.0.1:8766/index.html"


def get_secret(page) -> int:
    secret = {"value": None}

    def on_console(msg):
        text = msg.text
        if text.startswith("Psiu... o numero e "):
            secret["value"] = int(text.split()[-1])

    page.on("console", on_console)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(300)
    if secret["value"] is None:
        raise RuntimeError("Não foi possível ler o número secreto do console.")
    return secret["value"]


def tentar(page, valor: int) -> None:
    page.fill("#palpite", str(valor))
    page.click("button[type='submit']")
    page.wait_for_timeout(500)


def capture() -> None:
    ASSETS.mkdir(exist_ok=True)
    frames: list[Path] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 650})
        secret = get_secret(page)

        page.screenshot(path=str(ASSETS / "adivinha-inicio.png"))
        frames.append(ASSETS / "frame-00.png")
        page.screenshot(path=str(frames[-1]))

        tentar(page, max(1, secret - 25))
        page.screenshot(path=str(ASSETS / "adivinha-dica.png"))
        frames.append(ASSETS / "frame-01.png")
        page.screenshot(path=str(frames[-1]))

        tentar(page, min(100, secret + 25))
        frames.append(ASSETS / "frame-02.png")
        page.screenshot(path=str(frames[-1]))

        tentar(page, secret)
        page.screenshot(path=str(ASSETS / "adivinha-vitoria.png"))
        frames.append(ASSETS / "frame-03.png")
        page.screenshot(path=str(frames[-1]))

        for i in range(4, 8):
            path = ASSETS / f"frame-{i:02d}.png"
            page.goto(URL, wait_until="networkidle")
            page.wait_for_timeout(250)
            page.screenshot(path=str(path))
            frames.append(path)

        browser.close()

    images = [Image.open(frame).convert("RGB") for frame in frames]
    gif_path = ASSETS / "adivinha-demo.gif"
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=900,
        loop=0,
    )
    Image.open(ASSETS / "adivinha-inicio.png").save(ASSETS / "adivinha-screenshot.png")
    print(f"GIF: {gif_path}")


if __name__ == "__main__":
    capture()
