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
        help="Revision hash of the aas-core-meta repository; latest if omitted",
        # NOTE (mristin):
        # There is no way to retrieve the latest revision hash with HTTP from
        # GitHub without an access token, so we enforce that the revision must
        # be explicitly given by the operator.
        required=True,
    )
    args = parser.parse_args()

    revision = str(args.revision)

    url = (
        f"https://raw.githubusercontent.com/aas-core-works/"
        f"aas-core-meta/{revision}/aas_core_meta/v3_http.py"
    )

    this_dir = pathlib.Path(os.path.realpath(__file__)).parent

    print(f"Downloading from: {url}")
    target_pth = this_dir / "meta_model.py"
    try:
        urllib.request.urlretrieve(url, str(target_pth))
    except urllib.error.HTTPError as exception:
        print(f"Failed to download from: {url}:\n{exception}", file=sys.stderr)
        return 1

    try:
        text = target_pth.read_text(encoding="utf-8")
        target_pth.write_text(f"# Downloaded from: {url}\n\n{text}", encoding="utf-8")
    except Exception as exception:
        print(
            f"Failed to prepend the URL to the meta-model file {target_pth}: {exception}",
            file=sys.stderr,
        )
        return 1

    print("Re-generating the code...")
    dev_scripts.codegen.generate.generate()

    return 0


if __name__ == "__main__":
    sys.exit(main())
