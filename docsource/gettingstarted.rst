********************************************************************************
Getting Started
********************************************************************************

Beta Release install (Windows Only)
===================================

Get the latest release from: https://github.com/BlockResearchGroup/compas-RV2/releases

1. Install RV2

   Unzip the folder and open `RV2\dev` in explorer, right click on `install.bat` (.bat extension might be hidden) and choose `Run as Administrator`. Click `Yes` in the pop-up window.
   Installation is successful if you see following output.

   .. code-block:: none

        C:\Windows\system32>C:\Users\lichen7\compas-RV2\dist\RV2\dev\env\python.exe -m compas_rv2.install --plugin_path C:\Users\lichen7\compas-RV2\dist\RV2\dev\..\
        Installing PlugIn RV2 to Rhino PythonPlugIns.

        PlugIn RV2 Installed.

        Restart Rhino and open the Python editor at least once to make it available.
        installing compas_rv2
        Installing COMPAS packages to Rhino 6.0 IronPython lib:
        IronPython location: C:\Users\lichen7\AppData\Roaming\McNeel\Rhinoceros\6.0\Plug-ins\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\settings\lib

            compas               OK
            compas_rhino         OK
            compas_tna           OK
            compas_ags           OK
            compas_pattern       OK
            compas_rv2           OK
            compas_bootstrapper  OK

        Completed.

        C:\Windows\system32>pause
        Press any key to continue . . .

2. Activate RV2 toolbar in Rhino

   * Go to menu `Tools > Toolbar Layout...`.
   * In pop-up window, click `File > Open...`.
   * Then in file explorer, select `YOUR_RV2_FOLDER\dev\RV2.rui`.
   * Now you will see RhinoVAULT2 appears in rhino menu.


Known Issues
============

Following error might appear for fresh Rhino installations:

.. code-block:: none

        FileNotFoundError: [WinError 3] The system cannot find the path specified:
            'C:\Users\xxx\AppData\Roaming\McNeel\Rhinoceros\6.0\Plug-ins\PythonPlugins'

To fix this, run `EditPythonScript` once and restart Rhino.
