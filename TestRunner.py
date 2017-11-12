import glob
import os
import sys
from os.path import basename


def main():
    filelist = glob.glob("./config/targets/aborgardt.badWAF/*.json")
    runconfigPath = "aborgardt.badWAF/"
    rounds = 25
    generators = ["smarty", "dharma"]
    runtests = ['', '--enableWebdriver']

    for round in range(0, rounds):
        for rt in runtests:
            for runconfig in filelist:
                for generator in generators:
                    logfile = basename(runconfig)

                    path = "reflected/"
                    if rt:
                        path = "executed/"

                    command = "python SmartGrazer.py -x " + runconfigPath + basename(
                        runconfig) + " -c " + rt + " --overwrite smartgrazer.imps.smithy.generator=" + generator + " smartgrazer.logging.logfile=logs/" + runconfigPath + path + "R" + str(
                        round) + "/" + generator + "/" + logfile + ".log"

                    os.system(command)


if __name__ == "__main__":
    sys.exit(main())
