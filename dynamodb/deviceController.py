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
from boto.dynamodb2.exceptions import ConditionalCheckFailedException
from boto.dynamodb2.exceptions import ItemNotFound
from boto.dynamodb2.exceptions import JSONResponseError
from boto.dynamodb2.exceptions import ValidationException
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from datetime               import datetime

class DeviceController:
    """
    This GameController class basically acts as a singleton providing the necessary 
    DynamoDB API calls.
    """
    def __init__(self, connectionManager):
        self.cm = connectionManager
        self.ResourceNotFound = 'com.amazonaws.dynamodb.v20120810#ResourceNotFoundException'

        self.count = 0

    def createNewDevice(self, manualName, manufacturer, equipment):
        print "in createNewDevice"
        # if self.count == 0:
        #     print "in createNewDevice"

        #     item = Item(self.cm.getDevicesTable(), data={
        #             "ManualName": manualName})

        #     item.save()
        #     self.count += 1

    def checkIfTableIsActive(self):
        description = self.cm.db.describe_table("Devices")
        status = description['Table']['TableStatus']
    
        return status == "ACTIVE"

    def getDevicesWithQuery(self, query):

        """
        Query for all games that a user appears in and have a certain status.
        Sorts/merges the results of the two queries for top 10 most recent games.
        Return a list of Game objects.
        """
    
        print query

        # results = self.cm.getDevicesTable().query_2(               ManualName__beginswith=query)

        results = self.cm.getDevicesTable().scan(
            ManualName__beginswith=query)
   
        resultList = []

        try:
            r = results.next()
            resultList.append(r)
        except StopIteration, si:
            print "No results"

        return resultList
