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

import os
import pytest

from .. import kubectl
from pathlib import Path
from unittest.mock import ANY


@pytest.mark.parametrize(
    "cmd,exit_status",
    [
        ("", 0),
        ("version --client --short", 0)
    ]
)
def test_commands(cmd, exit_status):

    """Tests a handful of simple scenarios"""

    res = kubectl(cmd)
    assert res.exit_status == exit_status


@pytest.mark.parametrize(
    "actual_cmd, expected_cmd, kubectl_exec",
    [
        ("", ["kubectl"], None)
        , ("", ["/bin/kubectl"], "/bin/kubectl")
        , ("", ["/bin/kubectl"], Path("/bin/kubectl"))
        , ("get pods", ["kubectl", "get", "pods"], None)
        , (["get", "pods"], ["kubectl", "get", "pods"], None)
        , (["get", "pods"], ["/bin/kubectl", "get", "pods"], "/bin/kubectl")
        , (["get", "pods"], ["/bin/kubectl", "get", "pods"], Path("/bin/kubectl"))
        , ("/foo/bar/kubectl get pods", ["/foo/bar/kubectl", "get", "pods"], Path("/bin/kubectl"))
    ]
)
def test_add_kubectl_exec(mocker, actual_cmd, expected_cmd, kubectl_exec):
    run = mocker.patch("kubectl.run")
    res = kubectl(actual_cmd, kubectl_exec=kubectl_exec)

    run.assert_called_once_with(
        args=expected_cmd,
        check=False,
        close_fds=True,
        cwd=ANY,
        env=ANY,
        shell=False,
        stdout=ANY,
        stderr=ANY
    )


@pytest.mark.parametrize(
    "cwd,expected_cwd",
    [
        (None, None)
        , ("/tmp", Path("/tmp"))
        , (Path("/tmp"), Path("/tmp"))
    ]
)
def test_cwd_set(mocker, cwd, expected_cwd):
    run = mocker.patch("kubectl.run")
    res = kubectl("version --client --short", cwd=cwd)

    assert res.cwd == expected_cwd
    run.assert_called_once_with(
        args=ANY,
        check=False,
        close_fds=True,
        cwd=expected_cwd,
        env=ANY,
        shell=False,
        stdout=ANY,
        stderr=ANY
    )


@pytest.mark.parametrize(
    "env,expected_env",
    [
        (None, os.environ)
        , ({}, {})
        , ({"foo": "bar"}, {"foo": "bar"})
    ]
)
def test_env_set(mocker, env, expected_env):
    run = mocker.patch("kubectl.run")
    res = kubectl("version --client --short", env=env)

    assert res.env == expected_env
    run.assert_called_once_with(
        args=ANY,
        check=False,
        close_fds=True,
        cwd=ANY,
        env=expected_env,
        shell=False,
        stdout=ANY,
        stderr=ANY
    )
