from __future__ import annotations

class Parser:
    @staticmethod
    def read_bytes(file: str) -> tuple[str, list[str]]:
        res = ""
        with open(file, "rb") as f:
            byte = f.read(1)
            while byte != b"":
                res += byte.decode("utf-8")
                byte = f.read(1)

        res = res.replace("\n", "").replace("(", "").replace(")", "")[1:]
        res = res.split(";")

        return res[0], res[1:]

