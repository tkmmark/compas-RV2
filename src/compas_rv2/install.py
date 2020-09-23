import compas
import compas_rhino
from compas_rhino.install import install
from compas_rhino.uninstall import uninstall
from compas_rhino.install_plugin import install_plugin
from compas_rhino.uninstall_plugin import uninstall_plugin
import argparse
import os
import json

if __name__ == '__main__':

    packages = ['compas', 'compas_rhino', 'compas_tna', 'compas_cloud', 'compas_skeleton', 'compas_singular', 'compas_rv2']

    import importlib

    print("\n", "-"*10, "Checking packages", "-"*10)
    for p in packages:
        try:
            importlib.import_module(p)
            print('   {} {}'.format(p.ljust(20), "OK"))
        except ImportError as e:
            print(p, "ERROR: cannot be imported, make sure it is installed")
            raise ImportError(e)

    parser = argparse.ArgumentParser(
        description='RhinoVault2 Installation command-line utility.')

    parser.add_argument('--dev', action='store_true', help="install dev version of RV2 from current env")
    parser.add_argument('--remove_plugins', action='store_true', help="remove all existing plugins")
    parser.add_argument('--plugin_path', help="The path to the plugin directory.")
    args = parser.parse_args()

    if args.remove_plugins:
        print("\n", "-"*10, "Removing existing plugins", "-"*10)
        python_plugins_path = compas_rhino._get_python_plugins_path("6.0")
        print("Plugin location: ", python_plugins_path)
        plugins = os.listdir(python_plugins_path)
        for p in plugins:
            uninstall_plugin(p, version="6.0")

    # print("\n", "-"*10, "Removing existing packages", "-"*10)
    # uninstall()

    print("\n", "-"*10, "Installing RV2 python plugin", "-"*10)
    if args.dev:
        plugin_path = os.path.join(os.path.dirname(__file__), "..", "..", 'ui/Rhino/RV2')
        plugin_path = os.path.abspath(plugin_path)
    elif args.plugin_path:
        plugin_path = args.plugin_path

    if os.path.exists(plugin_path):
        install_plugin(plugin_path, version="6.0")
    else:
        raise RuntimeError("%s does not exist" % plugin_path)

    print("\n", "-"*10, "Installing COMPAS packages", "-"*10)

    install(packages=packages)

    print("\n", "-"*10, "Installation is successful", "-"*10)

    print("\n", "-"*10, "Registering Installation", "-"*10)

    os.makedirs(compas.APPDATA, exist_ok=True)
    register_json_path = os.path.join(compas.APPDATA, "compas_plugins.json")
    if os.path.exists(register_json_path):
        register_json = json.load(open(register_json_path))
    else:
        register_json = {"Plugins": [], "Current": "dev"}

    if args.dev:
        register_json["Current"] = "dev"
        print("    Registered as dev installation")

    else:

        if args.plugin_path:
            plugin_path = os.path.abspath(args.plugin_path)
        else:
            plugin_path = os.path.join(os.getcwd(), "..")
            plugin_path = os.path.abspath(plugin_path)

        print("registering to", register_json_path)

        if plugin_path not in register_json["Plugins"]:
            register_json["Plugins"].append(plugin_path)

        register_json["Current"] = plugin_path

        print(" "*4, plugin_path, "is registered")

    for plugin_path in register_json["Plugins"]:
        if not os.path.exists(plugin_path):
            register_json["Plugins"].remove(plugin_path)
            print("    Removed un-existed path: ", plugin_path)

    json.dump(register_json, open(register_json_path, "w"), indent=4)

    print("\n", "-"*10, "Installation is Registered", "-"*10)
