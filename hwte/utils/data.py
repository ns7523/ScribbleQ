# Copyright (C) 2025, CraftIQ.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

# Adapted from https://github.com/pytorch/vision/blob/master/torchvision/datasets/utils.py

import hashlib
import logging
import os
import re
import urllib
import urllib.error
import urllib.request
from pathlib import Path

from tqdm.auto import tqdm
import requests  # ✅ added

__all__ = ["download_from_url"]

# matches bfd8deac from resnet18-bfd8deac.ckpt
HASH_REGEX = re.compile(r"-([a-f0-9]*)\.")
USER_AGENT = "mindee/hwte"


# ✅ FIXED FUNCTION — supports HTTP 308 redirects and tqdm progress
def _urlretrieve(url: str, filename: Path | str, chunk_size: int = 1024) -> None:
    headers = {"User-Agent": USER_AGENT}
    try:
        with requests.get(url, headers=headers, stream=True, allow_redirects=True, timeout=30) as response:
            response.raise_for_status()
            total = int(response.headers.get("content-length", 0))
            with open(filename, "wb") as fh, tqdm(
                total=total,
                unit="B",
                unit_scale=True,
                desc=f"Downloading {Path(filename).name}",
            ) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        fh.write(chunk)
                        pbar.update(len(chunk))
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to download {url}: {e}") from e


def _check_integrity(file_path: str | Path, hash_prefix: str) -> bool:
    with open(file_path, "rb") as f:
        sha_hash = hashlib.sha256(f.read()).hexdigest()

    return sha_hash[: len(hash_prefix)] == hash_prefix


def download_from_url(
    url: str,
    file_name: str | None = None,
    hash_prefix: str | None = None,
    cache_dir: str | None = None,
    cache_subdir: str | None = None,
) -> Path:
    """Download a file using its URL

    >>> from hwte.models import download_from_url
    >>> download_from_url("https://yoursource.com/yourcheckpoint-yourhash.zip")
    """
    if not isinstance(file_name, str):
        file_name = url.rpartition("/")[-1].split("&")[0]

    cache_dir = (
        str(os.environ.get("hwte_CACHE_DIR", os.path.join(os.path.expanduser("~"), ".cache", "hwte")))
        if cache_dir is None
        else cache_dir
    )

    # Check hash in file name
    if hash_prefix is None:
        r = HASH_REGEX.search(file_name)
        hash_prefix = r.group(1) if r else None

    folder_path = Path(cache_dir) if cache_subdir is None else Path(cache_dir, cache_subdir)
    file_path = folder_path.joinpath(file_name)

    # Check file existence
    if file_path.is_file() and (hash_prefix is None or _check_integrity(file_path, hash_prefix)):
        logging.info(f"Using downloaded & verified file: {file_path}")
        return file_path

    try:
        # Create folder hierarchy
        folder_path.mkdir(parents=True, exist_ok=True)
    except OSError:
        error_message = f"Failed creating cache directory at {folder_path}"
        if os.environ.get("hwte_CACHE_DIR", ""):
            error_message += " using path from 'hwte_CACHE_DIR' environment variable."
        else:
            error_message += (
                ". You can change default cache directory using 'hwte_CACHE_DIR' environment variable if needed."
            )
        logging.error(error_message)
        raise

    # Download the file
    try:
        print(f"Downloading {url} to {file_path}")
        _urlretrieve(url, file_path)
    except (urllib.error.URLError, IOError) as e:
        if url[:5] == "https":
            url = url.replace("https:", "http:")
            print(f"Failed download. Trying https -> http instead. Downloading {url} to {file_path}")
            _urlretrieve(url, file_path)
        else:
            raise e

    # Remove corrupted files
    if isinstance(hash_prefix, str) and not _check_integrity(file_path, hash_prefix):
        os.remove(file_path)
        raise ValueError(f"corrupted download, the hash of {url} does not match its expected value")

    return file_path
