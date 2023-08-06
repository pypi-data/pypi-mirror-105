import datetime
import glob
import os
import time
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT

from .configuration import PlotmanConfig
from .plot_util import df_b


class FarmPlot:
    """
    The final state to move files from tmp folder to given hard drive devices
    """

    def __init__(self, cfg: PlotmanConfig):
        self.dsts = cfg.directories.dst
        self.checktmps = cfg.directories.tmp
        self.schedule = cfg.scheduling.polling_time_s

    def isAvailable(self, size) -> (bool, str):
        for d in self.dsts:
            lockFile = os.path.join(d, "antLock")
            if df_b(d) > size and not os.path.exists(lockFile):
                with open(lockFile, 'w') as f:
                    f.write("This disk is now in operation now.")
                    f.close()
                return (True, d, lockFile)
        return (False, "", "")

    def removeFile(self, lockedFile):
        file_to_rem = Path(lockedFile)
        file_to_rem.unlink()

    def checking(self):
        while True:
            try:
                files_x_list = []
                for tmp in self.checktmps:
                    path = "%s*.plot".format(tmp)
                    mylist = [f for f in glob.glob(path)]
                    files_x_list.extend(mylist)

                if len(files_x_list) > 0:
                    for file in files_x_list:
                        size = Path(file).stat().st_size
                        (a, vDir, lockFile) = self.isAvailable(size)
                        # is busy now?
                        if not a:
                            continue

                        filename, file_extension = os.path.splitext(os.path.basename(file))
                        source = file
                        destination = os.path.join(vDir, filename, file_extension)
                        t0 = datetime.datetime.now()
                        p = Popen(["mv", "-v", source, destination], stdout=PIPE, stderr=STDOUT)
                        output, error = p.communicate()
                        output = output.strip().decode("utf-8")
                        print("start moving file from temp folder to destination farm location")
                        if p.returncode:
                            print(f"E: {output}")
                            self.removeFile(lockFile)
                        else:
                            elapsed = (datetime.datetime.now() - t0).total_seconds()
                            self.removeFile(lockFile)
                            print(output)

                time.sleep(self.schedule)
            except ConnectionError as cc:
                print('got ConnectionError from io', cc)
                continue
            except ValueError as v:
                print('got ValueError from io', v)
                continue
            except TimeoutError as th:
                print('got TimeoutError from io', th)
                continue
            except IOError as io:
                print('got IOError from io', io)
                continue
