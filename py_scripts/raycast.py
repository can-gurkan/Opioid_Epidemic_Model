import csv
import pandas as pd

class Point:
    def __init__(self, x, y):
        """
        A point specified by (x,y) coordinates in the cartesian plane
        """
        self.x = x
        self.y = y


class Polygon:
    def __init__(self, points):
        """
        points: a list of Points in clockwise order.
        """
        self.points = points

    @property
    def edges(self):
        ''' Returns a list of tuples that each contain 2 points of an edge '''
        edge_list = []
        for i, p in enumerate(self.points):
            p1 = p
            p2 = self.points[(i + 1) % len(self.points)]
            edge_list.append((p1, p2))

        return edge_list

    def contains(self, point):
        import sys
        # _huge is used to act as infinity if we divide by 0
        _huge = sys.float_info.max
        # _eps is used to make sure points are not on the same line as vertexes
        _eps = 0.00001

        # We start on the outside of the polygon
        inside = False
        for edge in self.edges:
            # Make sure A is the lower point of the edge
            A, B = edge[0], edge[1]
            if A.y > B.y:
                A, B = B, A

            # Make sure point is not at same height as vertex
            if point.y == A.y or point.y == B.y:
                point.y += _eps

            if (point.y > B.y or point.y < A.y or point.x > max(A.x, B.x)):
                # The horizontal ray does not intersect with the edge
                continue

            if point.x < min(A.x,
                             B.x):  # The ray intersects with the edge inside = not inside continue try: m_edge = (B.y - A.y) / (B.x - A.x) except ZeroDivisionError: m_edge = _huge try: m_point = (point.y - A.y) / (point.x - A.x) except ZeroDivisionError: m_point = _huge if m_point >= m_edge:
                # The ray intersects with the edge
                inside = not inside
                continue

        return inside


def read_file(region_name):
    polylist = []
    df = pd.read_csv('polygons/'+region_name+'Poly.txt',delimiter='\t',index_col=None)
    for index,row in df.iterrows():
        polylist.append([row.iloc[2], row.iloc[1]])
    q = Polygon([Point(i[0],i[1]) for i in polylist])
    return q


def is_inside(x, y, region):
    poly = read_file(region)
    p0 = Point(y,x)
    return poly.contains(p0)


if __name__ == "__main__":

    is_inside(27.900778149999997,-82.7314389,"Pinellas")

    q = Polygon([Point(20, 10),
                 Point(50, 125),
                 Point(125, 90),
                 Point(150, 10)])

    # Test 1: Point inside of polygon
    p1 = Point(75, 50)
    print("P1 inside polygon: " + str(q.contains(p1)))
