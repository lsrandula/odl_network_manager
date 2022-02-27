# from flask import *
import network_manager
from flask import Flask, render_template
from flask_navigation import Navigation
  
app = Flask(__name__)
nav = Navigation(app)

# Initializing navigations
nav.Bar('top', [
    nav.Item('Topology', 'topology'),
    nav.Item('View Flows', 'view_flows'),
])

@app.route('/')
def navpage():
    return render_template('navpage.html')

@app.route('/topology/')
def topology():
    network_manager.view_topology()
    return render_template('topology.html')
  
@app.route('/view_flows/')
def view_flows():
    network_manager.view_flowentries()
    return render_template('view_flows.html')
  
  
if __name__ == '__main__':
    app.run()

# @app.route('/index/')
# # @app.route('/index/<name>')
# def index(name=None):
#     return render_template('index.html', name=name)