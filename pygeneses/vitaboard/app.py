from flask import Flask, request, render_template, redirect, flash, jsonify
import os
import pkgutil

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'my-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        file_location = request.form['file_location']
        speed = request.form['speed']

        with open('pass_params.txt', 'w') as file:
            file.write(file_location + '\n')
            file.write(speed + '\n')

        visualizer_contents = pkgutil.get_data(__name__, "visualizer.py").decode()
        with open('./visualizer.py', 'w') as file:
            file.write(visualizer_contents)

        os.system('python visualizer.py')

        os.remove('pass_params.txt')
        os.remove('visualizer.py')

        return jsonify({"status": "Visualizer ran successfully!"})

if __name__ == "__main__":
    app.run()
