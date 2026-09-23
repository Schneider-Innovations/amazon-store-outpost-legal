"""Verify the exact admitted local Review workflow in the current tree."""

import hashlib
import subprocess


PATH = ".github/workflows/codex-cli-review-receipt.yml"
POLICY_LINE = b"              '487b8e2d43db74160c50b6e76b9ca7b99dfd5591d7719c5807e2181387921d61',\n"
EXPECTED_BLOB = "40dd0e5e977f3acfb5e90ea662856e613aeae190"


def main() -> None:
    source = subprocess.check_output(["git", "show", f"HEAD:{PATH}"])
    if source.count(POLICY_LINE) != 1:
        raise AssertionError("protected-base policy digest is missing or duplicated")
    actual = hashlib.sha1(f"blob {len(source)}\0".encode() + source).hexdigest()
    if actual != EXPECTED_BLOB:
        raise AssertionError(f"protected-base blob mismatch: {actual}")
    print(f"verified exact admitted Git blob: {actual}")


if __name__ == "__main__":
    main()
