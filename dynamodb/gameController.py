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

class DevicesController:
    """
    This GameController class basically acts as a singleton providing the necessary 
    DynamoDB API calls.
    """
    def __init__(self, connectionManager):
        self.cm = connectionManager
        self.ResourceNotFound = 'com.amazonaws.dynamodb.v20120810#ResourceNotFoundException'
   
   """ 
    def createNewGame(self, gameId, creator, invitee):
        """
        """
        Using the High-Level API, an Item is created and saved to the table.
        All the primary keys for either the schema or an index (GameId,
        HostId, StatusDate, and OpponentId) as well as extra attributes needed to maintain
        game state are given a value.
        Returns True/False depending on the success of the save.
        """
        """ 
        now = str(datetime.now())
        statusDate = "PENDING_" + now
        item = Item(self.cm.getGamesTable(), data= {
                            "GameId"     : gameId,
                            "HostId"     : creator,
                            "StatusDate" : statusDate,
                            "OUser"      : creator,
                            "Turn"       : invitee,
                            "OpponentId" : invitee
                        })
        
        return item.save()
    """
    
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
    
        results = self.cm.getDevicesTable().query_2(               Equipment__beginswith=query)
   
        resultList = []

        for result in results:
            resultList.append(result)

        return resultList
