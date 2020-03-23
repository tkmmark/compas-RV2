from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas_rhino.artists import MeshArtist



__all__ = ['MeshArtist']


class MeshArtist(MeshArtist):
    """A customised `MeshArtist` for RV2 `Mesh`-based data structures."""

    # def draw_vertexlabels(self, text, color):
    #     if isinstance(text, dict):
    #         keys = list(text.keys())
    #     else:
    #         keys = list(self.mesh.vertices())
    #     guids = super(MeshArtist, self).draw_vertexlabels(text=text, color=color)
    #     return list(zip(guids, keys))

    # def draw_edgelabels(self, text, color):
    #     if isinstance(text, dict):
    #         keys = list(text.keys())
    #     else:
    #         keys = list(self.mesh.edges())
    #     guids = super(MeshArtist, self).draw_edgelabels(text=text, color=color)
    #     return list(zip(guids, keys))

    # def draw_facelabels(self, text, color):
    #     if isinstance(text, dict):
    #         keys = list(text.keys())
    #     else:
    #         keys = list(self.mesh.faces())
    #     guids = super(MeshArtist, self).draw_facelabels(text=text, color=color)
    #     return list(zip(guids, keys))

    # def draw_vertexnormals(self, color, scale):
    #     keys = list(self.mesh.vertices())
    #     guids = super(MeshArtist, self).draw_vertexnormals(keys=keys, color=color, scale=scale)
    #     return list(zip(guids, keys))

    # def draw_facenormals(self, color, scale):
    #     keys = list(self.mesh.faces())
    #     guids = super(MeshArtist, self).draw_facenormals(keys=keys, color=color, scale=scale)
    #     return list(zip(guids, keys))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
