import random, string
from flask import Flask, render_template

# Create a flask app
app = Flask(__name__,
	# Name of html file folder
  template_folder='templates',  
  # Name of directory for static files
	static_folder='static'  
)


@app.route('/')  # '/' for the default page
def home():
	return "<h1> Wow this is the main page! </h1>"


@app.route('/help')  # '/' for the default page
def help():
	return "<h1> this is the help page! </h1>"

@app.route('/hello')  # '/' for the default page
def hello():
	render_template('hello.html')















# Makes sure this is the main process
if __name__ == "__main__":  
	# Starts the site
  app.run( 
		# EStablishes the host, required for repl to detect the site
    host='0.0.0.0',  
    # Randomly select the port the machine hosts on.
		port=random.randint(2000, 9000) , 
    debug=True
	)