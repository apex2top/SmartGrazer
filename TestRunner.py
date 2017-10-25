import subprocess

import os

if __name__ == "__main__":
    command = "SmartGrazer.py -c -x {RUNCONFIG} --overwrite smartgrazer.imps.smithy.generator={GENERATOR} smartgrazer.imps.webber.timelimit={TIMELIMIT}"

    generator = ["dharma","smarty"]
    timelimit = [5, 10, 15]
    runconfigs = ["aborgardt.bwapp/level-0.json", "aborgardt.bwapp/level-1.json"]#, "aborgardt.bwapp/level-2.json"]

    for t in timelimit:
        for g in generator:
            for r in runconfigs:
                print("Running: " + r + " -> " + g + " for " + str(t))
                cmd = 'python ' + command.replace("{RUNCONFIG}",r).replace("{GENERATOR}",g).replace("{TIMELIMIT}",str(t))
                os.system(cmd)