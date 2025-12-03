This script generates fully parametric 3D re-entrant auxetic structures using CadQuery for solid modeling and PyVista for visualization. The geometry is constructed from a set of defined vertex coordinates and edge connections, where each edge is modeled as a cylindrical ligament and each node as a spherical joint.
The script supports generating two types of lattices:

a cubic auxetic lattice
a pyramidal auxetic lattice with progressively decreasing cell count per layer

Key features include:

Adjustable geometric parameters (cell size, thickness, re-entrant angle, repetition count).
Automatic construction of cylinders and spheres based on vertex/edge definitions.
Creation of large-scale repeated auxetic lattices in 3D.
Export of the final compound structure to STEP and STL formats.
Built-in visualization of the exported STL using PyVista.

The resulting geometry is suitable for finite element analysis, CAD workflows, and auxetic structure research.
