"""Update the ``meta_model.py`` to the revision of aas-core-meta."""

import argparse
import os
import pathlib
import sys
import urllib.request
import urllib.error

import dev_scripts.codegen.generate


def main() -> int:
    """Execute the main routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--revision",
        help="Revision hash of the aas-core-meta repository; latest if omitted"
    )
    args = parser.parse_args()

    revision = str(args.revision) if args.revision is not None else None

    url: str
    if revision is None:
        url = "https://raw.githubusercontent.com/aas-core-works/aas-core-meta/main/aas_core_meta/v3_http.py"
    else:
        url = f"https://raw.githubusercontent.com/aas-core-works/aas-core-meta/{revision}/aas_core_meta/v3_http.py"

    this_dir = pathlib.Path(os.path.realpath(__file__)).parent

    print(f"Downloading from: {url}")
    try:
        urllib.request.urlretrieve(url, str(this_dir / "meta_model.py"))
    except urllib.error.HTTPError as exception:
        print(f"Failed to download from: {url}:\n{exception}", file=sys.stderr)
        return 1

    print("Re-generating the code...")
    dev_scripts.codegen.generate.generate()

    return 0


if __name__ == "__main__":
    sys.exit(main())
