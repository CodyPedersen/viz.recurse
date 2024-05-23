"""FIXME: Add docstring"""

from vizrecurse import draw, visualize


@visualize
def toh(n, source, destination, auxiliary):
    """TODO: Add docstring"""
    if n==1:
        print ("Move disk 1 from source", source, "to destination", destination)
        return
    toh(n-1, source, auxiliary, destination)
    print ("Move disk", n,"from source", source, "to destination", destination)
    toh(n-1, auxiliary, destination, source)

# Driver code
N = 5
toh(N,'A','B','C')

draw()
