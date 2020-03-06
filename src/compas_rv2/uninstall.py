if __name__ == '__main__':
    print('uninstalling compas_rv2')
    from compas_rhino.uninstall import uninstall
    from compas_rhino.uninstall_plugin import uninstall_plugin
    import compas_rv2

    packages = ['compas_rv2']
    uninstall_plugin('RV2')
    uninstall(packages=packages)