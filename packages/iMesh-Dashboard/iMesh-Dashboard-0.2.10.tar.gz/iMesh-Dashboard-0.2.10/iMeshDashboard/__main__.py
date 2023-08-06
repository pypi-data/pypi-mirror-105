#!/usr/bin/env python3

import traceback
from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from flask_basicauth import BasicAuth
from flask_apscheduler import APScheduler
import requests
import json
import copy
import atexit
import time
import timeago
from datetime import datetime
import paho.mqtt.client as mqtt
import meshtastic
from meshtastic import remote_hardware, portnums_pb2, remote_hardware_pb2

from pubsub import pub
import configparser
from pkg_resources import get_distribution, DistributionNotFound
import os.path
from waitress import serve

class iMeshDashboard:
    def __init__(self):
        try:
            dist = get_distribution('iMesh-Dashboard')
        except DistributionNotFound:
            self.version = 'Unknown version'
        else:
            self.version = dist.version
        
        self.dataPath = '/usr/local/iMeshDashboard'
        self.config = configparser.ConfigParser()
        self.config.read(self.dataPath+'/conf/app.conf') 

        self.oldReceivedNodes = dict()
        self.receivedNodes = dict()
        self.myNodeInfo = dict()
        self.mapNodes = []

        self.positionBeacon = False

        self.interface = meshtastic.SerialInterface()
        
        self.client = mqtt.Client()
        self.client.username_pw_set(username=self.config['MQTT']['username'], password=self.config['MQTT']['password'])
        
        self.appData = {"version":self.version}

        self.scheduler = APScheduler()

    def reboot(self):
        print("Rebooting")
        self.interface.localNode.reboot()
        
    def sendPosition(self):
        print("Sending Position Beacon")
        self.interface.sendPosition(float(self.config['Position']['lat']), float(self.config['Position']['lon']), 
                               int(self.config['Position']['alt']), int(time.time()))

    def stripKey(self, inDict, keys):
        keySet = set(keys)
        strippedDict = {}
        for key, value in inDict.items():
            if key not in keySet:
                if isinstance(value, dict):
                    strippedDict[key] = self.stripKey(value, keySet)
                else:
                    strippedDict[key] = value
            else:
                print("stripped key", key)
        return strippedDict

    def getHourDiff(self, TS):
        return int((int(time.time())-int(TS))/3600)
    
    def getFloat(self, fnum):
        if isinstance(fnum, float):
            return "{:.4f}".format(fnum)
        else:
            return ""
    
    def getLH(self, ts, default=""):
        return datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S') if ts else default
    
    def getTimeAgo(self, ts, default=""):
        return timeago.format(datetime.fromtimestamp(ts), datetime.now()) if ts else default
    
    def getNodeInfo(self):
        try:
            self.myNodeInfo = self.stripKey(self.interface.localNode.iface.getMyNodeInfo(), "raw")
            return json.dumps(self.myNodeInfo)
        except Exception as e:
            traceback.print_exc()
            return None
    
    
    def getMapNodeInfo(self, node):
            tDelta = int(time.time()) - int(node.get("lastHeard"))
            color = "indigo"
            if(tDelta <= 172800):
                color = "purple"
            if(tDelta <= 86400):
                color = "red"
            if(tDelta <= 43200):
                color = "coral"
            if(tDelta <= 21600):
                color = "orange"
            if(tDelta <= 10800):
                color = "yellowgreen"
            if(tDelta <= 3600):
                color = "green"
            textContent = ("<div><h4>"+node['user']['longName']+"</h4><table>"
                          "<tr><td>Id:</td><td>"+node['user']['id']+"<td></tr>"
                          "<tr><td>Position:</td><td>"+self.getFloat(node['position']['latitude'])+"°, "+self.getFloat(node['position']['longitude'])+"°,"
                          " "+str(node['position'].get('altitude', '--'))+"m<td></tr>"
                          "<tr><td>Last Heard:</td><td>"+self.getLH(node.get("lastHeard"))+"<td></tr>"
                          "<tr><td></td><td>"+self.getTimeAgo(node.get("lastHeard"))+"<td></tr>"
                          "</table></div>")
            return color, textContent
    
    def onGPIOreceive(self, interface, packet):
        print("remote_hardware")
        #print(packet)
        pb = remote_hardware_pb2.HardwareMessage()
        pb.ParseFromString(packet["decoded"]["data"]["payload"])
        #print(pb)
        print(f"Received RemoteHardware typ={pb.typ}, gpio_value={pb.gpio_value}")
    
    def updateImeshMap(self, interface, packet):
        self.mapNodes = []
        self.receivedNodes = self.stripKey(self.interface.nodes, "raw")
        print("New Data Received", datetime.now())
        self.interface.showNodes()
        '''
        if packet is not None:
            print("Packet received:")
            #print(packet)
            hop = packet.get('hopLimit', None)
            #print(hop)
            if (hop is not None) and (myNodeInfo['user']['id'] != packet.get('fromId')):
                print("Pushing received node info")
                client.publish("meshInfo/hopInfo", json.dumps({"receivedNode":packet.get('fromId'), "receiverNode":myNodeInfo['user']['id'],
                               "hopLimit":packet.get('hopLimit'), "rxTime":packet.get('rxTime')}))
        '''                       
        try:
            for node, nodeValue in self.receivedNodes.items():       
                try:
                    self.mapNodes.append([nodeValue['user']['longName'], nodeValue['position']['latitude'],
                                     nodeValue['position']['longitude'], self.getMapNodeInfo(nodeValue)[0], self.getMapNodeInfo(nodeValue)[1], self.getHourDiff(nodeValue.get("lastHeard"))])
                    if node in self.oldReceivedNodes:
                        print(node +" - "+ nodeValue['user']['longName'] +" nodo presente")
                        if nodeValue.get("lastHeard") > self.oldReceivedNodes[node].get("lastHeard"):
                            print("aggiornato")
                            self.client.publish("receivedNodes/"+node, json.dumps(nodeValue))
                    else:
                        print("New node received: "+node +" - "+ nodeValue['user']['longName']+" @ "+str(nodeValue['position'].get('time')))
                        if(self.config['MQTT']['enabled']=="True"):
                            self.client.publish("receivedNodes/"+node, json.dumps(nodeValue))
                except Exception as e:
                    traceback.print_exc()
                    print(nodeValue)
        except Exception as e:
            traceback.print_exc()
        finally:
            self.oldReceivedNodes = copy.deepcopy(self.receivedNodes) 

    def getNodes(self):
        nodesList = []
        for node, value in self.receivedNodes.items():
            if (value['user']['id'] == self.myNodeInfo['user']['id']):
                continue
            lhTS = value.get('lastHeard')
            #if (lhTS is None) or (lhTS < (int(time.time())-86400)):
            #    print("INVALID LH", value['user']['id'], getLH(lhTS), value['user']['longName'],)
            #    continue
            #else:
            lh = self.getLH(lhTS)
            since = self.getTimeAgo(lhTS)
    
            if 'position' in value:
                if 'latitude' in value['position'] and 'longitude' in value['position']:
                    pos = self.getFloat(value['position'].get('latitude')) +"°, "+self.getFloat(value['position'].get('longitude')) + "°, " + str(value['position'].get('altitude', '---'))+"m"
                else:
                    pos=""
                batt = str(value['position'].get('batteryLevel', ""))
                batt = batt + ("%" if (batt != "") else "")
            else:
                pos = ""
                batt = ""
    
            snr = str(value.get('snr'))
            snr = snr + (" dB" if (snr != "") else "")
            nodesList.append({"user":value['user']['longName'], "id":node, "pos":pos, "lh":lh, "batt":batt, "snr":snr, "since":since, "lhTS":lhTS})
            nodesList = sorted(nodesList, key=lambda k: k['lhTS'], reverse=True)
        return(json.dumps(nodesList))


    def Run(self):
        self.positionBeacon
        print("Starting iMeshDashboard v%s" % (self.version,))
    
        print("MQTT ENABLED: %s" % self.config['MQTT']['enabled'])
        
        if ("Position" in self.config) and (self.config['Position']['enabled']=='True'):
            print("Position Beacon Enabled")
            self.positionBeacon = True
        if(self.positionBeacon):
            print("Setting postition info")
            self.scheduler.add_job(func=self.sendPosition, trigger='interval', id='sendPos', seconds=int(self.config['Position']['interval']))
            self.interface.sendPosition(float(self.config['Position']['lat']), float(self.config['Position']['lon']), int(self.config['Position']['alt']), int(time.time()))
            self.interface.localNode.waitForConfig()
            self.interface.localNode.writeConfig()
    
        if ("Reboot" in self.config) and (self.config['Reboot']['enabled']=='True'):
            print("Reboot Enabled")
            self.scheduler.add_job(func=self.reboot, trigger='interval', id='rebootNode', seconds=int(self.config['Reboot']['interval']))
        self.scheduler.start()
    
        if(self.config['MQTT']['enabled']=="True"):
            self.client.connect(self.config['MQTT']['host'], int(self.config['MQTT']['port']), int(self.config['MQTT']['keepalive']))
            self.client.loop_start()
        try:
            self.getNodeInfo()
            self.updateImeshMap(self.interface, None)
        except Exception as e:
            traceback.print_exc()   
            
