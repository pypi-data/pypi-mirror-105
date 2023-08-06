# -*- coding: utf-8 -*-
"""
@author: WYJQ

Description: A standard wps2openGMS encapsulation file 
"""

import os
import sys
import requests

from modelservicecontext import EModelContextStatus
from modelservicecontext import ERequestResponseDataFlag
from modelservicecontext import ERequestResponseDataMIME
from modelservicecontext import ModelServiceContext
from modeldatahandler import ModelDataHandler

import createwpsxml

# encapsulation program
# Begin encapsulation
if len(sys.argv) < 3:
    exit()

ms = ModelServiceContext()
ms.onInitialize(sys.argv[1], sys.argv[2], sys.argv[3])
mdh = ModelDataHandler(ms)

print(ms.getMappingLibraryDirectory())

# Enter State
ms.onEnterState('run')

# Event
ms.onFireEvent('inputdata')
ms.onRequestData()
if ms.getRequestDataFlag() == ERequestResponseDataFlag.ERDF_OK:
    if ms.getRequestDataMIME() == ERequestResponseDataMIME.ERDM_RAW_FILE:
        data_path = ms.getRequestDataBody()
else:
    ms.onFinalize()

# Event
ms.onFireEvent('outputResult')

instance_dir = os.path.normpath(ms.getModelInstanceDirectory())
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

# create wps post request xml
new_xml_path = instance_dir+"/xml_new.xml"
createwpsxml.create(data_path, new_xml_path)

# send post http request to 52n wps
# ***the url need change to different wps interface***
url = "$(wps_url)"
with open(new_xml_path, encoding="utf-8") as fp:
    body = fp.read()
headers = {'Content-Type': 'application/xml'}
r = requests.post(url, data=body.encode("utf-8"), headers=headers)

# save the result file
result_path = instance_dir + "/result_data"
with open(result_path, "wb") as code:
    code.write(r.content)

# finish
ms.setResponseDataFlag(ERequestResponseDataFlag.ERDF_OK)
ms.setResponseDataMIME(ERequestResponseDataMIME.ERDM_RAW_FILE)
ms.setResponseDataBody(result_path)

# exit
ms.onResponseData()
ms.onLeaveState()
ms.onFinalize()
