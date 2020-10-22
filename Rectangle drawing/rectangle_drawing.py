'''
Script for drawing a rectangles on a Qgis map and changing its color regarding some defined value.

Author: Leo Tisljaric
Email: tisljaricleo@gmail.com
Repo: https://github.com/tisljaricleo/PyQgisScripts
License: MIT

This script show a example of drawing a nxm rectangles on a Qgis map.
The color of a rectangle is defined by the average speed value of the vehicles that was driving in that rectangle.
All speed values are made up (not measured)!

'''

def drawRectangles(points, c_value, name):
    """
    Draws a rectangle as a layer on a Qgis map.
    :param points: Four points of a rectangle [lower left, lower right, upper right, upper left].
    :param c_value: Value for defining a color of a given rectangle.
    :return:
    """
    # Create layer.
    layer = QgsVectorLayer('Polygon', name, "memory")
    pr = layer.dataProvider()
    poly = QgsFeature()
    poly.setGeometry(QgsGeometry.fromPolygonXY([points]))
    pr.addFeatures([poly])
    # Add "Speed" attribute to layer attribute table.
    pr.addAttributes([QgsField("c_value", QVariant.Double)])
    attr_value = {0: c_value}
    pr.changeAttributeValues({1: attr_value})
    layer.updateFields()
    layer.updateExtents()
    QgsProject.instance().addMapLayers([layer])

    # Define ranges for rectangles color.
    # ('name',lower_bound, upper_bound, rgb_color)
    values = (
        ('Low speed', 0, 30, (255, 0, 0, 100)),
        ('Medium speed', 31, 60, (255, 255, 0, 100)),
        ('High speed', 61, 200, (0, 255, 0, 100))
    )

    # Create a category for each item in values.
    ranges = []
    for label, lower, upper, color in values:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(color[0], color[1], color[2], alpha=color[3]))
        symbol.symbolLayer(0).setStrokeColor(QColor(0, 0, 0, alpha=0))  # Border color
        ranges.append(QgsRendererRange(lower, upper, symbol, label))

    renderer = QgsGraduatedSymbolRenderer('c_value', ranges)
    layer.setRenderer(renderer)


def create_coordinate_matrix(sp, xn, yn, lons, lats):
    """
    Creates xn times yn matrix of GNSS points.
    :param sp: Starting GNSS point.
    :param xn: Number of rectangles (columns).
    :param yn: Number of rectangles (rows).
    :param lons: Longitude step.
    :param lats: Latitude step.
    :return: Matrix of GNSS points for rectangle drawing. Every cell consists of a tuple with four points (lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4)
    """
    coordinate_matrix = []
    column_values = []
    for i in range(1, yn + 1):
        for j in range(1, xn + 1):
            lon1 = sp[0] + ((j - 1) * lons)
            lat1 = sp[1] - ((i - 1) * lats)
            lon2 = sp[0] + (j * lons)
            lat2 = sp[1] - (i * lats)
            lon3 = lon1 + lons
            lat3 = lat1
            lon4 = lon2 - lons
            lat4 = lat2
            column_values.append((lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4))
        coordinate_matrix.append(column_values)
        column_values = []
    return coordinate_matrix


def draw_coordinate_matrix(coordinate_matrix, c_values):
    """
    Draws all rectangles defined by the coordinate matrix.
    :param coordinate_matrix: Matrix of GNSS points.
    :param c_values: Matrix of color values for every rectangle.
    :return:
    """
    for i in range(0, len(coordinate_matrix)):
        for j in range(0, len(coordinate_matrix[0])):
            point = coordinate_matrix[i][j]
            p1 = QgsPointXY(point[0], point[1])
            p3 = QgsPointXY(point[2], point[3])
            p2 = QgsPointXY(point[4], point[5])
            p4 = QgsPointXY(point[6], point[7])
            name = str(i) + '-' + str(j)
            drawRectangles([p1, p2, p3, p4], c_values[i][j], name)


#################################################################
# Define starting GNSS point and size of a rectangles to draw.
#################################################################
lon_step = 0.006545  # ~500[m]
lat_step = 0.004579  # ~500[m]

x_num = 5   # Number of rectangles (columns).
y_num = 5   # Number of rectangles (rows).

lon_start = 15.779056
lat_start = 45.834558
start_point = (lon_start, lat_start)    # Starting GNSS point.

#################################################################
# Create a coordinate matrix.
#################################################################
cm = create_coordinate_matrix(sp=start_point,
                              xn=x_num,
                              yn=y_num,
                              lons=lon_step,
                              lats=lat_step)

# Example of the speed matrix.
# Every cell represent the speed for corresponding rectangle.
# The color of a rectangle corresponds to its speed value.
# Small speed - red; Medium speed - yellow; High speed - green
sm = [[0, 20, 50, 0, 3],
      [30, 50, 60, 80, 2],
      [80, 50, 30, 20, 1],
      [0, 0, 0, 0, 5],
      [80, 50, 30, 20, 1]]

#################################################################
# Draw rectangles on the map.
#################################################################
draw_coordinate_matrix(coordinate_matrix=cm,
                       c_values=sm)



