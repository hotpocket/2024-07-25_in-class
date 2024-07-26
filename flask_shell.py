#!/usr/bin/env python
# Needed imports for this lab
from flask import Flask, redirect, request


# Flask constructor takes the name of
# current module (__name__) as argument
app = Flask(__name__)


# TODO: STEP 1
# Use a dictionary to simulate the database mapping for each short cod to long URL
# add 5 keys and 5 values (full-length URLs)
# keys and values should be strings

dict = {"good": "https://google.com", "evil": "https://facebook.com"}

"""
# verify static dict entries work

curl -I localhost:8080/good
# pre-add, verify what we are about to add does not exist
curl -I localhost:8080/omg

# POST: Create a new user
curl -Ss -XPOST "localhost:8080/url" \
    -H 'Content-Type: application/json' \
    -d '{"code": "omg", "url": "https://omg.com"}'

# verify it does exist
curl -I localhost:8080/omg

# DELETE: Remove a user - with a bad API KEY
curl -Ss -XDELETE "localhost:8080/url/omg" \
    -H 'Content-Type: application/json' \
    -H 'API-KEY: BAD-KEY-JUNK-HERE'

# DELETE: Remove a user - with a good API KEY
curl -Ss -XDELETE "localhost:8080/url/omg" \
    -H 'Content-Type: application/json' \
    -H 'API-KEY: TEST-API-KEY'

# verify it does not exist
curl -I localhost:8080/omg
"""


# Use this for last step of Lab
valid_api_key = 'TEST-API-KEY'




# Use of <converter: variable name> in the route() decorator.
@app.route('/<short_code>')
def allow(short_code):

    print("The short_code was: ", short_code);

    # Add code to test your dictionary for the short_code key
    # If the short-code was found call: return redirect(dict[short_code], code=301)
    if short_code in dict:
        return redirect(dict[short_code], code=301)

    else:
        return f'Your short-code was not found!'



#
# TODO: STEP Add CRUD APIs
#
# C.R.U.D. based API to either Retrieve (GET) a long-url or Create (POST) one
#
# The GET method will simply return the URL associated with the short_code
# The POST method will add a new entry into the dictionary using the data supplied in JSON format
# The DELETE method will remove the entry from the dictionary (no JSON body is needed)
#


#
# TODO: This is for the Insert CRUD API using POST
#
@app.route('/url', methods=['POST'])
def crud_api_post():

    # TODO: LAST STEP in Lab
    # Add a check to test if the incoming request contains the "API-KEY" Header and the value is correct
    # The value to test for is the variable: valid_api_key
    # Retun an error message if the api-key is not valid
    api_key = request.headers.get('API-KEY')

    # TODO: Test for a POST method, read the JSON body and update your dictionary
    if request.method == 'POST':
        data = request.json
        code = data.get('code')
        url = data.get('url')

        dict[code] = url

        return '\nShort-code: ' + code + ' is now pointing to: ' + url + '\n'
        """
        # POST: Create a new user
        curl -Ss -XPOST "localhost:8080/url" \
            -H 'Content-Type: application/json' \
            -d '{"code": "omg", "url": "https://omg.com"}'
        """


    # If something other than a POST request was received return an error
    # You could add code to accept a PUT method that will update an existing short-code
    else:
        return 'The method of: ' + request.method + ' is not supported for this url'


#
# TODO: This for the Delete CRUD API (and also the Retrieve CRUD API)
#
@app.route('/url/<short_code>', methods=['DELETE', 'GET'])
def crud_api_delete(short_code):

    # TODO: LAST STEP in Lab
    # Add a check to test if the incoming request contains the "API-KEY" Header and the value is correct
    # The value to test for is the variable: valid_api_key
    # Retun an error message if the api-key is not valid
    api_key = request.headers.get('API-KEY')

    # TODO: Retrieve CRUD API
    # Add a Retrieve CRUD based method to Retrieve the long URL associated with the given short_code
    if request.method == 'GET':
    #TEST-API-KEY
	# Test if the short exists in your dictionary, return a string message that shows the mapping
        # If the short code does not exist in your dictionary then return a string message indicating not found
        if None:
            return 'Short code: ' + short_code + " maps to: " + dict[short_code]
        else:
            return 'Short code: ' + short_code + ' was not found!'



    # TODO: Delete CRUD API
    # Add code to remove the short_code from your dictionary
    # Check if the short-code exists first before trying to delete it
    # Return a message that the short_code has been removed or not
    elif request.method == 'DELETE':
        if(api_key != valid_api_key):
            return 'API-KEY is not valid!'
        if short_code in dict:
            dict.pop(short_code)
            return 'Short-code: ' + short_code + ' has been removed'
        else:
            return 'The short-code: ' + short_code + ' was not found in the dictionary'


    # Any http methods other than GET or DELETE should return an error message.
    else:
        return 'The method of: ' + request.method + ' has not been implemented'






# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0", port=8080)

