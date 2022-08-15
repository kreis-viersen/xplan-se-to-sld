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

#  Verzeichns mit SE-Dateien (Endung .xml)
se_directory = 'D:/se/'

for xml_file in pathlib.Path(se_directory).glob('*.xml'):
    print(xml_file.name)
    filename = xml_file.name

    name_without_ext = filename.split(".")[0]
    # Name und Pfad der erzeugten SLD-Datei
    new_file_path = se_directory + name_without_ext + '.sld'

    # SE-Datei parsen
    tree = etree.parse(se_directory + filename)
    root_1 = tree.getroot()

    # Ergänze SLD-"Hülle"
    xml_2 = '''<!--
    Based on SE-Styles from https://gitlab.opencode.de/diplanung/ozgxplanung/
    Modified with https://github.com/kreis-viersen/xplan-se-to-sld

    Copyright (C) 2008 - 2022 lat/lon GmbH, info@lat-lon.de, www.lat-lon.de

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    -->
    <sld:StyledLayerDescriptor version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld
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

    # Entferne substrings xplan: und Code, so wird z.B. aus xplan:allgArtDerBaulNutzungCode -> allgArtDerBaulNutzung.
    # Dann passt das zu den Feldnamen nach dem XPlanGML Import in QGIS (attributbasiertes Styling).
    for property_name in root_2.iter('{http://www.opengis.net/ogc}PropertyName'):
        property_name.text = property_name.text.replace('xplan:', '').replace('Code', '')

    # Verwende uom-Attribut gemäß SE-Spezifikation, ref: https://gitlab.opencode.de/diplanung/ozgxplanung/-/issues/1#note_2177
    symbolizers = ['TextSymbolizer', 'PointSymbolizer', 'LineSymbolizer', 'PolygonSymbolizer']

    for symbolizer in symbolizers:
        for symbolizer in root_2.iter('{http://www.opengis.net/se}' + symbolizer):
            if 'uom' in symbolizer.attrib and symbolizer.attrib['uom'] == 'meter':
                symbolizer.attrib['uom'] = 'http://www.opengeospatial.org/se/units/metre'

    #Formatiere und schreibe SLD in das Verzeichnis mit den SE-Dateien
    etree.indent(tree_2, space="\t", level=0)
    tree_2.write(new_file_path, encoding = "UTF-8", xml_declaration = True)