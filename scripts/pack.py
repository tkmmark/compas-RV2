import conda_pack
import os
import shutil
import time

start = time.time()
conda_pack.pack(output="env.zip", verbose=True, n_threads=-1, force=True)

print('unpacking to ui/Rhino/RV2/dev/env')
shutil.unpack_archive("env.zip", "ui/Rhino/RV2/dev/env")
os.remove("env.zip")

print('re-packing to rhi')
shutil.make_archive( "RV2", "zip", "ui/Rhino/RV2/dev")
shutil.rmtree("ui/Rhino/RV2/dev/env")
os.rename("RV2.zip","RV2.rhi")

print('finished, took %s s'%(time.time()-start))