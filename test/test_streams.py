import json
import unittest
import subprocess
from subprocess import Popen

from parameterized import parameterized

from singertools.check_tap import StdoutReader


def run_and_summarize(tap, config, catalog=None, state=None, debug=False):
    cmd = [tap, "--config", config]
    if state:
        cmd += ["--state", state]
    if catalog:
        cmd += ["--catalog", catalog]
    print("Running command {}".format(" ".join(cmd)))

    stderr = None if debug else subprocess.DEVNULL
    with Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=stderr,
        bufsize=1,
        universal_newlines=True,
    ) as tap:
        summarizer = StdoutReader(tap)
        summarizer.start()
        returncode = tap.wait()
        if returncode != 0:
            print("ERROR: tap exited with status {}".format(returncode))
            exit(1)

    return summarizer.summary


class TestEndpoint(unittest.TestCase):

    STREAM_LIST = ["sample_catalog"]

    @parameterized.expand(STREAM_LIST)
    def test_if_works(self, stream):
        package_name = "tap_produtos_crawler"
        run_and_summarize(
            tap="tap-produtos-crawler",
            config="config.json",
            catalog=f"{package_name}/catalogs/{stream}.json",
        )


if __name__ == "__main__":
    unittest.main()
