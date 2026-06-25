# MP3 Compression Tool
"""
Target	Use this
low	         64k
voice	     96k
podcast	    128k
good	    160k
high	    192k
very high	256k
max	        320k
"""
# Requires ffmpeg installed:
#   Mac:     brew install ffmpeg
#   Linux:   sudo apt install ffmpeg
#   Windows: https://ffmpeg.org/download.html

import os
import time
import argparse
import multiprocessing
from multiprocessing import freeze_support
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="MP3 bulk compressor")
    parser.add_argument("folder", help="Root folder containing lower subfolder and MP3 files to compress")
    parser.add_argument("bitrate", nargs="?", default="192k", help="Target bitrate (default: 192k)"    )
    return parser.parse_args()

def compress_mp3(args):
    mp3_path, bitrate = args
    size_before = os.path.getsize(mp3_path)
    temp_file = mp3_path + ".tmp.mp3"
    cmd = [
        "ffmpeg",
        "-y",                 # overwrite temp file
        "-i",   mp3_path,
        "-b:a", bitrate,
        temp_file
    ]
    subprocess.run(cmd, capture_output=True, text=True)

    os.replace(temp_file, mp3_path)
    size_after = os.path.getsize(mp3_path)
    return (os.path.basename(mp3_path), size_before, size_after)

def scan_folder(folder_path):
    mp3_files = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(".mp3"):
                mp3_files.append(os.path.join(root, file_name))
                print(f"   - Found: '{file_name}' at '{root}' \n")
    return mp3_files

def format_size(bytes):
    if bytes < 1024 * 1024:
        return f"{bytes / 1024:.1f} KB"
    else:
        return f"{bytes / (1024 * 1024):.1f} MB"

def batch_compress(folder_path, bitrate="192k"):
    mp3_files = scan_folder(folder_path)
    print(f"- Found a total of: {len(mp3_files)} MP3 file(s)")
    tasks = [(mp3_file, bitrate) for mp3_file in mp3_files] # gathers tuples of (file + bitrate) data per each found file
    start_time = time.time()
    
    with multiprocessing.Pool(os.cpu_count()) as pool:
        results = pool.map(compress_mp3, tasks) # passes each (file + bitrate) to compress_mp3 method to execute compression on each
    
    elapsed = time.time() - start_time
    print("\nCompression Summary:")
    print("-" * 90)
    print(f"{'File':<60} {'Before':>12} {'After':>12}") # :<XX means padding spaces to the left
    print("-" * 90)

    for file_name, before, after in results:
        print(f"{file_name:<60} {format_size(before):>12} {format_size(after):>12}")
        #print(f"{format_size(file_name):<60}", f"{format_size(before):>12}", f"{format_size(after):>12}")
    
    print("-" * 90)
    print(f"  - Completed in {elapsed:.1f} seconds")


if __name__ == "__main__":
    freeze_support()
    args = parse_args()
    print("MP3 Bulk file Compressor -----------------------------------------------------------------")
    print(f"Source Folder: {args.folder}")
    print(f"Bitrate      : {args.bitrate} \n")
    batch_compress(args.folder, args.bitrate)