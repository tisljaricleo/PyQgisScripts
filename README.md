# PyQgisScripts :snake:

This repository contains some useful PyQgis scripts.
Most of the scripts are related to drawing various elements on a Qgis map.

## Installation

Install the latest version of [QGIS](https://qgis.org/en/site/).
This script works on Qgis 3.14.16.  

## Usage

1. Open the Qgis application.
2. Open the map (XYZ Tiles -> OpenStreetMap -> Add layer to project).
3. Open the Python console in Qgis.
4. Click 'Show editor'.
4. Copy and paste the code in the Python console.
5. Edit the code if needed.
6. Send feedback. Thank you!

## Scripts

### Rectangle drawing
The script will draw rectangles on a Qgis map. Users need to define a starting GNSS point, the size of rectangles, and the number of rectangles. Also, the matrix for rectangles colors must be provided. The full description and examples can be found in the [Medium article](https://medium.com/student-research-group-sis-dva/pyqgis-script-for-drawing-colored-rectangles-4c4944caffe4).
The result will be something like this:
![Rectangles_example](https://www.dropbox.com/s/bajfy4cjx0y7kvv/QgisRectangles.JPG?dl=0&raw=1)



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/tisljaricleo/PyQgisScripts/blob/main/LICENSE)
