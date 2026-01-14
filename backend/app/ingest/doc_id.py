import hashlib


def make_doc_id(text: str) -> str:
    return hashlib.sha3_256(text.encode("utf-8")).hexdigest()
