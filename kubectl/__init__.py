# Copyright 2018 Philip Lombardi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import shlex
import os

from pathlib import Path
from subprocess import run, PIPE
from typing import Dict, List, Optional, Sequence, NamedTuple, Union


class KubectlResult(NamedTuple):
    args: Sequence[str]
    env: Dict[str, str]
    cwd: Optional[Path]
    exit_status: int
    stdout: Optional[str]
    stderr: Optional[str]


def kubectl(args: Union[str, List[str]] = "",
            cwd: Union[str, Path] = None,
            env: Dict[str, str] = None,
            kubectl_exec: Path = None) -> KubectlResult:

    if isinstance(args, str):
        args = shlex.split(args)

    if isinstance(cwd, str):
        cwd = Path(cwd)

    if cwd and not cwd.is_dir():
        raise ValueError("kubectl 'cwd = {}' is not a directory".format(cwd))

    # It feels "nicer" to just write code such as kubectl("get pods")
    # instead of kubectl("kubectl get pods")
    if not args or not args[0].endswith("kubectl"):
        args.insert(0, str(kubectl_exec) if kubectl_exec else "kubectl")

    if env is None:
        env = {k: v for (k, v) in os.environ.items()}

    completed = run(args=args,
                    check=False,
                    close_fds=True,
                    cwd=cwd,
                    env=env,
                    shell=False,
                    stdout=PIPE,
                    stderr=PIPE)

    return KubectlResult(args=completed.args,
                         env=env,
                         cwd=cwd,
                         exit_status=completed.returncode,
                         stdout=completed.stdout.decode("utf-8"),
                         stderr=completed.stderr.decode("utf-8"))
