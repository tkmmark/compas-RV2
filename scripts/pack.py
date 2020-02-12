import conda_pack
import os
import shutil
import time


import argparse

parser = argparse.ArgumentParser(
    description='RhinoVault2 release package tool.')

parser.add_argument('--skip_packing',action='store_false', help="The path to the plugin directory.")
parser.add_argument('--format',default='zip', help="The path to the plugin directory.")

args = parser.parse_args()


start = time.time()
conda_pack.pack(output="env.zip", verbose=True, n_threads=-1, force=True)

print('unpacking to ui/Rhino/RV2/dev/env')
shutil.unpack_archive("env.zip", "ui/Rhino/RV2/dev/env")

if args.skip_packing:

    print('finished, took %s s'%(time.time()-start))
    print('packing skipped, go to ui/Rhino/RV2/dev and run install.bat')

else:

    os.remove("env.zip")
    print('re-packing whole plugin')
    shutil.make_archive( "RV2", "zip", "ui/Rhino/RV2/dev")
    shutil.rmtree("ui/Rhino/RV2/dev/env")
    os.rename("RV2.zip","RV2.%s"%args.format)

    print('finished, took %s s'%(time.time()-start)) 