if __name__ == '__main__':
    dashboard = iMeshDashboard()
    dashboard.Run()

    app = Flask(__name__, template_folder=dashboard.dataPath+'/templates')
    app.config['BASIC_AUTH_USERNAME'] = dashboard.config['AUTH']['username']
    app.config['BASIC_AUTH_PASSWORD'] = dashboard.config['AUTH']['password']
    basic_auth = BasicAuth(app)

    pub.subscribe(dashboard.updateImeshMap, "meshtastic.receive")
    pub.subscribe(dashboard.onGPIOreceive, "meshtastic.receive.data.REMOTE_HARDWARE_APP")
    atexit.register(lambda: self.interface.close())         
    

    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory(dashboard.dataPath+'/js', path)
    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory(dashboard.dataPath+'/css', path)
    @app.route('/img/<path:path>')
    def send_img(path):
        return send_from_directory(dashboard.dataPath+'/img', path)
    
    @app.route('/')
    def indexPage():
        dashboard.getNodes()
        radioPrefs = dashboard.interface.localNode.radioConfig.preferences
        return render_template('index.html', Title="iMesh Node Landing Page", 
                                             nodeInfo=dashboard.myNodeInfo, info=dashboard.interface.myInfo,
                                             appData=dashboard.appData, prefs=radioPrefs)

    @app.route('/lh')
    def lhPage():
        dashboard.getNodes()
        return render_template('lh.html', Title="Last Heard", 
                                          nodeInfo=dashboard.myNodeInfo, appData=dashboard.appData)
    
    @app.route('/map')
    def mapPage():
        dashboard.getNodes()
        return render_template('map.html', nodesList=dashboard.mapNodes, Title="Nodes Map", 
                                           nodeInfo=dashboard.myNodeInfo, appData=dashboard.appData)
    
    @app.route('/private/config')
    @basic_auth.required
    def configPage():
        dashboard.getNodes()
        radioPrefs = dashboard.interface.localNode.radioConfig.preferences
        return render_template('config.html', Title="Nodes Map", 
                                              nodeInfo=dashboard.myNodeInfo, appData=dashboard.appData,
                                              nodes=receivedNodes.items(), prefs=radioPrefs)
    
    @app.route('/getNodes')
    def printNodes():
        return dashboard.getNodes()
    
    @app.route('/getNodeInfo')
    def printNodeInfo():
        return dashboard.getNodeInfo()
    
    @app.route('/sendMessage', methods=['POST'])
    @basic_auth.required
    def sendMessage():
        if request.method == 'POST':
            msg = request.form['fmsg']
            dashboard.interface.sendText(msg, wantAck=True)
        return redirect(url_for('configPage'))
    
    @app.route('/setNode', methods=['POST'])
    @basic_auth.required
    def setNode():
        if request.method == 'POST':
            radioPrefs = dashboard.interface.localNode.radioConfig.preferences
            dashboard.interface.waitForConfig()
            dashboard.interface.localNode.setOwner(request.form['flongName'],  request.form['fshortName'])
            dashboard.interface.localNode.waitForConfig()
            setattr(radioPrefs, "region", int(request.form['fRegion']))
            alt = int(request.form['faltitude'])
            lat = float(request.form['flatitude'])
            lon = float(request.form['flongitude'])
            ts = int(time.time())
            if not dashboard.interface.myInfo.has_gps and not (dashboard.positionBeacon):
                setattr(radioPrefs, "fixed_position", True)
                dashboard.interface.sendPosition(lat, lon, alt, ts)
            else:
                print("Cannot set node parameters beacuse has gps: %s or has fixed position config in config file: %s" % 
                       (dashboard.interface.myInfo.has_gps, (dashboard.positionBeacon),))
            dashboard.interface.localNode.writeConfig()
        return redirect(url_for('configPage'))
    
    @app.route('/setGpio', methods=['POST'])
    @basic_auth.required
    def setGpio():
        if request.method == 'POST':
            tId = request.form['fTarget']
            tGpio = int(request.form['fGpio'])
            tValue = int(request.form['fValue'])
            bitmask = 0
            bitval = 0
            bitmask |= 1 << tGpio
            bitval |= tValue << tGpio
            r = remote_hardware_pb2.HardwareMessage()
            r.typ = remote_hardware_pb2.HardwareMessage.Type.WRITE_GPIOS
            r.gpio_mask = bitmask
            r.gpio_value = bitval
            dashboard.interface.sendData(r, tId, portnums_pb2.REMOTE_HARDWARE_APP, wantAck = True)
            print(f"Writing GPIO mask 0x{bitmask:x} with value 0x{bitval:x} to {tId}")
        return redirect(url_for('configPage'))
        
    
    @app.route('/getGpio')
    @basic_auth.required
    def getGpio():
        if request.method == 'GET':
            tId = request.args.get('target')
            tGpio = int(request.args.get('gpio'))
            bitmask = 0
            bitmask |= 1 << tGpio
            r = remote_hardware_pb2.HardwareMessage()
            r.typ = remote_hardware_pb2.HardwareMessage.Type.READ_GPIOS
            r.gpio_mask = bitmask
            dashboard.interface.sendData(r, tId, portnums_pb2.REMOTE_HARDWARE_APP, wantAck = True)
        #return redirect(url_for('configPage'))
        return (tId+" "+str(tGpio)+" "+hex(bitmask))
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            login_user(user)
    
            flask.flash('Logged in successfully.')
    
            next = flask.request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(400)
    
            return flask.redirect(next or flask.url_for('indexPage'))
        return flask.render_template('login.html', form=form)

    serve(app, host=dashboard.config['NET']['bind'], port=dashboard.config['NET']['port'])
    #only for debug!
    #app.run(debug=True, use_reloader=False)    
            