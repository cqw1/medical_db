# Copyright 2014. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from boto.dynamodb2.items import Item
from datetime             import datetime

class Device:
    def __init__(self, item):
        self.item = item
        self.equipment = item["Equipment"]
        self.model = item["model"]
        self.manufacturer = item["Manufacturer"]
        self.operationManualName = item["operationManualName"]
        self.operationManualLink = item["operationmanualLink"]
        self.serviceManualName = item["serviceManualName"]
        self.serviceManualName = item["serviceManualLink"]
        self.manualName = item["ManualName"]

    def getEquipment(self):
        return self.equipment

    def getModel(self):
        return self.model

    def getManufacturer(self):
        return self.manufacturer

    def getOperationManualName(self):
        return self.operationManualName

    def getOperationManualLink(self):
        return self.operationManualLink

    def getServiceManualName(self):
        return self.serviceManualName

    def getServiceManualLink(self):
        return self.serviceManualLink

    def __str__(self):
        return self.manualName
