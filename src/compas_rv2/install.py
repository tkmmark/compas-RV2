if __name__ == '__main__':

    import compas_rhino
    from compas_rhino.install import install
    from compas_rhino.uninstall import uninstall
    from compas_rhino.install_plugin import install_plugin
    from compas_rhino.uninstall_plugin import uninstall_plugin
    import argparse
    import os


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

    print("\n", "-"*10, "Removing existing packages", "-"*10)
    uninstall()

    print("\n", "-"*10, "Installing RV2 python plugin", "-"*10)
    if args.dev:
        install_plugin('ui/Rhino/RV2', version="6.0")
    elif args.plugin_path:
        install_plugin(args.plugin_path, version="6.0")

    print("\n", "-"*10, "Installing COMPAS packages", "-"*10)

    packages = ['compas', 'compas_rhino', 'compas_tna', 'compas_cloud', 'compas_skeleton', 'compas_singular', 'compas_rv2']
    install(packages=packages)
