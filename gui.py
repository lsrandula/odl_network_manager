import network_manager
from flask import Flask, render_template, request, redirect, url_for
from flask_navigation import Navigation
import os
  
app = Flask(__name__)
nav = Navigation(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initializing navigations
nav.Bar('top', [
    nav.Item('Topology', 'topology'),
    nav.Item('View Flow Entries', 'view_flows'),
    nav.Item('Add/Remove Flow Entries', 'flow_addremove_switch_select'),
    nav.Item('Add Batch Flow Entries', 'batch_flow_add'),
    nav.Item('Log Out', 'logout'),
])


@app.route('/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('topology'))
    return render_template('login.html', error=error)

@app.route('/topology/', methods=['GET','POST'])
def topology():
    try:
        network_manager.view_topology()
        image = [i for i in os.listdir('static/images') if i.endswith('.png')][0]
    except:
        image = None
    # return render_template('topology.html')
    return render_template('topology.html', topology=image)
  
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
    return render_template('render_flows.html', flows=flows, switch_id=switch_id)

@app.route('/flow_addremove_switch_select/')
def flow_addremove_switch_select():
    try:
        switches = network_manager.get_switchlist()
    except:
        switches = ["None"]
    return render_template('flow_addremove_switch_select.html', switches=switches)

@app.route('/add_flowentry/', methods=['POST', 'GET'])
def add_flowentry():
    if request.method == 'POST':
        switch_id = request.form.get('switch_id')
        print("Switch ID: ", switch_id)
    else:
        flows = ["None"]
    try:
        network_manager.view_topology()
        image = [i for i in os.listdir('static/images') if i.endswith('.png')][0]
    except:
        image = None
    return render_template('add_flowentry.html', switch_id=switch_id, topology=image)


@app.route('/add_flowentry_satus/', methods=['POST', 'GET'])
def add_flowentry_status():
    if request.method == 'POST':
        switch_id = request.form.get('switch_id')
        cookie = request.form.get('cookie')
        priority = request.form.get('priority')
        dest_ip = request.form.get('dest_ip')
        dest_mask = request.form.get('dest_mask')
        action = request.form.get('action')
        status = network_manager.add_flow(switch_id, priority, cookie, dest_ip, dest_mask, action)
        if (status.status_code==200):
            status= "Successful"
        else:
            status= "Unuccessful"
        print ("Add flow status: ", status)
    else:
        status = "Unsucessful"
    return render_template('add_flowentry_status.html', switch_id=switch_id, status=status)

@app.route('/remove_flowentry/', methods=['POST', 'GET'])
def remove_flowentry():
    switch_id = request.form.get('switch_id')
    print("Switch ID: ", switch_id[9:])
    flows = network_manager.view_flowentries(switch_id[9:])
    return render_template('remove_flowentry.html', flows=flows, switch_id=switch_id)

@app.route('/remove_flowentry_status/', methods=['POST', 'GET'])
def remove_flowentry_status():
    if request.method == 'POST':
        switch_id = request.form.get('switch_id')
        cookie = request.form.get('cookie')
        priority = request.form.get('priority')
        dest_ip = request.form.get('dest_ip')
        dest_mask = request.form.get('dest_mask')
        status = network_manager.remove_flow(switch_id, priority, cookie, dest_ip, dest_mask)
        if (status.status_code==200):
            status= "Successful"
        else:
            status= "Unuccessful"
        print ("Remove flow status: ", status)
    else:
        status = "Unsucessful"
    return render_template('remove_flowentry_status.html', switch_id=switch_id, status=status)

@app.route('/batch_flow_add/', methods=['POST', 'GET'])
def batch_flow_add():
    try:
        network_manager.view_topology()
        image = [i for i in os.listdir('static/images') if i.endswith('.png')][0]
    except:
        image = None
    return render_template('batch_flow_add.html', topology=image)

@app.route('/add_batchflowentry_status/', methods=['POST', 'GET'])
def add_batchflowentry_status():
    if request.method == 'POST':
        path = request.form.get('path')
        cookie = request.form.get('cookie')
        priority = request.form.get('priority')
        dest_ip = request.form.get('dest_ip')
        dest_mask = request.form.get('dest_mask')
        action = request.form.get('action')
        # print (path)
        segments = path.split("->")
        for i in range(len(segments)):
            id_action = segments[i].split(":")
            switch_id = "openflow:"+id_action[0][1:]
            action = id_action[1]
            print ("Switch ID: ", switch_id)
            print ("Action: ", action)
            status = network_manager.add_flow(switch_id, priority, cookie, dest_ip, dest_mask, action)
            if (status.status_code==200):
                status = "Successful"
            else:
                status = "Unuccessful"
    else:
        status = "Unsucessful"
    return render_template('add_batchflowentry_status.html', status=status)

@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    return render_template('logout.html')

  
if __name__ == '__main__':
    app.run()
