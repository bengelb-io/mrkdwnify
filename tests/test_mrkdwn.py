from mrkdwnify import mrkdwnify
import os
from os import path, getcwd

delimiter = "===="

def test_mrkdwnify():
    fixtures_path = path.join(getcwd(), "tests/fixtures")
    filenames = os.listdir(fixtures_path)
    for filename in filenames:
        if filename == "escaping.mrkdwn":
            continue
        with open(path.join(fixtures_path, filename)) as file:
            test_case = file.read()
            test_input, expected = test_case.split(delimiter)
            output = mrkdwnify(test_input).strip()
            assert output.strip() == expected.strip()