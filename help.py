"""Help methods for Path Tracining

- sampling_up_hemisphere
- snell_law
"""

import numpy as np 


def sampling_up_hemisphere(V, N):
    """Return a vector from the hemisphere with N as the Z coordinates"""

    # random selecting a vector from a hemisphere(canonical basis)
    e1, e2 = np.random.rand(), np.random.rand()
    a, b = np.arccos(np.sqrt(e1)), 2*np.pi*e2

    canonical_vector = np.array((
        np.sin(a)*np.cos(b),
        np.sin(a)*np.sin(b),
        np.cos(a)
        )
    )
    
    # creating a new basis with V and N vectors
    N = N/np.linalg.norm(N)
    S = np.cross(N, V)
    S = S/np.linalg.norm(S)
    V = np.cross(S, N)
    V = V/np.linalg.norm(V)

    # orthogonal matrix
    matrix = np.array([S, V, N]) 

    return matrix.transpose()@canonical_vector

    
def snell_law(V, N, n_obj = 1.5, n_air = 1.0):
    """return refracted vector given the view vector V(V "points" toward the surface) and the surface normal(N)"""
    if np.dot(N, V) > 0:
        N = -N
        nr = n_obj/n_air
    else: 
        nr = n_air/n_obj

    I = -V
    
    sqrt = 1 - nr**2*(1-np.dot(N, I)**2)
    
    if sqrt < 0:
        return np.zeros(3)

    T = (nr*np.dot(N, I) - np.sqrt(sqrt))*N - nr*I

    return T