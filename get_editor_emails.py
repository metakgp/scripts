import argparse
import subprocess
import shlex

parser = argparse.ArgumentParser()
parser.add_argument("-p",
                    help="database password",
                    type=str)
args = parser.parse_args()

cmd = "mysql -u metakgp_user --database=metakgp_wiki_db --password=\"{}\" < get_editor_emails.sql >emails.csv".format(args.p)

process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = process.communicate(cmd.encode('utf-8'))
print(out.decode('utf-8'))
