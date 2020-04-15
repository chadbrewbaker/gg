from unittest import TestCase, skipIf
import pathlib
import re
import tempfile
import subprocess as sub
import os
import shutil as sh


class ExampleTest(TestCase):
    @skipIf(not pathlib.Path("examples").exists(), "Missing examples dir")
    def test_examples(self) -> None:
        remote = "REMOTE_TEST" in os.environ
        if remote:
            self.assertIn("AWS_SECRET_ACCESS_KEY", os.environ)
        for p in pathlib.Path("examples").iterdir():
            if p.suffix == ".py":
                print(f"Testing: {p.name}")
                with p.open() as f:
                    s = f.read()
                res = re.search("#.*ARGS: (.*)", s)
                self.assertIsNotNone(res)
                assert res is not None  # for mypy
                args = res.group(1).strip().split()

                res = re.search("#.*RESULT: (\\w*)", s)
                assert res is not None  # for mypy
                self.assertIsNotNone(res)
                result = res.group(1)
                print(args, result)

                with tempfile.TemporaryDirectory() as d:
                    py = sh.which("python3.7")
                    force = sh.which("gg-force")
                    assert py is not None
                    assert force is not None
                    sub.run(
                        cwd=d,
                        check=True,
                        args=[py, str(os.path.abspath(p)), "init"] + args,
                    )
                    a = [force]
                    if remote:
                        a.extend(["--jobs", "1", "--engine", "lambda"])
                    a.append("out")
                    sub.run(cwd=d, check=True, args=a)
                    with open(f"{d}/out") as f:
                        self.assertEqual(f.read().strip(), result)

