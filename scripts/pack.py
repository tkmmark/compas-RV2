import conda_pack
import os
import shutil
import time

start = time.time()
conda_pack.pack(output="env.tar.gz", verbose=True, n_threads=-1, force=True)

print('unpacking to ui/Rhino/RV2/env')
shutil.unpack_archive("env.tar.gz", "ui/Rhino/RV2/env")
os.remove("env.tar.gz")

print('re-packing to rhi')
shutil.make_archive( "RV2", "zip", "ui/Rhino/")
shutil.rmtree("ui/Rhino/RV2/env")
os.rename("RV2.zip","RV2.rhi")

print('finished, took %s s'%(time.time()-start))