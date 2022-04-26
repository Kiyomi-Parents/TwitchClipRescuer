import os
from pathlib import Path

from yt_dlp import YoutubeDL

import ftp


def download_clip(
        url: str,
        output_template: str,
        target_directory: Path = "",
        ftp_server: ftp.FTP = None,
        delete_local: bool = False
):
    if not ftp_server and delete_local:
        return

    ydl_opts = {
        'outtmpl': f'{target_directory}/{output_template}'
    }

    def callback(path: str):
        if ftp_server is not None:
            ftp_server.upload(path, target_directory)

        if delete_local:
            os.remove(path)

    with YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_hook(callback)
        ydl.download([url])
