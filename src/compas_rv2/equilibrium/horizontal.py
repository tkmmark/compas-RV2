from compas_rv2.diagrams import FormDiagram
from compas_rv2.diagrams import ForceDiagram

from compas_tna.equilibrium import horizontal_nodal


__all__ = ['horizontal_nodal_proxy']


def horizontal_nodal_proxy(formdata, forcedata, *args, **kwargs):
    form = FormDiagram.from_data(formdata)
    force = ForceDiagram.from_data(forcedata)
    horizontal_nodal(form, force, *args, **kwargs)
    return form.to_data(), force.to_data()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
