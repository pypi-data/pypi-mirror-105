#!/usr/bin/env python3

import json
import copy

import time
import timeago
from datetime import datetime
import paho.mqtt.client as mqtt
import meshtastic
from meshtastic import remote_hardware, portnums_pb2, remote_hardware_pb2
import configparser
from pkg_resources import get_distribution, DistributionNotFound
import os.path

import traceback

from flask_apscheduler import APScheduler


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
        
        if packet is not None:
            print("Packet received:")
            #print(packet)
            hop = packet.get('hopLimit', None)
            #print(hop)
            if (hop is not None) and (myNodeInfo['user']['id'] != packet.get('fromId')):
                print("Pushing received node info")
                client.publish("meshInfo/hopInfo", json.dumps({"receivedNode":packet.get('fromId'), "receiverNode":myNodeInfo['user']['id'],
                               "hopLimit":packet.get('hopLimit'), "rxTime":packet.get('rxTime')}))
                              
        try:
            for node, nodeValue in self.receivedNodes.items():       
                try:
                    self.mapNodes.append([nodeValue['user']['longName'], nodeValue['position']['latitude'],
                                     nodeValue['position']['longitude'], self.getMapNodeInfo(nodeValue)[0], self.getMapNodeInfo(nodeValue)[1], self.getHourDiff(nodeValue.get("lastHeard"))])
                    if node in self.oldReceivedNodes:
                        print(node +" - "+ nodeValue['user']['longName'] +" nodo presente")
                        if nodeValue.get("lastHeard") > self.oldReceivedNodes[node].get("lastHeard"):
                            print("aggiornato")
                            self.client.publish("receivedNodes/"+node, json.dumps(self.stripKey(nodeValue, "raw")))
                    else:
                        print("New node received: "+node +" - "+ nodeValue['user']['longName']+" @ "+str(nodeValue['position'].get('time')))
                        if(self.config['MQTT']['enabled']=="True"):
                            self.client.publish("receivedNodes/"+node, json.dumps(self.stripKey(nodeValue, "raw")))
                except Exception as e:
                    traceback.print_exc()
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
            