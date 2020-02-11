if __name__ == '__main__':
    print('installing compas_rv2')
    from compas_rhino.install import install
    import compas_rv2

    packages = ['compas','compas_rhino','compas_tna','compas_ags','compas_pattern','compas_rv2']
    install(packages=packages)