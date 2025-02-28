from flask import Flask, jsonify, request
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Creating a Flask app
app = Flask(__name__)

@app.route('/make_call', methods=['GET'])
def make_call():
    try:
        # Retrieve Twilio credentials from environment variables
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_FROM_NUMBER')
        to_number = os.getenv('TWILIO_TO_NUMBER')

        if not all([account_sid, auth_token, from_number, to_number]):
            return jsonify({"error": "Missing environment variables"}), 500

        client = Client(account_sid, auth_token)

        call = client.calls.create(
            from_=from_number,
            to=to_number,
            url="http://demo.twilio.com/docs/voice.xml",
        )

        print(call.sid)
        return jsonify({"call_sid": call.sid}), 200

    except TwilioRestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    # Retrieve host and port from environment variables or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app.run(host=host, port=port, debug=True)
