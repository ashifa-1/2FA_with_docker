#!/usr/bin/env python3
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

import base64
import subprocess
from cryptography.hazmat.primitives import serialization
from app.crypto_utils import sign_message, encrypt_with_public_key


def get_latest_commit_hash() -> str:
    """Return the latest commit hash (40-character hex)."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%H"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def load_private_key(path: str):
    with open(path, "rb") as f:
        pem_data = f.read()
    return serialization.load_pem_private_key(pem_data, password=None)


def load_public_key(path: str):
    with open(path, "rb") as f:
        pem_data = f.read()
    return serialization.load_pem_public_key(pem_data)


def main():
    commit_hash = get_latest_commit_hash()
    print(f"Latest commit hash: {commit_hash}")

    student_private_key = load_private_key("keys/student_private.pem")
    instructor_public_key = load_public_key("keys/instructor_public.pem")

    signature = sign_message(commit_hash, student_private_key)

    encrypted_signature = encrypt_with_public_key(signature, instructor_public_key)

    encoded = base64.b64encode(encrypted_signature).decode("ascii")
    print(encoded)

    with open("commit_proof.txt", "w") as f:
        f.write(encoded + "\n")

    print("Saved proof to commit_proof.txt")


if __name__ == "__main__":
    main()
