# Backend API for VitaBoard

# Import required libraries
from flask import Flask, request, render_template, redirect, flash, jsonify
import os
import pkgutil
import json

# Import functions to compute values used in VitaBoard
from .graph_gen import get_life_stats, tsne, get_parents, get_children

# Instantiate flask app
app = Flask(__name__)

# Basic config for flask app
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = "my-secret-key"
app.config["SESSION_TYPE"] = "filesystem"


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Index (/) route

    Methods
    =======
    GET
        : Get index.html (main file for VitaBoard)
    POST
        : Show visualizer when provided with the full path of log file and speed
    """

    if request.method == "GET":
        """
        Returns index.html (file which contains template for VitaBoard)
        """

        # Retur index.html from templates
        return render_template("index.html")

    elif request.method == "POST":
        """
            file_location (str)
                : Full path of log file which is to be visualized
            speed         (int)
                : Speed (in seconds) with which the visualizer's frame should change
        """

        # Get file_location and speed from AJAX call
        file_location = request.form["file_location"]
        speed = request.form["speed"]

        # Check if file exists or not
        if not os.path.exists(file_location):
            return jsonify(
                {
                    "title": "Error",
                    "text": "The location " + file_location + " does not exist",
                    "icon": "error",
                }
            )

        # Check if the file is of npy type or not
        if ".npy" not in file_location:
            return jsonify(
                {
                    "title": "Error",
                    "text": "You need to pass a npy file",
                    "icon": "error",
                }
            )

        # Copy the parameters (file_location and speed) into a text file to be passed to the visualizer
        with open("pass_params.txt", "w") as file:
            file.write(file_location + "\n")
            file.write(speed + "\n")

        # From the pygeneses installation copy the script called visualizer.py to current working directory
        # (from where VitaBoard server is started)
        # This is done because both flask and pygame require main thread which could not be given if they are not different processes altogether
        visualizer_contents = pkgutil.get_data(__name__, "visualizer.py").decode()
        with open("./visualizer.py", "w") as file:
            file.write(visualizer_contents)

        # Run the visualizer.py file which takes input from pass_params.txt (which now has the current params)
        os.system("python visualizer.py")

        # After the visualizer runs delete both the visualizer and pass_params from current working directory
        os.remove("pass_params.txt")
        os.remove("visualizer.py")

        # Return success message
        return jsonify(
            {
                "title": "Success",
                "text": "Visualizer ran successfully",
                "icon": "success",
            }
        )


@app.route("/groups", methods=["POST"])
def groups():
    """
    Groups (/groups) route

    Methods
    =======
    POST
        : Returns t-SNE embeddings of all the agents in a particular log directory
    """

    if request.method == "POST":
        """
            location (str)
                : Full path of log directory to compute t-SNE
        """

        # Get the location of log directory from AJAX call
        location = request.form["location"]

        # Check if the directory exists or not
        if not os.path.exists(location):
            return jsonify(
                {
                    "title": "Error",
                    "text": "The location " + location + " does not exist",
                    "icon": "error",
                }
            )

        # Check if Embeddings directory exists inside the directory or not
        if not os.path.exists(os.path.join(location, "Embeddings")):
            return jsonify(
                {
                    "title": "Error",
                    "text": "The location "
                    + location
                    + " does not have any embeddings",
                    "icon": "error",
                }
            )

        # Get coordinates in 2D space after training t-SNE
        coord = tsne(location)

        # If there are no npy files inside Embeddings folder (no one died before stopping training) then throw error
        if coord == -1:
            return jsonify(
                {
                    "title": "Error",
                    "text": "The location "
                    + location
                    + " does not have any embeddings",
                    "icon": "error",
                }
            )

        # Return success message along with 2D coordinates for n-D embedding
        return jsonify(
            {
                "title": "Success",
                "text": "Groups generated successfully",
                "icon": "success",
                "coord": coord,
            }
        )


@app.route("/stats", methods=["POST"])
def stats():
    """
    Stats (/stats) route

    Methods
    =======
    POST
        : Returns statistics like mean, variance and quality of life based on agent's age of death
    """

    if request.method == "POST":
        """
            location (str)
                : Full path of log directory to compute statistics
        """

        # Get the location of log directory from AJAX call
        location = request.form["location"]

        # Check if the directory exists or not
        if not os.path.exists(location):
            return jsonify(
                {
                    "title": "Error",
                    "text": "The location " + location + " does not exist",
                    "icon": "error",
                }
            )

        # Get the mean, variance and qof (Quality of life)
        mean, variance, qof = get_life_stats(location)

        # If there were no npy files then the mean, variance and qof values will be -1 (which means no one died before training was stopped)
        # throw an error in this case
        if mean == -1 and variance == -1 and qof == -1:
            return jsonify(
                {
                    "title": "Error",
                    "text": "The location " + location + " does not have any log files",
                    "icon": "error",
                }
            )

        # Return success message along with the stats (mean, variance, qof)
        return jsonify(
            {
                "title": "Success",
                "text": "Stats generated successfully",
                "icon": "success",
                "mean": mean,
                "variance": variance,
                "qof": qof,
            }
        )


@app.route("/lineage", methods=["POST"])
def lineage():
    """
    Lineage (/lineage) route

    Methods
    =======
    POST
        : Returns family tree (both ancestors and successors) of an agent whose log file location is passed
    """

    if request.method == "POST":
        """
            location (str)
                : Full path of log file containing information about a particular agent whose family tree is to be generated
        """

        # Get the location of log directory from AJAX call
        filename = request.form["filename"]

        # Check if the directory exists or not
        if not os.path.exists(filename):
            return jsonify(
                {
                    "title": "Error",
                    "text": "The location " + filename + " does not exist",
                    "icon": "error",
                }
            )

        # Check if the file is of npy type or not
        if ".npy" not in filename:
            return jsonify(
                {
                    "title": "Error",
                    "text": "You need to pass a npy file",
                    "icon": "error",
                }
            )

        # Split filename into directory name and filename
        dir = os.path.dirname(filename)
        filename = os.path.basename(filename)

        # Get the list of ancestors recusrively until the initial population
        ancestor_list = []
        get_parents(dir, filename, ancestor_list)

        # Sort ancestor_list according to level of depth in tree
        ancestor_list = sorted(
            ancestor_list, key=lambda k: int(k["level"]), reverse=True
        )

        # Dump ancestor_list into JSON object
        ancestor_list = json.dumps(ancestor_list)

        # Get the list of successors recusrively until an agent is found without any offspring(s)
        successor_list = []
        get_children(dir, filename, successor_list)

        # Sort successor_list according to level of depth in tree
        successor_list = sorted(successor_list, key=lambda k: int(k["level"]))

        # Dump successor_list into JSON object
        successor_list = json.dumps(successor_list)

        # Return success message along with ancestor_list and successor_list
        return jsonify(
            {
                "title": "Success",
                "text": "Stats generated successfully",
                "icon": "success",
                "ancestor_list": ancestor_list,
                "successor_list": successor_list,
            }
        )

# Run the app if in __main__ namespace
if __name__ == "__main__":
    app.run()
