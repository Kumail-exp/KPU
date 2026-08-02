from PIL import Image
import os

folder = "frames"
skip = 5

frames = sorted(os.listdir(folder))

with open("dotasm/badapple.asm", "w") as out:
    out.write("ldi r4 1\n\n")

    for i, filename in enumerate(frames):
        if i % skip != 0:
            continue

        img = Image.open(os.path.join(folder, filename))
        img = img.resize((32, 32), Image.Resampling.NEAREST)
        img = img.convert("L")

        pixels = list(img.getdata())

        for y in range(32):
            for x in range(32):
                p = pixels[y * 32 + x]
                out.write(f"ldi r1 {x}\n")
                out.write(f"ldi r2 {y}\n")
                out.write(f"ldi r3 {p}\n")
                out.write("setpixel r1 r2 r3\n")

        out.write("dispflip\n\n")