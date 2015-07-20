#!flask/bin/python
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
from dynamodb.connectionManager       import ConnectionManager
from dynamodb.deviceController        import DeviceController
from models.device                    import Device
from uuid                             import uuid4
from flask                            import Flask, render_template, request, session, flash, redirect, jsonify, json
from ConfigParser                     import ConfigParser
import os, time, sys, argparse

application = Flask(__name__)
application.debug = True
application.secret_key = str(uuid4())
        
"""
   Configure the application according to the command line args and config files
"""

cm = None

parser = argparse.ArgumentParser(description='Run the TicTacToe sample app', prog='application.py')
parser.add_argument('--config', help='Path to the config file containing application settings. Cannot be used if the CONFIG_FILE environment variable is set instead')
parser.add_argument('--mode', help='Whether to connect to a DynamoDB service endpoint, or to connect to DynamoDB Local. In local mode, no other configuration ' \
                    'is required. In service mode, AWS credentials and endpoint information must be provided either on the command-line or through the config file.',
                    choices=['local', 'service'], default='service')
parser.add_argument('--endpoint', help='An endpoint to connect to (the host name - without the http/https and without the port). ' \
                    'When using DynamoDB Local, defaults to localhost. If the USE_EC2_INSTANCE_METADATA environment variable is set, reads the instance ' \
                    'region using the EC2 instance metadata service, and contacts DynamoDB in that region.')
parser.add_argument('--port', help='The port of DynamoDB Local endpoint to connect to.  Defaults to 8000', type=int)
parser.add_argument('--serverPort', help='The port for this Flask web server to listen on.  Defaults to 5000 or whatever is in the config file. If the SERVER_PORT ' \
                    'environment variable is set, uses that instead.', type=int)
args = parser.parse_args()

configFile = args.config
config = None
if 'CONFIG_FILE' in os.environ:
    if configFile is not None:
        raise Exception('Cannot specify --config when setting the CONFIG_FILE environment variable')
    configFile = os.environ['CONFIG_FILE']
if configFile is not None:
    config = ConfigParser()
    config.read(configFile)

# Read environment variable for whether to read config from EC2 instance metadata
use_instance_metadata = ""
if 'USE_EC2_INSTANCE_METADATA' in os.environ:
    use_instance_metadata = os.environ['USE_EC2_INSTANCE_METADATA']

cm = ConnectionManager(mode=args.mode, config=config, endpoint=args.endpoint, port=args.port, use_instance_metadata=use_instance_metadata)
controller = DeviceController(cm)

serverPort = args.serverPort
if config is not None:
    if config.has_option('flask', 'secret_key'):
        application.secret_key = config.get('flask', 'secret_key')
    if serverPort is None:
        if config.has_option('flask', 'serverPort'):
            serverPort = config.get('flask', 'serverPort')

# Default to environment variables for server port - easier for elastic beanstalk configuration
if 'SERVER_PORT' in os.environ:
    serverPort = int(os.environ['SERVER_PORT'])

if serverPort is None:
    serverPort = 5000

"""
   Define the urls and actions the app responds to   
"""

"""
@application.route('/table', methods=["GET", "POST"])
def createTable():
    cm.createGamesTable() 

    while controller.checkIfTableIsActive() == False:
        time.sleep(3)

    return redirect('/index')
    """
cm.createDevicesTable()
controller.createNewDevice("CardioCare", "Medikraft", "Infant Incubator")
@application.route('/')
@application.route('/index', methods=["GET", "POST"])
def index():
    """
    Method associated to both routes '/' and '/index' and accepts
    post requests for when a user logs in.  Updates the user of
    the session to the person who logged in.  Also populates 3 tables for game invites, games in progress, and
    games finished by the logged in user (if there is one).
    """

    if request.method == "POST":
        return redirect('/index')

    matchingDevices = controller.getDevicesWithQuery("CardioCare")
    print Device(matchingDevices[0])
    results = [Device(device) for device in matchingDevices]

    return render_template("index.html", results=results)

"""
@application.route('/create')
def create():
"""

"""
    if session.get("username", None) == None:
        flash("Need to login to create game")
        return redirect("/index")
    return render_template("create.html",
                            user=session["username"])
"""

if __name__ == "__main__":
    if cm:
        application.run(debug = True, port=serverPort, host='0.0.0.0')
