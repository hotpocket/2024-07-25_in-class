#!/usr/bin/env python
from flask import Flask, redirect, request

# vars

app = Flask(__name__)
# a few starter url short codes
shortCodes = {"good": "https://google.com", "evil": "https://facebook.com"}
# hard coded valid api key value for testing
valid_api_key = 'TEST-API-KEY'

# routes

# The standard use case: a person hits a short url & gets redirected
# Use of <converter: variable name> in the route() decorator.
@app.route('/<short_code>', methods=['GET']) # should only be valid for a GET
def allow(short_code):
    print("The short_code was: ", short_code);
    if short_code in shortCodes:
        return redirect(shortCodes[short_code], code=301)
    else:
        return 'Your short-code was not found!'


# Handle url CRUD (POST handles update & create in one)
@app.route('/url/<short_code>', methods=['DELETE', 'GET', 'POST'])
def crud_api_delete(short_code):
    is_valid_api_key = request.headers.get('API-KEY') == valid_api_key
    match request.method:
        case 'GET':
            if short_code not in shortCodes: return f'Short code: {short_code} was not found!'
            return f'Short code: {short_code} maps to:{shortCodes[short_code]}'
        case 'DELETE':
            if(not is_valid_api_key):  return 'API-KEY is not valid!'
            if short_code not in shortCodes: return f'short-code: {short_code} NOT FOUND'
            shortCodes.pop(short_code) # delete the url short code
            return f'Short-code: {short_code} DELETED'
        case 'POST':
            # now that this is shortened an inconsistency is revealed. the code should be provided on the url
            if(not is_valid_api_key): return 'API-KEY is not valid!'
            posted = request.json
            url, code = posted['url'], posted['code']
            if url is None or code is None:  return 'You must provide a url and a short-code'
            op = 'UPDATED' if code in shortCodes else 'CREATED'
            shortCodes[code] = url
            return f'\nShort-code: {op}.  {code} now points to: {url} \n'
        case _: # default/unmatched case
            return f'{request.method} Not implemented not implemented'


# start the flask app on port 8080 if run as a script
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

