from flask import Flask, request, jsonify
import os
import logging
import traceback
import asyncio

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/generate', methods=['POST'])
def generate():
    """Generate a project from a prompt using the Vega agent."""
    data = request.get_json()
    
    prompt = data.get('prompt')
    problem_count = data.get('problem_count', 20)
    auth_token = data.get('auth_token')
    user_id = data.get('user_id')
    
    if not prompt:
        return jsonify({'error': 'prompt is required'}), 400
    
    if not auth_token:
        return jsonify({'error': 'auth_token is required'}), 400
    
    try:
        from agent.nodes import graph as vega_graph
        from agent.state import AgentState
        
        logger.info(f"Generating project for user {user_id} with prompt: {prompt[:50]}...")
        
        # Initialize the state with the prompt and auth token
        initial_state: AgentState = {
            "user_id": user_id,
            "goal": prompt,
            "total": problem_count,
            "auth_token": auth_token,
            "stats": None,
            "tag_stats": None,
            "tag_ranking": None,
            "level": None,
            "strategy": None,
            "difficulty_percent": None,
            "difficulty_counts": None,
            "tag_weights": None,
            "focus_tags": None,
            "strategy_reason": None,
            "selected_problems": None,
            "ignore_slugs": [],
            "project": None,
            "project_id": None,
            "selection": None,
            "retry_count": 0,
        }
        
        # Run the graph asynchronously
        result = asyncio.run(vega_graph.ainvoke(initial_state))
        
        logger.info(f"Graph invocation completed successfully")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in generate: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
