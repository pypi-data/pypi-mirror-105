import subprocess


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_a28_no_param():
    command = ["a28"]
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    assert err == b'usage: a28 [-h] {build,install} ...\na28: error: the following arguments are required: action\n'


def test_a28_build_no_param():
    command = ["a28", "build"]
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    assert err == b'usage: a28 build [-h] --src SRC [--dest DEST]\na28 build: error: the following arguments are required: --src\n'


def test_a28_install_no_param():
    command = ["a28", "install"]
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    assert err == b'usage: a28 install [-h] --pkg PKG\na28 install: error: the following arguments are required: --pkg\n'
