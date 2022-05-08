from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt

ID_PATH = Path("/mnt/c/Users/dpalma/Desktop/ids")
with open(ID_PATH / "human-face1.JPG", "rb") as img_code:
    img_view_ready = Image.open(img_code)
    _, ax = plt.subplots()
    ax.imshow(img_view_ready)

plt.show()
