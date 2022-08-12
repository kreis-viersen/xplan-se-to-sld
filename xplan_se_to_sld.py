"""
***************************************************************************
XPlan-SE-to-SLD
Python script

        Date                 : May 2022
        Copyright            : (C) 2022 by Kreis Viersen
        Email                : open@kreis-viersen.de

***************************************************************************

***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from lxml import etree
import pathlib

se_directory = 'D:/se/'

for xml_file in pathlib.Path(se_directory).glob('*.xml'):
    print(xml_file.name)
    filename = xml_file.name

    name_without_ext = filename.split(".")[0]
    name_without_ext = name_without_ext[0].upper() + name_without_ext[1].upper() + name_without_ext[2:]
    new_file_path = se_directory + name_without_ext + '.sld'

    tree = etree.parse(se_directory + filename)
    root_1 = tree.getroot()

    xml_2 = '''<sld:StyledLayerDescriptor version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld
    StyledLayerDescriptor.xsd" xmlns:sld="http://www.opengis.net/sld"
    xmlns:se="http://www.opengis.net/se"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <sld:NamedLayer>
            <se:Name>''' + name_without_ext + '''</se:Name>
                <sld:UserStyle>
                    <sld:IsDefault>1</sld:IsDefault>
                </sld:UserStyle>
        </sld:NamedLayer>
    </sld:StyledLayerDescriptor>'''

    tree_2 = etree.ElementTree(etree.fromstring(xml_2))
    root_2 = tree_2.getroot()

    named_layer = root_2.find('{http://www.opengis.net/sld}NamedLayer')
    user_style = named_layer.find('{http://www.opengis.net/sld}UserStyle')
    user_style.append(root_1)

    for property_name in root_2.iter('{http://www.opengis.net/ogc}PropertyName'):
        property_name.text = property_name.text.replace('xplan:', '').replace('Code', '')

    symbolizers = ['TextSymbolizer', 'PointSymbolizer', 'LineSymbolizer', 'PolygonSymbolizer']

    for symbolizer in symbolizers:
        for symbolizer in root_2.iter('{http://www.opengis.net/se}' + symbolizer):
            if 'uom' in symbolizer.attrib and symbolizer.attrib['uom'] == 'meter':
                symbolizer.attrib['uom'] = 'http://www.opengeospatial.org/se/units/metre'

    etree.indent(tree_2, space="\t", level=0)
    tree_2.write(new_file_path, encoding = "UTF-8", xml_declaration = True)