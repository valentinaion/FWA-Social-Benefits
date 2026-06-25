"""
Scenario-2 CONTROL documents — the genuine "clean applicant" (Elena Marinescu, A-88204).
These are the legitimate counterpart to the fraudulent Scenario-1 set: a valid passport,
a registered-employer pay stub, a recent unaltered utility bill, and a passed video frame.
Use them to show the system letting an honest citizen through — and as negative (genuine)
samples for the Validation / Face Verification agents.

Run from repo root:  python synthetic-data/generators/build_documents_scenario2.py
(expects working/id-face-clean.png; falls back to a placeholder if absent)
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps, PngImagePlugin

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "synthetic-data", "documents", "scenario2")
os.makedirs(OUT, exist_ok=True)
FD = "/opt/venv/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf"

GREEN = (57, 165, 110)
INK = (20, 30, 50)


def font(size, bold=False, mono=False):
    name = "DejaVuSansMono.ttf" if mono else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    try:
        return ImageFont.truetype(os.path.join(FD, name), size)
    except Exception:
        return ImageFont.load_default()


def load_face(filename, box):
    for base in (os.path.join(ROOT, "working"), "working", os.path.join(ROOT, "..", "..", "working")):
        p = os.path.join(base, filename)
        if os.path.exists(p):
            return ImageOps.fit(Image.open(p).convert("RGB"), box, method=Image.LANCZOS)
    ph = Image.new("RGB", box, (60, 72, 96))
    ImageDraw.Draw(ph).text((box[0] // 2 - 10, box[1] // 2 - 10), "?", font=font(48, True), fill=(210, 220, 235))
    return ph


def watermark(img, text="SPECIMEN  ·  SYNTHETIC DATA"):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(max(28, img.width // 22), bold=True)
    for i in range(-img.height, img.width, 520):
        d.text((i, img.height // 2), text, font=f, fill=(120, 150, 210, 38))
    return Image.alpha_composite(img.convert("RGBA"), layer.rotate(30, expand=False)).convert("RGB")


def save_png(img, name, software="GovScan IDCapture v3", extra=None):
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Software", software)
    meta.add_text("Comment", "SYNTHETIC SPECIMEN — not a real document")
    for k, v in (extra or {}).items():
        meta.add_text(k, str(v))
    path = os.path.join(OUT, name)
    img.save(path, pnginfo=meta)
    print("wrote", os.path.relpath(path, ROOT))


def verified_badge(d, x, y):
    d.rounded_rectangle([x, y, x + 116, y + 26], radius=6, fill=(20, 60, 42), outline=GREEN, width=2)
    d.ellipse([x + 8, y + 6, x + 22, y + 20], outline=GREEN, width=2)
    d.line([x + 11, y + 13, x + 14, y + 17], fill=GREEN, width=2)
    d.line([x + 14, y + 17, x + 19, y + 9], fill=GREEN, width=2)
    d.text((x + 30, y + 6), "VERIFIED", font=font(13, True), fill=GREEN)


# ---------------- Passport (genuine) ----------------
def passport():
    W, H = 1000, 660
    img = Image.new("RGB", (W, H), (17, 34, 63))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 70], fill=(11, 23, 48))
    d.text((28, 22), "REPUBLIC OF UTOPIA   ·   PASSPORT  /  PASSEPORT", font=font(24, True), fill=(180, 200, 235))
    d.text((W - 150, 26), "TYPE  P", font=font(18, True, mono=True), fill=(150, 175, 215))
    box = (240, 300)
    img.paste(load_face("id-face-clean.png", box), (36, 110))
    d.rectangle([36, 110, 276, 410], outline=(90, 115, 160), width=2)
    fx = 320
    fields = [
        ("Surname / Nom", "MARINESCU"),
        ("Given names / Prénoms", "ELENA"),
        ("Passport No. / No.", "Y2 884 204"),
        ("Nationality", "UTOPIAN"),
        ("Date of birth", "25 FEB 1994"),
        ("Date of expiry", "09 OCT 2032"),
    ]
    y = 118
    for k, v in fields:
        d.text((fx, y), k.upper(), font=font(14, mono=True), fill=(130, 155, 195))
        d.text((fx, y + 18), v, font=font(26, True), fill=(238, 244, 255))
        y += 64
    verified_badge(d, 760, 120)
    d.rectangle([0, H - 110, W, H], fill=(243, 245, 251))
    d.text((28, H - 92), "P<UTOMARINESCU<<ELENA<<<<<<<<<<<<<<<<<<<<<<<<", font=font(26, mono=True), fill=INK)
    d.text((28, H - 56), "Y28842041UTO9402254F3210099<<<<<<<<<<<<<<<<06", font=font(26, mono=True), fill=INK)
    save_png(watermark(img), "passport-clean-elena.png")


# ---------------- Pay stub (registered employer) ----------------
def payslip():
    W, H = 820, 1040
    img = Image.new("RGB", (W, H), (244, 246, 251))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 90], fill=(31, 79, 160))
    d.text((34, 24), "Contoso Ltd", font=font(28, True), fill=(255, 255, 255))
    d.text((34, 60), "Payslip — Period 05/2026 · Ref CTS-20416", font=font(16), fill=(190, 205, 230))
    rows = [
        ("Employee", "E. Marinescu", False),
        ("National ID", "UT-8820401", False),
        ("Employer VAT", "UT-VAT-114829  (valid)", True),
        ("Gross pay", "EUR 2,000.00", False),
        ("Pay date", "2026-05-29", False),
        ("Tax withheld", "EUR 400.00", False),
        ("Net pay", "EUR 1,600.00", False),
    ]
    y = 150
    for k, v, ok in rows:
        d.text((44, y), k, font=font(20), fill=(60, 72, 96))
        col = GREEN if ok else INK
        if ok:
            tw = d.textlength(v, font=font(20, True))
            d.rounded_rectangle([460 - 6, y - 4, 460 + tw + 6, y + 26], radius=4, fill=(225, 245, 234))
        d.text((460, y), v, font=font(20, True), fill=col)
        d.line([44, y + 40, W - 44, y + 40], fill=(210, 217, 232), width=1)
        y += 58
    d.text((44, y + 16), "Cross-match: employer registered · income consistent with tax records.",
           font=font(15), fill=GREEN)
    d.text((44, H - 70), "SYNTHETIC SPECIMEN — illustrative payslip (genuine control sample).",
           font=font(15), fill=(140, 150, 170))
    save_png(img, "payslip-contoso.png")


# ---------------- Utility bill (recent, unaltered) ----------------
def utility_bill():
    W, H = 820, 1040
    img = Image.new("RGB", (W, H), (250, 250, 252))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 86], fill=(31, 79, 160))
    d.text((34, 26), "Capital City Power & Water  —  Statement", font=font(24, True), fill=(255, 255, 255))
    rows = [
        ("Issue date", "05 JUN 2026   (within 3-month policy)", True),
        ("Account holder", "ELENA MARINESCU", False),
        ("Service address", "77 Birch Rd, Capital City", False),
        ("Account no.", "CC-5521-8820", False),
        ("Billing period", "May 2026", False),
        ("Amount due", "EUR 74.10", False),
    ]
    y = 140
    for k, v, ok in rows:
        d.text((44, y), k, font=font(19), fill=(60, 72, 96))
        col = GREEN if ok else INK
        d.text((300, y), v, font=font(19, True), fill=col)
        d.line([44, y + 38, W - 44, y + 38], fill=(225, 228, 238), width=1)
        y += 56
    d.text((44, y + 18), "Recent, consistent name & address — passes proof-of-address checks.",
           font=font(15), fill=GREEN)
    d.text((44, H - 64), "SYNTHETIC SPECIMEN — illustrative utility bill (genuine control sample).",
           font=font(15), fill=(150, 158, 175))
    save_png(img, "utility-bill-recent.png")


# ---------------- Video frame (passed liveness) ----------------
def video_frame():
    W, H = 880, 540
    img = Image.new("RGB", (W, H), (12, 22, 30))
    img.paste(load_face("id-face-clean.png", (300, 380)), (W // 2 - 150, 70))
    d = ImageDraw.Draw(img)
    d.ellipse([20, 18, 34, 32], fill=(255, 70, 100))
    d.text((42, 16), "REC  ·  LIVE", font=font(18, True), fill=(240, 245, 255))
    d.rectangle([0, H - 60, W, H], fill=(20, 90, 60))
    d.text((24, H - 46), "LIVENESS PASSED  ·  face matches ID  ·  genuine applicant",
           font=font(20, True), fill=(220, 255, 235))
    save_png(img, "video-consult-frame-clean.png", software="VideoCapture (synthetic)")


def sidecars():
    json.dump({
        "file": "passport-clean-elena.png", "synthetic": True, "ground_truth": "genuine",
        "expected_agent": "validation", "expected_capabilities": ["vision", "docintel"],
        "indicators": {"portrait_splice": False, "noise_inconsistency": False, "jpeg_ghost": False,
                       "copy_move": False, "metadata_software": "GovScan IDCapture v3", "edited": False},
        "expected_finding": "No tampering detected — genuine document",
    }, open(os.path.join(OUT, "passport-clean-elena.metadata.json"), "w"), indent=2)
    json.dump({
        "file": "video-consult-frame-clean.png", "synthetic": True, "ground_truth": "genuine",
        "expected_agent": "face-verification", "expected_capabilities": ["face", "safety", "vision"],
        "liveness": {"passive_score": 0.97, "blink_detected": True, "micro_expression": True},
        "deepfake_score": 0.03, "face_match_to_id": True,
        "expected_finding": "Live person, matches ID portrait",
    }, open(os.path.join(OUT, "video-session-clean.metadata.json"), "w"), indent=2)
    json.dump({
        "_note": "SYNTHETIC. Genuine control application — the clean counterpart to the fraud ring.",
        "applicant": {"id": "A-88204", "name": "Elena Marinescu", "national_id": "UT-8820401",
                      "dob": "1994-02-25", "address": "77 Birch Rd, Capital City",
                      "employer": "Contoso Ltd", "declared_annual_income_eur": 24000,
                      "monthly_benefit_eur": 1100, "iban": "UT12BANK0000088204",
                      "phone": "+40 720 110 204", "benefit_types": ["unemployment", "housing"]},
        "checks": {"identity_verified": True, "document_tampering": False, "employer_registered": True,
                   "income_matches_tax": True, "address_valid_recent": True, "liveness_passed": True,
                   "device_ip_anomaly": False},
        "decision": {"outcome": "approve", "stage": "auto", "riskScore": 12,
                     "note": "All cross-checks passed — onboarded without friction.",
                     "audit": {"loggedTo": "Microsoft Purview"}},
    }, open(os.path.join(OUT, "application-summary.json"), "w"), indent=2)
    print("wrote 3 metadata/summary files")


if __name__ == "__main__":
    passport()
    payslip()
    utility_bill()
    video_frame()
    sidecars()
    print("clean-applicant documents complete.")
