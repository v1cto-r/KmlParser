import xml.etree.ElementTree as ET
import json

def parse_kml(file_path) -> dict:
    placemark_coordinates = {}

    tree = ET.parse(file_path)
    root = tree.getroot()

    file_placemarks = root.findall('.//{http://www.opengis.net/kml/2.2}Placemark')

    for placemark in file_placemarks:
        placemark_name = placemark.find('.//{http://www.opengis.net/kml/2.2}name')
        if placemark_name is not None:
            placemark_name = placemark_name.text.strip()

        multi_geometry = placemark.find('.//{http://www.opengis.net/kml/2.2}MultiGeometry')

        if multi_geometry is not None:
            geometries = multi_geometry.findall('.//{http://www.opengis.net/kml/2.2}Polygon')
            for i, geometry in enumerate(geometries):
                coordinates = extract_coordinates(geometry)
                if placemark_name:
                    if i == 0:
                        placemark_coordinates[placemark_name] = coordinates
                    else:
                        placemark_coordinates[f"{placemark_name}{chr(96 + i)}"] = coordinates

    return placemark_coordinates


def extract_coordinates(polygon_element) -> list:
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    coordinates = []
    coords_kml_element = polygon_element.find('.//kml:coordinates', ns)
    if coords_kml_element is not None:
        coordinates_text = coords_kml_element.text.strip()
        coordinates_lines = coordinates_text.split()
        for coordinate_line in coordinates_lines:
            coords = coordinate_line.split(',')
            longitude = float(coords[0])
            latitude = float(coords[1])
            coordinates.append((latitude, longitude))

    return coordinates


def main():
    name = 'FILE_NAME_WITHOUT_EXTENSION'
    file_path = f'{name}.kml'

    coordinates = parse_kml(file_path)

    json_file_path = f"{name}.json"
    with open(json_file_path, 'w') as json_file:
        json.dump(coordinates, json_file)

if __name__ == "__main__":
    main()