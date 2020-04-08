if __name__ == '__main__':

    from compas_rhino.install import install
    from compas_rhino.install_plugin import install_plugin
    import argparse

    parser = argparse.ArgumentParser(
        description='RhinoVault2 Installation command-line utility.')

    parser.add_argument('--dev', action='store_true', help="install dev version of RV2 from current env")
    parser.add_argument('--plugin_path', help="The path to the plugin directory.")
    args = parser.parse_args()

    if args.dev:
        install_plugin('ui/Rhino/RV2', version="6.0")
    elif args.plugin_path:
        install_plugin(args.plugin_path, version="6.0")

    print('installing compas_rv2')

    packages = ['compas', 'compas_rhino', 'compas_tna', 'compas_ags', 'compas_pattern', 'compas_cloud', 'compas_skeleton', 'compas_rv2']
    install(packages=packages)
