from web_rekollect import app

@app.route('/api/<file_name>')
def check_file_name(file_name):
    '''Returns all data for file_name if file_name already exists'''
    pass

@app.route('/api/<file_name>/<plugin>', methods=['GET', 'POST'])
def use_plugin(file_name, plugin):
    '''For GET request, return JSON for results
       For POST requests, run that plugin
    '''
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
