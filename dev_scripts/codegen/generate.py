"""Generate the code of the SDK based on the meta-model and the snippets."""

import argparse
import os
import pathlib
import subprocess
import sys

def generate() -> None:
    """Generate the code."""
    this_dir = pathlib.Path(os.path.realpath(__file__)).parent
    snippets_dir = this_dir / "snippets"
    meta_model_path = this_dir / "meta_model.py"

    cmd = [
        sys.executable,
        "-m",
        "aas_core_codegen",
        "--model_path",
        str(meta_model_path),
        "--snippets_dir",
        str(snippets_dir),
        "--output_dir",
        str(this_dir.parent.parent / "aas_core3_http"),
        "--target",
        "python"
    ]

    subprocess.check_call(cmd, cwd=str(this_dir))

def main() -> int:
    """Execute the main routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    generate()

    return 0


if __name__ == "__main__":
    sys.exit(main())
