import ftplib
import os
from pathlib import Path

from yt_dlp import YoutubeDL


def download_clip(url: str, target_directory: Path, ftp_server: ftplib.FTP):
    def callback(path: str):
        ensure_directory_exists(target_directory, ftp_server)
        with open(path, "rb") as f:
            pwd = ftp_server.pwd()
            ftp_server.cwd(str(target_directory))
            ftp_server.storbinary(f"STOR {Path(path).name}", f)
            ftp_server.cwd(pwd)
        os.remove(path)

    with YoutubeDL() as ydl:
        ydl.add_post_hook(callback)
        ydl.download([url])


def ensure_directory_exists(path: Path, ftp_server: ftplib.FTP):
    pwd = ftp_server.pwd()
    try:
        ftp_server.cwd(str(path))
        ftp_server.cwd(pwd)
    except ftplib.error_perm:
        for i in range(len(path.parts) + 1):
            current_path = "/".join(path.parts[:i])
            try:
                ftp_server.mkd(current_path)
            except ftplib.error_perm:
                continue

    ftp_server.cwd(pwd)
