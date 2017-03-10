import subprocess
import shlex
import pandas as pd

# Batman is an exception as it is a fork of pywikibots and hence its history includes
# contributors to pywikibots.

base_url = "https://github.com/metakgp"
repos = ["mftp",
         "mfqp",
         "mcmp",
         "mfqp-source",
         "gyft",
         "naarad",
         "naarad-source",
         "Zoom",
         "eva",
         "kakashi",
         "blackjack",
         "FaceMail",
         "MetaBot",
         "scripts"
        ]

for repo in repos:
    cmds = [
            "git clone {}/{}".format(base_url, repo),
            "cd {}".format(repo),
            "git pull origin master".format(repo),
            "git log --pretty=\"%cn,%ce\" | sort | uniq > ../{}.csv".format(repo),
            # maintaining list of contributors to individual projects for verfication
            "git log --pretty=\"%cn,%ce\" | sort | uniq >> ../unsorted_contributors.csv".format(repo),
            "cd .."
            ]

    cmds = "\n".join(cmds)

    # See http://stackoverflow.com/a/38182313/1780891
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(cmds.encode('utf-8'))
    print(out.decode('utf-8'))


cmd = """
cat unsorted_contributors.csv | sort | uniq > contributors.csv
rm unsorted_contributors.csv
"""
process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = process.communicate(cmd.encode('utf-8'))
print(out.decode('utf-8'))
