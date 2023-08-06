# -*- coding: utf-8 -*-
"""
@author: WYJQ

Description: Create OpenGMS service package from wps request xml
"""

import os
import sys
import uuid
import shutil
import zipfile
import tempfile
from lxml import etree

# compress files


def zipDir(dirpath, outFullName):
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        fpath = path.replace(dirpath, '')
        if fpath != "":
            zip.write(path, fpath)
        for filename in filenames:
            zip.write(os.path.join(path, filename),
                      os.path.join(fpath, filename))
    zip.close()


def createWPS2OpenGMS(wps_url, xml_file):
    #get xml basename, abspath, result zip abspath
    xml_name=os.path.basename(xml_file)[0:-4]
    xml_abspath=os.path.abspath(xml_file)
    result_zip_abspath=xml_abspath[0:-4]+".zip"
    #create result temp folder
    dirname = tempfile.TemporaryDirectory().name
    #get self resource files path
    resourceDir = os.path.join(os.path.dirname(__file__), "resource")
    # generate file tree
    os.mkdir(dirname)
    os.mkdir(dirname + "\\model")
    os.mkdir(dirname + "/assembly")
    os.mkdir(dirname + "/testify")
    os.mkdir(dirname + "/supportive")

    # generate deployment file package
    # modify the createwpsxml.py
    fct = open(resourceDir+"/createwpsxml_template.py", "r")
    content = fct.read()
    fct.close()

    content = content.replace("$(origin_xml_name)", xml_name)

    fc = open(dirname + "/model/createwpsxml.py", "w")
    fc.write(content)
    fc.close()
    print("---1/3-generate createwpsxml.py ok.")

    # modify the encapsulation.py
    fet = open(resourceDir+"/encapsulation_template.py", "r")
    content = fet.read()
    fet.close()

    content = content.replace("$(wps_url)", wps_url)

    fe = open(dirname + "/model/encapsulation.py", "w")
    fe.write(content)
    fe.close()
    print("---2/3-generate encapsulation.py ok.")

    # modify the mdl file
    # open origin xml
    tree_xml = etree.parse(xml_abspath)
    root_xml = tree_xml.getroot()

    # open mdl template file
    mdl_file = resourceDir+"/mdl_template.mdl"
    tree_mdl = etree.parse(mdl_file)

    # define tag name(whether there is a prefix)
    n_datainputs = "wps:DataInputs"
    n_input = "wps:Input"
    n_identifer = "ows:Identifier"
    n_reference = "wps:Reference"
    n_data = "wps:Data"
    n_literaldata = "wps:LiteralData"
    n_responseform = "wps:ResponseForm"
    n_rawdataoutput = "wps:RawDataOutput"
    n_responsedocument = "wps:ResponseDocument"
    n_output = "wps:Output"

    # used to determine whether the prefix is suitable
    if "wps" not in root_xml.nsmap:
        n_datainputs = n_datainputs[4:]
        n_input = n_input[4:]
        n_data = n_data[4:]
        n_reference = n_reference[4:]
        n_literaldata = n_literaldata[4:]
        n_responseform = n_responseform[4:]
        n_rawdataoutput = n_rawdataoutput[4:]
        n_responsedocument = n_responsedocument[4:]
        n_output = n_output[4:]

    if "ows" not in root_xml.nsmap:
        n_identifer = "ns:"+n_identifer[4:]

    params_dir = "---Parameter Description:"

    # add information in new mdl file
    # add model class description
    total_identifer = root_xml.find(n_identifer, root_xml.nsmap)
    modelclass = tree_mdl.xpath("//ModelClass")
    model_name = total_identifer.text.split(".")[-1]
    modelclass[0].set("name", model_name)
    uid = str(uuid.uuid4())
    modelclass[0].set("uid", uid)

    # set the state uid
    state = tree_mdl.xpath("//Behavior/StateGroup/States/State")
    uid = str(uuid.uuid4())
    state[0].set("id", uid)

    # add LocalAttribute
    lattrs = tree_mdl.xpath(
        "//ModelClass/AttributeSet/LocalAttributes/LocalAttribute")
    for lattr in lattrs:
        lattr.set("localName", model_name)
        keywords = lattr.find("Keywords")
        keywords.text = model_name
        abstract = lattr.find("Abstract")
        abstract.text = model_name

    # add input description
    datainputs = root_xml.find(n_datainputs, root_xml.nsmap)
    intput_c = 1
    for datainput in datainputs.findall(n_input, root_xml.nsmap):
        data_dir = "Input"+str(intput_c)+": inputname:"
        data = datainput.find(n_data, root_xml.nsmap)
        if not(data is None):
            identifer = datainput.find(n_identifer, root_xml.nsmap)
            data_dir = data_dir+identifer.text

            if (not(data.find(n_literaldata, root_xml.nsmap) is None)):
                literaldata = data.find(n_literaldata, root_xml.nsmap)
                if literaldata.get("dataType") is None:
                    data_dir = data_dir+" datatype:LiteralData; "
                else:
                    data_dir = data_dir+" datatype:" + \
                        literaldata.get("dataType")+"; "
            else:
                data_dir = data_dir+" datatype:ComplexData; "
        else:
            identifer = datainput.find(n_identifer, root_xml.nsmap)
            data_dir = data_dir+identifer.text
            reference = datainput.find(n_reference, root_xml.nsmap)
            if reference.get("mimeType") is None:
                data_dir = data_dir+" datatype:href; "
            else:
                data_dir = data_dir+" datatype:" + \
                    reference.get("mimeType")+"; "
        intput_c += 1
        params_dir += data_dir

    Event_input = tree_mdl.xpath(
        "//Behavior/StateGroup/States/State/Event[@name='inputdata']")
    Event_input[0].set("description", "input data in one txt"+params_dir)

    # add output description
    output_dir = "--Output Description:"
    if(not(root_xml.find(n_responseform, root_xml.nsmap) is None)):
        responseform = root_xml.find(n_responseform, root_xml.nsmap)

        if (not(responseform.find(n_responsedocument, root_xml.nsmap) is None)):

            responsedocument = responseform.find(
                n_responsedocument, root_xml.nsmap)
            output = responsedocument.find(n_output, root_xml.nsmap)
            identifer = output.find(n_identifer, root_xml.nsmap)
            output_dir = output_dir+identifer.text
            if output.get("mimeType") is None:
                output_dir = output_dir+" datatype:No description; "
            else:
                output_dir = output_dir+" datatype:" + \
                    output.get("mimeType")+"; "
        else:
            rawdataoutput = responseform.find(
                n_rawdataoutput, root_xml.nsmap)
            identifer = rawdataoutput.find(n_identifer, root_xml.nsmap)
            output_dir = output_dir+identifer.text
            if rawdataoutput.get("mimeType") is None:
                output_dir = output_dir+" datatype:No description; "
            else:
                output_dir = output_dir+" datatype:" + \
                    rawdataoutput.get("mimeType")+"; "
        Event_input = tree_mdl.xpath(
            "//Behavior/StateGroup/States/State/Event[@name='outputResult']")
        Event_input[0].set("description", output_dir)

    # write new mdl file
    tree_mdl.write(dirname + "/model/new_dml.mdl", encoding='utf-8')
    print("---3/3-generate new_mdl.mdl ok.")

    # copy the necessary file
    shutil.copyfile(xml_abspath, dirname + '/model/' +xml_name)
    shutil.copyfile(resourceDir+"/modeldatahandler.py",
                    dirname + "/model/modeldatahandler.py")
    shutil.copyfile(resourceDir+"/modelservicecontext.py",
                    dirname + "/model/modelservicecontext.py")

    #! wrap and compress package
    zipDir(dirname, result_zip_abspath)
    print("result zip file at:"+result_zip_abspath)
    print("Successfully created the OpenGMS deployment package.")

    #! clear temp files
    shutil.rmtree(dirname, ignore_errors=True)