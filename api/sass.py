from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource 
from datetime import datetime
import sys
from model.sasses import Sass

# Create score blueprint for API
sasses_bp = Blueprint("sasses_bp", __name__, url_prefix='/api/sass')
# Score API derived from blueprint
sass_api = Api(sasses_bp)

# Define class for the API
class SassesAPI:
    # Define class to create a user using the POST method
    class SassCreate(Resource):    
        # def post(self) creates POST method
        def post(self):
            # Gets the data from postman or frontend
            data = request.get_json()

            # Gets the username, checks if the username is exactly 3 characters. If it isn't 3 characters, POST is terminated
            username = data.get('username')
            if username is None or len(username) <= 0:
                return {'message': f'username is not 3 characters'}, 210
                
            question1 = data.get('question1')
            if question1 is None or len(question1) <= 0:
                return {'message': f'Response to question 1 does not exist.'}, 210 
            
            question2 = data.get('question2')
            if question2 is None or len(question2) <= 0:
                return {'message': f'Response to question 2 does not exist.'}, 210 
            
            question3 = data.get('question3')
            if question3 is None or len(question3) <= 0:
                return {'message': f'Response to question 3 does not exist.'}, 210 
            
            question4 = data.get('question4')
            if question4 is None or len(question4) <= 0:
                return {'message': f'Response to question 4 does not exist.'}, 210 
            
            # Gets the date of score
            doquestion = data.get('doquestion')
            
            # sob uses class Score to create a user
            sassProfile = Sass(username=username,
                       question1=question1,
                       question2=question2,
                       question3=question3,
                       question4=question4)

            # Checks if date of score exists, reformats it to mm-dd-yyyy
            if doquestion is not None:
                try:
                    sassProfile.doquestion = datetime.strptime(doquestion, '%m-%d-%Y').date()
                except:
                    return {'message': f'Date obtained has a format error {doquestion}, must be mm-dd-yyyy'}, 210
            
            # CREATE operation: creates user
            user = sassProfile.create()
            if user:
                # make_dict() function to return a dictionary for the user
                return jsonify(user.read())
            # returns error message if unable to return a dictionary
            return {'message': f'Processed {username}, there is likely a format error'}, 210

    # GET method displays the data from the API
    class SassListAPI(Resource):
        # def get(self) does the GET method
        def get(self):
            # Gets all the data from Score and returns a dictionary
            sasses = Sass.query.all()
            json_ready = [user.read() for user in sasses]
            return jsonify(json_ready)

    # PUT method updates data in the API
    class SassUpdate(Resource):
        # def put(self) does the PUT method
        def put(self):
            # Gets the data from postman or frontend
            data = request.get_json()

            username = data.get('username')
            if username is None or len(username) <= 0:
                return {'message': f'username is not 3 characters'}, 210
                
            question1 = data.get('question1')
            if question1 is None or len(question1) <= 0:
                return {'message': f'Response to question 1 does not exist.'}, 210 
            
            question2 = data.get('question2')
            if question2 is None or len(question2) <= 0:
                return {'message': f'Response to question 2 does not exist.'}, 210 
            
            question3 = data.get('question3')
            if question3 is None or len(question3) <= 0:
                return {'message': f'Response to question 3 does not exist.'}, 210 
            
            question4 = data.get('question4')
            if question4 is None or len(question4) <= 0:
                return {'message': f'Response to question 4 does not exist.'}, 210 

            # Gets the user through the username
            userUpdating = Sass.query.filter_by(_username = username).first()
            if userUpdating:
                # Updates the score for the user
                userUpdating.update(username = username,
                                    question1 = question1,
                                    question2 = question2,
                                    question3 = question3,
                                    question4 = question4)
                # Returns a dictionary to confirm that the score was updated
                return jsonify(userUpdating.read())
            else:
                # Error message if update fails
                return {'message': f'{username} not found'}, 210

    # Delete method deletes data in the API
    class SassDelete(Resource):
        # def delete(self) does the DELETE method
        def delete(self):
            # Gets the data from postman or frontend
            data = request.get_json()

            # Gets the ID
            getID = data.get('id')

            # Gets the user through the ID
            historyDeleting = Sass.query.get(getID)
            if historyDeleting:
                # Deletes the user according to its ID number
                historyDeleting.delete()
                return {'message': f'Profile #{getID} deleted'}, 210
            else:
                # Error message if delete fails
                return {'message': f'Profile #{getID} not found'}, 210
    
    # Endpoints, uses URL prefix and '/' to refer to different classes which corresponds to different methods
    sass_api.add_resource(SassCreate, '/addSass')
    sass_api.add_resource(SassListAPI, '/sassList')
    sass_api.add_resource(SassUpdate, '/updateSass')
    sass_api.add_resource(SassDelete, '/deleteSass')