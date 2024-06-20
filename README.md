# KML PARSER

Code that transforms a KML file into a JSON file.
It parses through every placemark and creates a key inside the JSON file with the placemark name. Using the geometry it parses the text and turns the coordinates into a 2 dimensional array.

In the case multiple geometries are found, it creates a secondary key with the same name, and a subnumber indicating its relationship.

## CODE EXPLANATION
```python
import xml.etree.ElementTree as ET
import json

def main():
    file_name = 'FILE_NAME_WITHOUT_EXTENSION'
    file_path = f'{file_name}.kml'

    coordinates = parse_kml(file_path)

    json_file_path = f"{file_name}.json"
    with open(json_file_path, 'w') as json_file:
        json.dump(coordinates, json_file)
```
So the main functions is just to declare the filename, run the parsing function, and save the data into a JSON file with the same name.

```python
def parse_kml(file_path) -> dict:
    placemark_coordinates = {}

    tree = ET.parse(file_path)
    root = tree.getroot()

    # Locate all Placemark elements in the KML file
    file_placemarks = root.findall('.//{http://www.opengis.net/kml/2.2}Placemark')

    # Iterate over each Placemark element and extract the name and coordinates
    for placemark in file_placemarks:
        placemark_name = placemark.find('.//{http://www.opengis.net/kml/2.2}name')
        if placemark_name is not None:
            placemark_name = placemark_name.text.strip()

        # Locate the MultiGeometry element within the Placemark element
        multi_geometry = placemark.find('.//{http://www.opengis.net/kml/2.2}MultiGeometry')

        if multi_geometry is not None:
            # Locate all Geometry elements within the MultiGeometry element
            geometries = multi_geometry.findall('.//{http://www.opengis.net/kml/2.2}Polygon')
            
            # Extract the coordinates from each Geometry element
            for i, geometry in enumerate(geometries):
                # Extract the coordinates from the Geometry element
                coordinates = extract_coordinates(geometry)
                if placemark_name:
                    if i == 0:
                        # Store the coordinates in the dictionary with the placemark name as the key
                        placemark_coordinates[placemark_name] = coordinates
                    else:
                        # Append the alphabet to the placemark name to differentiate between the different geometries
                        placemark_coordinates[f"{placemark_name}{chr(96 + i)}"] = coordinates

    return placemark_coordinates
```
The function first locates all the placemarks inside a KML file, then for each placemark it will locate the multigeometries. For each geometries, the coordinates are extracted and formated with the `extract_coordinates()` function. Finally there are appended into a dictionary, if there are multiple geometries inside a same placemark, a letter is appended to the name to diferentiate them.

```python
def extract_coordinates(polygon_element) -> list:
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    coordinates = []
    
    # Locate the coordinates element within the Polygon element
    coords_kml_element = polygon_element.find('.//kml:coordinates', ns)
    
    if coords_kml_element is not None:
        
        # Extract the text from the coordinates element and split the text into lines
        coordinates_text = coords_kml_element.text.strip()
        coordinates_lines = coordinates_text.split()
        
        # Iterate over each line and extract the latitude and longitude
        for coordinate_line in coordinates_lines:
            coords = coordinate_line.split(',')
            longitude = float(coords[0])
            latitude = float(coords[1])
            
            # Append the latitude and longitude to the coordinates list
            coordinates.append((latitude, longitude))

    return coordinates
```
The function locates the coordinates, and then converts them into plain text and splits it into lines to be iterated. Then the lat, lng is extracted and appended into an array.
