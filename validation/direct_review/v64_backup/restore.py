from pathlib import Path
import hashlib, zipfile
root = Path(__file__).resolve().parent
shas = ["ca9aca8ca7c827fabc45194f60108b88d600e320","d6297f787b6cf7010e8451ff623b2972d49f0bfc","8ec64e4e850af67a5f489fdb16e52c16dc6f1853","02eb350a278385079d52b75f35ac09577551ee3f","43b0176ceedcef39470b573682fddd73c2a875f0"]
parts = []
for i, expected in enumerate(shas, 1):
    data = (root / ("X_Finger_V64_review.zip.part%02d" % i)).read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if actual != expected:
        raise ValueError("Corrupt archive part %d" % i)
    parts.append(data)
data = b"".join(parts)
if len(data) != 37095900:
    raise ValueError("Unexpected archive size")
target = root / "X_Finger_V64_review.zip"
target.write_bytes(data)
with zipfile.ZipFile(target) as archive:
    bad = archive.testzip()
    if bad:
        raise ValueError("Corrupt ZIP entry: " + bad)
    if len(archive.namelist()) != 129:
        raise ValueError("Unexpected file count")
print("Verified:", target)
print("SHA256:", hashlib.sha256(data).hexdigest())
