# 1. Create a basic API in Azure (as we did in class) that tells you how to access the different 
# endpoints when you go to the home page. You should have the following endpoints:

#!/usr/bin/env python

from flask import Flask, json, render_template, request
import os

#create instance of Flask app
app = Flask(__name__)

# a. A /all endpoint that displays all of the nobel.json data
@app.route("/")
def all_info():
    json_url = os.path.join(app.static_folder,"","nobel.json")
    data_json = json.load(open(json_url))
    return render_template('index.html',data=data_json)

# b. A / GET endpoint that allows for you to pass in any year and shows you the Nobel prizes from that
# year. No need to create an HTML page for this, but you can if you want.
@app.route("/<year>", methods=['GET'])
def prize_year(year):
    json_url = os.path.join(app.static_folder,"","nobel.json")
    data_json = json.load(open(json_url))
    data = data_json["prizes"]
    if request.method == 'GET':
        data_json = json.load(open(json_url))
        data = data_json['prizes']
        year = request.view_args['year']
        output_data = [x for x in data if x['year']==year]
        return render_template('index.html',data=output_data)

# c. A /add POST endpoint that lets you add additional data
@app.route("/year/<year>",methods=['GET','POST'])
def add_info(year):
    json_url = os.path.join(app.static_folder,"","nobel.json")
    if request.method == 'GET':
        data_json = json.load(open(json_url))
        data = data_json['prizes']
        year = request.view_args['year']
        output_data = [x for x in data if x['year']==year]
        return render_template('form.html',html_page_text=output_data)
    elif request.method == 'POST':
        year = request.form['year']
        category=request.form['category']
        firstname = request.form['firstname']
        surname = request.form['surname']
        reason = request.form['motivation']
        laureate_dict = { "year":year,
                    "category":category,
                    "firstname":firstname,
                    "surname":surname,
                    "reason":reason
                    }

        with open(json_url,"r+") as file:
            data_json = json.load(file)
            data_json["prizes"].append(laureate_dict)
            json.dump(data_json, file)
        
        #Adding text
        text_success = "Data successfully added: " + str(laureate_dict)
        return render_template('form.html', html_page_text=text_success) 

if __name__ == "__main__":
    app.run(debug=True)

