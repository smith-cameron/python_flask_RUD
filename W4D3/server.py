from flask_app import app
# import controllers 
from flask_app.controllers import users_controller


if __name__ == "__main__":
  app.run(debug=True)
  #optional host='localhost', port=5001