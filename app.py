# import the flask class  from the flask template
from  flask import Flask, render_template

# create the application  object
app = Flask(__name__)

# use decorators  to link the function to  a url
@app.route('/')
def home():
	return "Hello Refuge Wise" # return  a string 


@app.route('/welcome')
def welcome():
	return render_template("welcome.html") #return a template


#start the server with the  'run()' method

if __name__ == '__main__':
	app.run(debug=True)