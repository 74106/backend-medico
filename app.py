from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add custom AI to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'custom_ai'))
from medical_ai import get_medical_advice

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'Backend is working'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        
        if not user_message:
            return jsonify({'reply': 'No message provided'}), 400
        
        # Use custom medical AI
        ai_response = get_medical_advice(user_message)
        
        return jsonify({'reply': ai_response}), 200
    
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({'reply': f'Server error: {str(error)}'}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
