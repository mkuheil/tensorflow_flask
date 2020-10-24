from flask import Flask, render_template, request
import numpy as np 
import tensorflow as tf 
import tensorflow_hub as hub
import PIL.Image as Image

# Create a flask app
app = Flask(__name__,
	# Name of html file folder
  template_folder='templates',  
  # Name of directory for static files
	static_folder='static'  
)

# Part I: pages with/without templates 
# '/' for the default, index, or home page
@app.route('/')  
def home():
	return "<h1> Wow this is the main page! </h1>"

# '/help' for the help page
@app.route('/help')  
def help():
	return "<h1> this is the help page! </h1>"

# '/hello' for the hello page
@app.route('/hello')  
def hello():
	return render_template('hello.html')


# Part II: Passing parameters 
# method 1 to get parameter
@app.route('/welcome/<name>')  
def welcome(name):
	return render_template('welcome.html', name=name)


# method 2 to get parameter
# show the post with the given id, the id is an integer
# to call /post/10
@app.route('/post/<int:post_id>')
def show_post(post_id):    
  return 'Post %d' % post_id


# method 3 to get parameter
@app.route('/greeting')
def greeting():
  name = request.args.get('name')
  # to call /greeting?name="Ahmed"
  return render_template('welcome.html', name=name)

# method 4 to get parameter
# to call /calc?x=10&y=5
@app.route('/calc')
def calc():
  x = request.args.get('x')
  y = request.args.get('y')
  msg = '<h1> {} + {} = {} </h1>'.format(x, y, int(x) + int(y))
  msg += '\n<h1> {} - {} = {} </h1>'.format(x, y, int(x) - int(y))
  msg += '\n<h1> {} * {} = {} </h1>'.format(x, y, int(x) * int(y))
  msg += '\n<h1> {} / {} = {} </h1>'.format(x, y, int(x) / int(y))
  return msg


@app.route('/calculator', methods=['GET', 'POST'])
def calculator2():
  result = ''
  n1 = ''
  n2 = ''
  op = ''
  if request.method == 'POST':
      n1 = request.form['num1']
      n2 = request.form['num2']
      op = request.form['op']
      if n1 and n2:
          try:
              result = eval('{}{}{}'.format(n1, op, n2))
              print(result)
          except BaseException as error:
              result = 'error: {}'.format(error)
              print(result)
      else:
          result = 'please fill the form'
  return render_template('calculator.html', n1=n1, op=op, n2=n2, result=result)



@app.route('/mostfreqtable', methods=['GET', 'POST'])
def mostfreqtable():
  counts = {}
  if request.method == 'POST':
      text = request.form['mytext']
      if not text:
          result = 'please fill the form'
          print(result)
      else:
          for word in text.split():
              counts[word] = counts.get(word, 0) + 1

  return render_template('wordfreq.html', counts=counts)


##################################################
# PART II RESTFUL API 

from flask_restful import Resource, Api
api = Api(app)
weather_data = {
    'Gaza': {'temp': 19, 'wind': 16, 'humidity': 80},
    'Khanyounis': {'temp': 30, 'wind': 10, 'humidity': 20},
    'Rafah': {'temp': 23, 'wind': 10, 'humidity': 80}
}


class Weather(Resource):
  def get(self, city):
      weather_city = weather_data.get(city)
      return {city: weather_city}

api.add_resource(Weather, '/weather/<city>')


classifier_model ="https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"

IMAGE_SHAPE = (224, 224)

classifier = tf.keras.Sequential([
    hub.KerasLayer(classifier_model, input_shape=IMAGE_SHAPE+(3,))
]) 

labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = np.array(open(labels_path).read().splitlines())

# 'https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg'
@app.route('/classifiy')
def classifiy():
  myurl = request.args.get('url')
  grace_hopper = tf.keras.utils.get_file('image.jpg', myurl)
  grace_hopper = Image.open(grace_hopper).resize(IMAGE_SHAPE)
  result = classifier.predict(grace_hopper[np.newaxis, ...])
  predicted_class = np.argmax(result[0], axis=-1)
  predicted_class_name = imagenet_labels[predicted_class]
  
  return predicted_class_name




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