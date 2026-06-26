"""
Generates the Scenario-1 SPECIMEN documents from synthetic ID portraits.
Every artifact is clearly watermarked SYNTHETIC / SPECIMEN and uses a fictional
country (Republic of Utopia). Ground-truth tamper/liveness labels are written to
*.metadata.json sidecars so the documents double as a labelled test set for the
Validation and Face Verification agents.

Run from repo root:  python synthetic-data/generators/build_documents.py
(expects working/id-face-genuine.png and working/id-face-imposter.png to exist;
 falls back to drawn placeholders if they are missing)
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps, PngImagePlugin

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "synthetic-data", "documents", "scenario1")
os.makedirs(OUT, exist_ok=True)
WORK = os.path.join(ROOT, "..", "..", "working")  # /mnt/workspace/working when run in-place
FD = "/opt/venv/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf"


def font(size, bold=False, mono=False):
    name = "DejaVuSansMono.ttf" if mono else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    try:
        return ImageFont.truetype(os.path.join(FD, name), size)
    except Exception:
        return ImageFont.load_default()


def load_face(filename, box):
    for base in (WORK, os.path.join(ROOT, "working"), "working"):
        p = os.path.join(base, filename)
        if os.path.exists(p):
            return ImageOps.fit(Image.open(p).convert("RGB"), box, method=Image.LANCZOS)
    ph = Image.new("RGB", box, (60, 72, 96))
    d = ImageDraw.Draw(ph)
    d.text((box[0] // 2 - 10, box[1] // 2 - 10), "?", font=font(48, True), fill=(200, 210, 230))
    return ph


def watermark(img, text="SPECIMEN  ·  SYNTHETIC DATA"):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(max(28, img.width // 22), bold=True)
    for i in range(-img.height, img.width, 360):
        d.text((i, img.height // 2), text, font=f, fill=(255, 70, 110, 40))
    layer = layer.rotate(30, expand=False)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def save_png(img, name, software="DocScanner v3", extra=None):
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Software", software)
    meta.add_text("Comment", "SYNTHETIC SPECIMEN — not a real document")
    if extra:
        for k, v in extra.items():
            meta.add_text(k, str(v))
    path = os.path.join(OUT, name)
    img.save(path, pnginfo=meta)
    print("wrote", os.path.relpath(path, ROOT))
    return path


# ---------------- Passport ----------------
def passport(face_file, tampered=False):
    W, H = 1000, 660
    img = Image.new("RGB", (W, H), (17, 34, 63))
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0, 0, W, 70], fill=(11, 23, 48))
    d.text((28, 22), "REPUBLIC OF UTOPIA   ·   PASSPORT  /  PASSEPORT", font=font(24, True), fill=(180, 200, 235))
    d.text((W - 150, 26), "TYPE  P", font=font(18, True, mono=True), fill=(150, 175, 215))
    # photo
    box = (240, 300)
    face = load_face(face_file, box)
    px, py = 36, 110
    img.paste(face, (px, py))
    d.rectangle([px, py, px + box[0], py + box[1]], outline=(90, 115, 160), width=2)
    # fields
    fx = 320
    fields = [
        ("Surname / Nom", "VOLKOV"),
        ("Given names / Prénoms", "ANDREI"),
        ("Passport No. / No.", "X1 902 412"),
        ("Nationality", "UTOPIAN"),
        ("Date of birth", "12 MAR 1989"),
        ("Date of expiry", "04 APR 2031"),
    ]
    y = 118
    for k, v in fields:
        d.text((fx, y), k.upper(), font=font(14, mono=True), fill=(130, 155, 195))
        d.text((fx, y + 18), v, font=font(26, True), fill=(238, 244, 255))
        y += 64
    # MRZ
    d.rectangle([0, H - 110, W, H], fill=(243, 245, 251))
    mrz1 = "P<UTOVOLKOV<<ANDREI<<<<<<<<<<<<<<<<<<<<<<<<<<"
    mrz2 = "X19024127UTO8903128M3104049<<<<<<<<<<<<<<<<00"
    d.text((28, H - 92), mrz1, font=font(26, mono=True), fill=(20, 30, 50))
    d.text((28, H - 56), mrz2, font=font(26, mono=True), fill=(20, 30, 50))

    if tampered:
        # subtle splice artifacts around the portrait (ground truth in sidecar)
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        od.ellipse([px + 40, py + 50, px + 200, py + 210], fill=(255, 60, 90, 55))   # ELA hotspot
        od.rectangle([px, py, px + box[0], py + box[1]], outline=(255, 60, 90, 160), width=3)
        od.line([px, py + 150, px + box[0], py + 150], fill=(255, 255, 255, 60), width=2)  # lighting seam
        img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

    img = watermark(img)
    if tampered:
        return save_png(img, "passport-tampered.png", software="GIMP 2.10 (edited)",
                        extra={"LastModified": "2026-06-21T22:14:00Z"})
    return save_png(img, "passport-clean.png", software="GovScan IDCapture v3")


# ---------------- Pay stub ----------------
def payslip():
    W, H = 820, 1040
    img = Image.new("RGB", (W, H), (244, 246, 251))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 90], fill=(14, 23, 48))
    d.text((34, 24), "Northwind Staffing Solutions LLC", font=font(28, True), fill=(255, 255, 255))
    d.text((34, 60), "Payslip — Period 05/2026 · Ref NW-44812", font=font(16), fill=(160, 180, 215))
    rows = [
        ("Employee", "A. Volkov", False),
        ("National ID", "UT-4471012", False),
        ("Employer VAT", "INVALID / UNREGISTERED", True),
        ("Gross pay", "EUR 4,950.00", True),
        ("Pay date", "Sun 2026-05-31  (weekend)", True),
        ("Tax withheld", "EUR 1,040.00", False),
        ("Net pay", "EUR 3,910.00", False),
    ]
    y = 150
    for k, v, bad in rows:
        d.text((44, y), k, font=font(20), fill=(60, 72, 96))
        col = (179, 23, 58) if bad else (20, 30, 50)
        if bad:
            tw = d.textlength(v, font=font(20, True))
            d.rectangle([460 - 6, y - 4, 460 + tw + 6, y + 26], fill=(255, 222, 230))
        d.text((460, y), v, font=font(20, True), fill=col)
        d.line([44, y + 40, W - 44, y + 40], fill=(210, 217, 232), width=1)
        y += 58
    d.text((44, H - 70), "SYNTHETIC SPECIMEN — fictitious employer, not a real payslip.",
           font=font(15), fill=(140, 150, 170))
    save_png(img, "payslip-northwind.png", software="PDFedit 1.2")


# ---------------- Utility bill ----------------
def utility_bill():
    W, H = 820, 1040
    img = Image.new("RGB", (W, H), (250, 250, 252))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 86], fill=(31, 79, 160))
    d.text((34, 26), "Lakeside Utilities  —  Account Statement", font=font(26, True), fill=(255, 255, 255))
    rows = [
        ("Issue date", "15 JUL 2025   (11 months ago — exceeds 3-month rule)", True),
        ("Account holder", "A. VOLKOV", True),
        ("Service address", "12 Harbor St, Lakeside", False),
        ("Account no.", "LU-7782-4471", False),
        ("Billing period", "Jun 2025", False),
        ("Amount due", "EUR 86.40", False),
    ]
    y = 140
    for k, v, bad in rows:
        d.text((44, y), k, font=font(19), fill=(60, 72, 96))
        col = (179, 23, 58) if bad else (20, 30, 50)
        if bad:
            tw = d.textlength(v, font=font(19, True))
            d.rectangle([300 - 6, y - 4, 300 + tw + 6, y + 24], outline=(220, 40, 70), width=2)
        d.text((300, y), v, font=font(19, True), fill=col)
        d.line([44, y + 38, W - 44, y + 38], fill=(225, 228, 238), width=1)
        y += 56
    d.text((44, y + 20), "Note: account-holder field shows a different embedded font (altered).",
           font=font(15), fill=(150, 80, 90))
    d.text((44, H - 64), "SYNTHETIC SPECIMEN — illustrative utility bill.",
           font=font(15), fill=(150, 158, 175))
    save_png(img, "utility-bill.png", software="GIMP 2.10 (edited)",
             extra={"LastModified": "2026-06-22T08:03:00Z"})


# ---------------- Deepfake video frame ----------------
def video_frame():
    W, H = 880, 540
    img = Image.new("RGB", (W, H), (12, 20, 38))
    face = load_face("id-face-imposter.png", (300, 380))
    img.paste(face, (W // 2 - 150, 70))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 28):
        d.line([x, 0, x, H], fill=(59, 155, 255), width=1)
    for yy in range(0, H, 28):
        d.line([0, yy, W, yy], fill=(59, 155, 255), width=1)
    img = Image.blend(img, Image.new("RGB", (W, H), (12, 20, 38)), 0.35)
    d = ImageDraw.Draw(img)
    d.ellipse([20, 18, 34, 32], fill=(255, 70, 100))
    d.text((42, 16), "REC  ·  LIVE", font=font(18, True), fill=(240, 245, 255))
    d.rectangle([0, H - 60, W, H], fill=(179, 23, 58))
    d.text((24, H - 46), "⚠  DEEPFAKE DETECTED  ·  liveness failed  ·  face mismatch vs. ID",
           font=font(20, True), fill=(255, 255, 255))
    save_png(img, "video-consult-frame.png", software="VideoCapture (synthetic)")


def sidecars():
    json.dump({
        "file": "passport-tampered.png", "synthetic": True, "ground_truth": "tampered",
        "expected_agent": "validation", "expected_capabilities": ["vision", "docintel"],
        "indicators": {
            "portrait_splice": True, "ela_hotspot_region_xywh": [76, 160, 160, 160],
            "noise_inconsistency": True, "jpeg_ghost": True, "copy_move": False,
            "metadata_software": "GIMP 2.10", "last_modified": "2026-06-21T22:14:00Z",
        },
        "expected_finding": "Tampered portrait detected — face-swap / re-compression",
    }, open(os.path.join(OUT, "passport-tampered.metadata.json"), "w"), indent=2)
    json.dump({
        "file": "video-consult-frame.png", "synthetic": True, "ground_truth": "deepfake",
        "expected_agent": "face-verification", "expected_capabilities": ["face", "safety", "vision"],
        "liveness": {"passive_score": 0.08, "blink_detected": False, "micro_expression": False},
        "deepfake_score": 0.94, "face_match_to_id": False,
        "frame_artifacts": ["gan_checkerboard", "temporal_flicker", "lip_sync_drift"],
        "expected_finding": "Synthetic video detected — liveness failed, face mismatch",
    }, open(os.path.join(OUT, "video-session.metadata.json"), "w"), indent=2)
    print("wrote 2 metadata sidecars")


if __name__ == "__main__":
    passport("id-face-genuine.png", tampered=False)
    passport("id-face-imposter.png", tampered=True)
    payslip()
    utility_bill()
    video_frame()
    sidecars()
    print("documents complete.")
