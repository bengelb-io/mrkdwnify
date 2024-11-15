from markdownify import MarkdownConverter, ATX, ASTERISK
from mrkdwn import mrkdwnify

from os import path, getcwd, listdir

delimiter = "===="


def test_mrkdwnify():
    fixtures_path = path.join(getcwd(), "tests/fixtures")
    filenames = listdir(fixtures_path)
    for filename in filenames:
        with open(path.join(fixtures_path, filename)) as file:
            test_case = file.read()
            test_input, expected = test_case.split(delimiter)
            # print(f"Input: {test_input.strip()}", f"Expected: {test_output.strip()}")
            output = mrkdwnify(test_input).strip()
            outcome = output.strip() == expected.strip()
            if filename == "img.mrkdwn":
                print("output", output)
                print("expected", expected)
            print("Testing: ", filename, outcome)


if __name__ == "__main__":
    html = '<p>Hello this is an inline link! <a href="https://www.example.com">Example</a></p>'
    link = '<a href="https://www.example.com">Example</a><a href="https://www.example.com">Example</a>'
    test_case = """
Hi 👋<br><br><b>Pending approval request from Oracle Fusion</b><br><br><b>Purchase Requisition (View Only): Invoice</b><br><br><br><ul><li><i><b>Approval Requested by: </b><a href="https.oracle.com"> jyoti@dropbox.com </a></i></li><li><i><b>Approval Requested Date: </b>09/13/2024 </i></li><li><i><b>Pending for: </b> 7 days</i></li><li><i><b>Transaction date: </b>09/13/2024</i></li><li><i><b>Total Amount: </b>100.00 USD</i></li><li><i><b>Requester: </b>Jyoti</i></li><li><i><b>Description: </b>Invoice Details</i></li></ul><br><br><br><b>Action: 👉<u><a href=https://ecxo.test.fa.us2.oraclecloud.com/integration/worklistapp/faces/home.jspx>Click to Approve in Oracle</a></u></b>"""
    mrkdwn = mrkdwnify(test_case)
    print(mrkdwn)
    # test_mrkdwnify()
