#!/usr/bin/python3
from json import loads
from os import system, getcwd, getlogin,path
from sys import exit
import logging

__version__ = "1.0.0"
exc_msg = lambda e: e if len(e.args) == 1 else e.args[1]


class main:
    def __init__(
        self,
        key: str,
        key_path: str,
        username: str,
        key_id: str,
        message: str,
        file: str,
        log_level: int,
        log_file: str,
    ):
        self.key = key
        self.key_path = key_path
        self.username = username
        self.key_id = key_id
        self.message = message
        self.file = file
        log_config = {
            "format": "[%(asctime)s] - %(levelname)s : %(message)s",
            "datefmt": "%H:%M:%S %d-%b-%Y",
        }
        if log_file:
            log_config["filename"] = log_file
        log_config["level"] = log_level
        logging.basicConfig(**log_config)

    def get_key(self):
        """gets the github token"""
        if self.key_path:
            try:
                with open(self.key_path) as fp:
                    rp = loads(fp.read())[self.key_id]
            except Exception as e:
                exit(logging.critical(exc_msg(e)))
        else:
            rp = self.key
        if not rp:
            exit(logging.critical("[*] Authentication Token is required!"))
        return rp

    def get_curdir(self):
        """gets the current dir"""
        resp = getcwd().split("/")[-1]
        return resp

    def get_commit_argument(self):
        """Gets commit message"""
        if any([self.message, self.file]):
            if self.message:
                rp = f'-m "{self.message}"'
            else:
                rp = f'-F "{self.file}"'
        else:
            exit(logging.critical("Commit message not found!"))
        return rp

    def run(self, files: str, site: str):
        """Main method"""
        msg_argument = self.get_commit_argument()
        repo_name = self.get_curdir()
        commands = {
            "Adding files": f"git add {files}",
            "Committing": f"git commit {msg_argument}",
            f'Pushing to "https://{site}/{self.username}/{repo_name}"': f"git push https://{self.username}:{self.get_key()}@{site}/{self.username}/{repo_name}.git",
        }
        system_run = lambda cmd: system(cmd)
        for key, val in commands.items():
            if val:
                logging.info(key)
                logging.debug(val)
                system_run(val)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Automate pushing files to remote - GitHub",
        epilog='[*] "Build by developers for developers"',
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s v{__version__}"
    )
    parser.add_argument("files", help="File(s) to be committed")
    parser.add_argument(
        "-u",
        "--username",
        help="Github account username - [current-user]",
        default='Simatwa', #
        metavar="name",
    )
    parser.add_argument(
        "-t", "--token", nargs="?", help="Github authentication key", metavar="key"
    )
    parser.add_argument(
        "-p",
        "--token-path",
        nargs="?",
        dest="token_path",
        help="Path to json file containing github token",
        metavar="path",
        default=path.join(path.expanduser('~'),'.key.json') #
    )
    parser.add_argument(
        "-i",
        "--key-id",
        help="Key-name to github token contained in the token-path - [github]",
        dest="key_id",
        default="github",
        metavar="id",
    )
    parser.add_argument("-m", "--message", help="Message to be committed along with")
    parser.add_argument(
        "-F",
        "--file",
        help="File-Path containing message to be committed along with",
        metavar="path",
    )
    parser.add_argument(
        "-l",
        "--level",
        help="Default logging level",
        choices=[10, 20, 30, 40, 50],
        metavar="10|20|30|40|50",
        default=20,
        type=int,
    )
    parser.add_argument(
        "-s",
        "--site",
        help="The version control site - [github.com]",
        default="github.com",
    )
    parser.add_argument("-o", "--output", help="Filepath to log to")
    args = parser.parse_args()
    start = main(
        key=args.token,
        key_path=args.token_path,
        username=args.username,
        key_id=args.key_id,
        message=args.message,
        file=args.file,
        log_level=args.level,
        log_file=args.output,
    )
    start.run(args.files, args.site)
