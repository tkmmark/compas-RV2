import conda_pack
import os
import shutil
import time


import argparse

parser = argparse.ArgumentParser(description='RhinoVault2 release package tool.')
parser.add_argument('--skip_packing', action='store_true', help="skip packaging to dist folder")
parser.add_argument('--rhi', action='store_true', help="pack into rhi installer")
parser.add_argument('--version', default="v0.0.0", help="version number")

args = parser.parse_args()


start = time.time()
conda_pack.pack(output="env.zip", verbose=True, n_threads=-1, force=True)

print('unpacking to ui/Rhino/RV2/dev/env')
shutil.unpack_archive("env.zip", "ui/Rhino/RV2/dev/env")

print('removing unnecessary files')
for root, dirs, files in os.walk("ui/Rhino/RV2/dev/env"):

    for d in dirs:
        if d.find("node_modules") >= 0:
            shutil.rmtree(os.path.join(root, d))

    for f in files:
        if f.find("electron.zip") >= 0:
            os.remove(os.path.join(root, f))


if args.skip_packing:

    print('finished, took %s s' % (time.time()-start))
    print('packing skipped, go to ui/Rhino/RV2/dev and run install.bat(win) or install.command(mac)')

else:

    os.remove("env.zip")
    print('re-packing whole plugin')

    if os.path.exists("dist"):
        shutil.rmtree("dist")
        os.mkdir("dist")

    if args.rhi:
        shutil.make_archive("dist/RV2", "zip", "ui/Rhino/RV2/dev")
        os.rename("dist/RV2.zip", "dist/RV2.rhi")
    else:
        shutil.make_archive(f"dist/RV2_{args.version}", "zip", "ui/Rhino/RV2")

    shutil.rmtree("ui/Rhino/RV2/dev/env")

    print('finished, took %s s' % (time.time()-start))
