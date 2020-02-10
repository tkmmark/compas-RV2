if __name__ == '__main__':
    print('install compas_rv2')
    from compas_rhino.install import install
    from compas_rhino.install_plugin import install_plugin
    import compas_rv2

    packages = ['compas','compas_rhino','compas_tna','compas_ags','compas_pattern','compas_rv2']

    # rv_2_path = os.path.abspath(os.path.dirname(compas_rv2.__file__))
    # install_plugin('ui/Rhino/RV2')
    install(packages=packages)