# !/usr/bin/env python3
import os
from string import Template

servers = [61, 62, 63, 64, 66, 67, 68, 69, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]
storage1 = [236, 237, 238, 239, 240, 241, 242, 243]
storage2 = [101, 102, 103, 104, 105, 106, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130]
dst = "/Users/hesdx/Documents/ipfs/deplotplot/workers"

c = 0

t = """

user_interface:
        use_stty_size: True
directories:
        log: /home/ipant/.chia/mainnet
        tmp:
                - /mnt/local/tmp
        tmp_overrides:
                "/mnt/local/tmp":
                        tmpdir_max_jobs: 30
        dst:
                - /mnt/nfs/{name1}/chiaFinalData
                - /mnt/nfs/{name2}/chiaFinalData
        archive:
                #rsyncd_module: plots
                #rsyncd_path: /plots
                #rsyncd_bwlimit: 80000  # Bandwidth limit in KB/s
                #rsyncd_host: myfarmer
                #rsyncd_user: chia
                #   index: 0
scheduling:
        tmpdir_stagger_phase_major: 2
        tmpdir_stagger_phase_minor: 3
        tmpdir_stagger_phase_limit: 25
        tmpdir_max_jobs: 40
        global_max_jobs: 90
        global_stagger_m: 20
        polling_time_s: 30
plotting:
        k: 32
        e: True              # Use -e plotting option
        n_threads: 4         # Threads per job
        n_buckets: 128       # Number of buckets to split data into
        job_buffer: 17068     # Per job memory
        # If specified, pass through to the -f and -p options.  See CLI reference.
        farmer_pk: 861467df6768932f1c2f3a7c00a70f1e111b22b55de42c497fb93fd398eb4fd4b213f399e0930d265ffdc2b5655f96f5
        pool_pk: 8e211cb1118b95ac9da2f31fd159a74993bfcc8ab72bff79c880227185ba2b1f372b8e829bd99f5796eb4f68e41f30a9

apis:
        port: 19992
        api_polling_throttle_s: 5
        """


def filename(k) -> str:
    if k < len(storage1):
        u = storage1[k]
        return "storage{}".format(u)
    else:
        p = storage2[k - len(storage1)]
        return "ipant{}".format(p)


for i in servers:
    FileName = "worker{}.yaml".format(i)
    file = os.path.join(dst, FileName)
    disk1It = filename(c * 2)
    disk2It = filename(c * 2 + 1)
    s = t.format(name1=disk1It, name2=disk2It)
    with open(file, 'w') as f:
        f.write(s)
        f.close()
    c += 1
