import traceback
from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from flask_basicauth import BasicAuth
from waitress import serve
import requests
from iMeshDashboard import iMeshDashboard
from pubsub import pub
import atexit

def main():
    dashboard = iMeshDashboard()
    dashboard.Run()

    app = Flask(__name__, template_folder=dashboard.dataPath+'/templates')
    app.config['BASIC_AUTH_USERNAME'] = dashboard.config['AUTH']['username']
    app.config['BASIC_AUTH_PASSWORD'] = dashboard.config['AUTH']['password']
    basic_auth = BasicAuth(app)

    pub.subscribe(dashboard.updateImeshMap, "meshtastic.receive")
    pub.subscribe(dashboard.onGPIOreceive, "meshtastic.receive.data.REMOTE_HARDWARE_APP")
    atexit.register(lambda: dashboard.interface.close())         
    

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
                                              nodes=dashboard.receivedNodes.items(), prefs=radioPrefs)
    
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

if __name__ == '__main__':
    main()