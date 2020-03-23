from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas_rv2.rhino.artists.meshartist import MeshArtist


__all__ = ['ThrustArtist']


class ThrustArtist(MeshArtist):
    """A customised `MeshArtist` for the RV2 `ThrustDiagram`."""

    def draw_reactions(self, keys, color, scale):
        """Draw the reaction forces at the anchored vertices of the diagram.

        Parameters
        ----------
        color : list or tuple
            The RGB color specification for reaction forces.
            The specification must be in integer format, with each component between 0 and 255.
        scale : float
            The scaling factor for the reaction force vectors.

        Returns
        -------
        list
            A list of tuples, with each tuple containing a vertex identifier
            paired with the guid of the corresponding reaction force vector in Rhino.

        Notes
        -----
        The reaction forces are the opposite of residual forces at anchored vertices.
        The residual force components are stored per vertex in the `rx`, `ry`, and `rz` attributes.

        """
        lines = []
        for key in keys:
            a = self.mesh.vertex_attributes(key, 'xyz')
            r = self.mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
            b = add_vectors(a, scale_vector(r, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': color,
                'arrow': "start"
            })
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids

    def draw_vertical_reactions(self, keys, color, scale):
        """Draw the vertical components of the reaction forces at the anchored vertices of the diagram.

        Parameters
        ----------
        color : list or tuple
            The RGB color specification for reaction forces.
            The specification must be in integer format, with each component between 0 and 255.
        scale : float
            The scaling factor for the reaction force vectors.

        Returns
        -------
        list
            A list of tuples, with each tuple containing a vertex identifier
            paired with the guid of the corresponding reaction force vector in Rhino.

        Notes
        -----
        The reaction forces are the opposite of residual forces at anchored vertices.
        The residual force components are stored per vertex in the `rx`, `ry`, and `rz` attributes.

        """
        lines = []
        for key in keys:
            a = self.mesh.vertex_attributes(key, 'xyz')
            r = self.mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
            b = add_vectors(a, scale_vector([0, 0, r[2]], scale))
            lines.append({
                'start': a,
                'end': b,
                'color': color,
                'arrow': "start"
            })
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids

    def draw_residuals(self, keys, color, scale):
        """Draw the vertical component of the residual forces at the non-anchored vertices of the diagram.

        Parameters
        ----------
        color : list or tuple
            The RGB color specification for residual forces.
            The specification must be in integer format, with each component between 0 and 255.
        scale : float
            The scaling factor for the residual force vectors.

        Returns
        -------
        list
            A list of tuples, with each tuple containing a vertex identifier
            paired with the guid of the corresponding residual force vector in Rhino.

        Notes
        -----
        The residual force components are stored per vertex in the `rx`, `ry`, and `rz` attributes.

        """
        lines = []
        for key in keys:
            a = self.mesh.vertex_attributes(key, 'xyz')
            r = self.mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
            b = add_vectors(a, scale_vector(r, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': color,
                'arrow': "start"
            })
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids

    def draw_vertical_residuals(self, keys, color, scale):
        """Draw the vertical component of the residual forces at the non-anchored vertices of the diagram.

        Parameters
        ----------
        color : list or tuple
            The RGB color specification for residual forces.
            The specification must be in integer format, with each component between 0 and 255.
        scale : float
            The scaling factor for the residual force vectors.

        Returns
        -------
        list
            A list of tuples, with each tuple containing a vertex identifier
            paired with the guid of the corresponding residual force vector in Rhino.

        Notes
        -----
        The residual force components are stored per vertex in the `rx`, `ry`, and `rz` attributes.

        """
        lines = []
        for key in keys:
            a = self.mesh.vertex_attributes(key, 'xyz')
            r = self.mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
            b = add_vectors(a, scale_vector([0, 0, r[2]], scale))
            lines.append({
                'start': a,
                'end': b,
                'color': color,
                'arrow': "start"
            })
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
