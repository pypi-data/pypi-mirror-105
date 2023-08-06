# -*- coding: utf-8 -*-
"""
@author: WYJQ

Description: This program used to create wps request xml according to user's input data
"""

import os
from lxml import etree
from lxml.builder import ElementMaker


def create(data_path, new_xml_path):
    # get wps xml model file path,$(xml_file) will be replace
    origin_xml_name = "$(origin_xml_name)"
    xml_model_path = os.path.join(os.path.dirname(__file__), origin_xml_name)

    # parse and modify xml
    tree = etree.parse(xml_model_path)
    root = tree.getroot()

    # add some special namespace
    mynsmap = root.nsmap.copy()
    mynsmap["pac"] = "http://www.opengis.net/examples/packet"
    mynsmap["gml"] = "http://www.opengis.net/gml"

    # define tag name(whether there is a prefix)
    n_datainputs = "wps:DataInputs"
    n_input = "wps:Input"
    n_identifer = "ows:Identifier"
    n_reference = "wps:Reference"
    n_data = "wps:Data"
    n_href = "href"
    n_literaldata = "wps:LiteralData"
    n_boundingboxdata = "wps:BoundingBoxData"
    n_lowercorner = "ows:LowerCorner"
    n_uppercorner = "ows:UpperCorner"
    n_complexdata = "wps:ComplexData"
    n_gmlpacket = "pac:GMLPacket"
    n_packetmember = "pac:packetMember"
    n_staticfeature = "pac:StaticFeature"
    n_polygonproperty = "gml:polygonProperty"
    n_polygon = "gml:Polygon"
    n_outerboundaryis = "gml:outerBoundaryIs"
    n_linearring = "gml:LinearRing"
    n_coord = "gml:coord"
    n_X = "gml:X"
    n_Y = "gml:Y"

    # used to determine whether the prefix is suitable
    if "wps" not in root.nsmap:
        n_datainputs = n_datainputs[4:]
        n_input = n_input[4:]
        n_data = n_data[4:]
        n_reference = n_reference[4:]
        n_literaldata = n_literaldata[4:]
        n_boundingboxdata = n_boundingboxdata[4:]
        n_complexdata = n_complexdata[4:]
    if "ows" not in root.nsmap:
        n_identifer = "ns:"+n_identifer[4:]
    if "xlink" in root.nsmap:
        n_herf = "{"+root.nsmap["xlink"]+"}"+n_href
    else:
        n_herf = "{"+root.nsmap["xlin"]+"}"+n_href

    # open input data files
    with open(data_path, encoding="utf-8") as fp_data:
        # set user's data
        datainputs = root.find(n_datainputs, root.nsmap)
        for datainput in datainputs.findall(n_input, root.nsmap):
            data = datainput.find(n_data, root.nsmap)
            if not(data is None):
                # if this is a Data tag

                # if the input data type is boundingbox
                boundingboxdata = data.find(n_boundingboxdata, mynsmap)
                if not (boundingboxdata is None):
                    print("---this is a Data tag : boundingboxdata")
                    lowercorner = boundingboxdata.find(n_lowercorner, mynsmap)
                    data_content = fp_data.readline().strip()
                    lowercorner.text = data_content
                    uppercorner = boundingboxdata.find(n_uppercorner, mynsmap)
                    data_content = fp_data.readline().strip()
                    uppercorner.text = data_content

                # if the input data type is complexdata gml:coord
                elif (not(data.find(n_complexdata, mynsmap) is None)):
                    print("---this is a Data tag : complexdata")
                    complexdata = data.find(n_complexdata, mynsmap)
                    gmlpacket = complexdata.find(n_gmlpacket, mynsmap)
                    packetmember = gmlpacket.find(n_packetmember, mynsmap)
                    staticfeature = packetmember.find(n_staticfeature, mynsmap)
                    polygonproperty = staticfeature.find(
                        n_polygonproperty, mynsmap)
                    polygon = polygonproperty.find(n_polygon, mynsmap)
                    outerboundaryis = polygon.find(n_outerboundaryis, mynsmap)
                    linearring = outerboundaryis.find(n_linearring, mynsmap)
                    coords = linearring.findall(n_coord, mynsmap)
                    for coord in coords:
                        linearring.remove(coord)
                    data_content = fp_data.readline().strip()
                    while data_content != "" and data_content != "*":
                        E = ElementMaker(namespace=mynsmap["gml"], nsmap={
                                         'gml': mynsmap["gml"]})
                        coord = E.coord()
                        X = E.X()
                        X.text = data_content
                        data_content = fp_data.readline().strip()
                        Y = E.Y()
                        Y.text = data_content
                        data_content = fp_data.readline().strip()
                        coord.append(X)
                        coord.append(Y)
                        linearring.append(coord)

                # if the input data type is literal data
                else:
                    print("---this is a Data tag : literaldata")
                    data_content = fp_data.readline().strip()
                    literaldata = data.find(n_literaldata, mynsmap)
                    literaldata.text = data_content
                identifer = datainput.find(n_identifer, mynsmap)
                print(identifer.text+" input ok")
            else:
                # if this is a Reference tag
                reference = datainput.find(n_reference, mynsmap)
                print("---this is a Reference tag")
                data_content = fp_data.readline().strip()
                reference.set(n_herf, data_content)
                identifer = datainput.find(n_identifer, mynsmap)
                print(identifer.text+" input ok")

    tree.write(new_xml_path)
    print("---create new xml finish")
