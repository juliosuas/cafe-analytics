"""Download only documented public assets; verify bytes before use."""
import argparse
import hashlib
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = [
    ("models/yolox_s.onnx", "https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.onnx", "c5c2d13e59ae883e6af3b45daea64af4833a4951c92d116ec270d9ddbe998063"),
    ("assets/retail.mp4", "https://videos.pexels.com/video-files/10901926/10901926-hd_1920_1080_30fps.mp4", "93e3f7aa893d781e61de49855d736662ab32b54d026f008a55b285b06cdbfd0b"),
]
CAFE_ASSET = ("assets/cafe-counter.mp4", "https://videos.pexels.com/video-files/8430969/8430969-uhd_4096_2160_25fps.mp4", "37c732b261d16cf8fe23b6a2f4745b0c321b18c5b7680657ed2e47ab0e28cebd")

FLOW_ASSET = ("assets/cafe-flow.mp4", "https://videos.pexels.com/video-files/35545660/15059172_2560_1440_30fps.mp4", "c71710a841291aa530a9596735ef8989464bc1fb11bd6c965144b552fed6f3b9")

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-only", action="store_true")
    parser.add_argument("--demo", choices=["retail", "cafe", "cafe-flow"], default="retail", help="Video publico que descargar junto al modelo")
    args = parser.parse_args()
    assets = ASSETS[:1] if args.model_only else [ASSETS[0], {"cafe": CAFE_ASSET, "cafe-flow": FLOW_ASSET, "retail": ASSETS[1]}[args.demo]]
    for relative, url, expected in assets:
        path = ROOT / relative
        if path.exists():
            if sha256(path) != expected:
                raise SystemExit(f"SHA256 incorrecto: {path}. Conservado sin modificar; revisa antes de reemplazar.")
            print(f"Verificado: {relative}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".part")
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "CafeAnalyticsDemo/0.1"})
            with urllib.request.urlopen(request, timeout=120) as response, temporary.open("wb") as output:
                for block in iter(lambda: response.read(1024 * 1024), b""):
                    output.write(block)
            if sha256(temporary) != expected:
                raise RuntimeError("La descarga cambio: hash distinto al documentado")
            temporary.replace(path)
            print(f"Descargado y verificado: {relative}")
        finally:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
