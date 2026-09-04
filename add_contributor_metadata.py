from pathlib import Path
import shutil
import subprocess

CONTRIBUTOR = "Rodriquez Ventura"
PROFILE_URL = "https://www.facebook.com/street.art.galleries.barcelona/"
ROOTS = (Path("assets/images"), Path("images"))
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def image_files():
    seen = set()
    for root in ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in EXTENSIONS and path not in seen:
                seen.add(path)
                yield path

def main():
    if shutil.which("exiftool") is None:
        raise SystemExit("ExifTool is required to write contributor metadata.")
    files = list(image_files())
    if not files:
        print("No image files found.")
        return
    for path in files:
        subprocess.run([
            "exiftool",
            "-overwrite_original",
            f"-XMP-dc:Contributor={CONTRIBUTOR}",
            f"-XMP-dc:Relation={PROFILE_URL}",
            f"-XMP-photoshop:Credit={CONTRIBUTOR} / Urban Arts News",
            f"-XMP-xmpRights:WebStatement={PROFILE_URL}",
            str(path),
        ], check=True, stdout=subprocess.DEVNULL)
    print(f"Contributor metadata written to {len(files)} image files.")

if __name__ == "__main__":
    main()
