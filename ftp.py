import ftplib
from pathlib import Path


class FTP(ftplib.FTP):
    def __init__(self, host: str, port: int, username: str, password: str, sub_directory: Path = Path("")):
        super().__init__()
        self.host = host
        self.port = port
        self.username = username
        self.__password = password
        if sub_directory is None:
            sub_directory = Path("")
        self.sub_directory = sub_directory

    def upload(self, path: str, previous_target_directory: Path):
        self.connect(self.host, self.port)
        self.login(self.username, self.__password)

        path = Path(path)

        path_to_be_removed = previous_target_directory.absolute()
        for i in range(len(previous_target_directory.parts)):
            path_to_be_removed = path_to_be_removed.parent

        ftp_target_directory = self.sub_directory / path.parent.relative_to(path_to_be_removed)

        self._ensure_directory_exists(ftp_target_directory, self)
        with open(path, "rb") as f:
            pwd = self.pwd()
            self.cwd(str(ftp_target_directory))
            self.storbinary(f"STOR {path.name}", f)
            self.cwd(pwd)

        self.quit()

    @staticmethod
    def _ensure_directory_exists(path: Path, ftp_server: ftplib.FTP):
        # ftp_server should already be connected and logged in when this is called
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
