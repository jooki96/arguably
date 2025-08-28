import gzip
import shutil
from arguably import command, arg, run, parg, main

@command("compress")
@main
@parg("src", help="Source file") 
@parg("dst", help="Destination .gz file")  
def compress(src, dst):
    with open(src, "rb") as f_in, gzip.open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"Compressed {src} -> {dst}")

@command("decompress")
@parg("src", help="Source .gz file") 
@parg("dst", help="Destination file") 
def decompress(src, dst):
    with gzip.open(src, "rb") as f_in, open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"Decompressed {src} -> {dst}")

if __name__ == "__main__":
    run()
