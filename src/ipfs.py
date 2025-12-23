from requests import Session
from src.constants import IPFS_NODE_URL


class IPFSClient:
    base_url: str = IPFS_NODE_URL

    def __init__(self) -> None:
        self.session: Session = Session()

    def write(self, filename: str, data: str):
        files = {"file": (filename, data.encode("utf-8"))}
        res = self.session.post(f"{self.base_url}/api/v0/add", files=files)
        return res.json()

    def read(self, cid: str):
        params = {"arg": cid}
        res = self.session.post(f"{self.base_url}/api/v0/cat", params=params)
        return res.content.decode("utf-8")
