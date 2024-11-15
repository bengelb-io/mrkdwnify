from mrkdwn import mrkdwnify
import os
from os import path, listdir, getcwd

delimiter = "===="

def test_mrkdwnify():
    fixtures_path = path.join(getcwd(), "tests/fixtures")
    filenames = os.listdir(fixtures_path)
    for filename in filenames:
        with open(path.join(fixtures_path, filename)) as file:
            test_case = file.read()
            print("Testing: ", filename)
            test_input, test_output = test_case.split(delimiter)
            # print(f"Input: {test_input.strip()}", f"Expected: {test_output.strip()}")
            assert mrkdwnify(test_input.strip()) == test_output.strip()