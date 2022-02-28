# from flask import *
import network_manager
from flask import Flask, render_template, request
from flask_navigation import Navigation
  
app = Flask(__name__)
nav = Navigation(app)

# Initializing navigations
nav.Bar('top', [
    nav.Item('Topology', 'topology'),
    nav.Item('View Flows', 'view_flows'),
])

# @app.route('/')
# def navpage():
#     return render_template('navpage.html')

@app.route('/')
@app.route('/topology/')
def topology():
    try:
        network_manager.view_topology()
    except:
        pass
    return render_template('topology.html')
  
@app.route('/view_flows/')
def view_flows():
    try:
        switches = network_manager.get_switchlist()
    except:
        switches = ["None"]
    return render_template('view_flows.html', switches=switches)

@app.route('/render_flows/', methods=['POST', 'GET'])
def render_flows():
    if request.method == 'POST':
        switch_id = request.form.get('switch_id')
        print("Switch ID: ", switch_id[9:])
        flows = network_manager.view_flowentries(switch_id[9:])
    else:
        flows = ["None"]
    return render_template('render_flows.html', flows=flows)

# @app.route('/render_flows/')
# def render_flows(switch_id):
#     print ("SWITCH ID: ",switch_id[10:])
#     network_manager.view_flowentries(switch_id[10:])
#     return render_template('render_flows.html')

  
if __name__ == '__main__':
    app.run()

# @app.route('/index/')
# # @app.route('/index/<name>')
# def index(name=None):
#     return render_template('index.html', name=name)