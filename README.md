# compas-RV2

RhinoVault for Rhino 6 based on COMPAS

## Beta release install
Instructions here: [INSTALLATION.md](INSTALLATION.md)

## Dev install

These installation instructions assume that Anaconda/conda are available on your system.

1. Set up a dedicated `conda` environment.

   On Windows.

   ```bash
   conda create -n rv2 python=3.7
   ```

   On Mac, also install Python as a framework (add ``python.app``).

   ```bash
   conda create -n rv2 python=3.7 python.app
   ```

2. Activate the environment.

   Whenever you work on `compas-RV2`, the `rv2` environment should be active.

   ```bash
   conda activate rv2
   ```

   > When an environment is active, the command line will start with the name of that environment in parenthesis: `(rv2)...>` (Windows) or `(rv2)...$` (Mac).

3. Install requirements.

   Since no requirements are explicitly listed in a "requirements" file, we will install all required packages manually "from source".
   Therefore, for each of `compas`, `compas_ags`, `compas_tna`, `compas_pattern`, `compas_triangle`, `compas_skeleton`, and `compas_cloud` navigate to the root of the corresponding repo, and do

   ```bash
   pip install -e .
   ```

   To verify, open an interactive Python prompt and import the installed packages.

   ```python
   >>> import compas
   >>> import compas_ags
   >>> import compas_tna
   >>> import compas_pattern
   >>> import compas_cloud
   >>> import compas_triangle
   >>> import compas_skeleton
   >>> exit()
   ```

4. Install RV2.

   Navigate to the root of `compas-RV2` and do

   ```bash
   pip install -e .
   ```

   To verify, open an interactive Python prompt and import the installed package.

   ```python
   >>> import compas_rv2
   >>> exit()
   ```

5. Install all packages for Rhino.

   From the root of `compas-RV2`, do

   ```bash
   python -m compas_rhino.install -p compas compas_rhino compas_ags compas_tna compas_pattern compas_rv2 compas_cloud compas_triangle
   ```

6. Install RV2 command plugin.

   From the root of `compas-RV2`, do

   ```bash
   python -m compas_rhino.install_plugin ui/Rhino/RV2
   ```

7. Test the installation.

   In Rhino, type `RV2init`.
   This should display the RhinoVault2 welcome page.

   > (Windows) If the command does not appear in the list of possible commands, you may have to open and close the Python Script Editor to initialise the plugin.

   A full list of available commands can be found [here](commands.html).

## Notes

`ui/Rhino/RV2/dev` contains `RV2.rui`, which defines the Rhino UI for RhinoVault2 on Windows. the file is generated using `rui.py` (command line: `python ui/Rhino/RV2/dev/rui.py`). part of its configuration is in `config.json`, part is in `rui.py`.

on windows, the .rui file can be dragged into Rhino to load the toolbar. on mac, there is no equivalent mechanism. the toolbar has to be created manually and, as far as i know, can't be shared.

just fyi, the .rui file can be converted to a .plist file using the `TestEditToolPaletteCollection` command. you can see the contents of the .plist file in the editor and even update it, but you can't load the palette and use it.
