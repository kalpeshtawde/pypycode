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
    project_id = data.get('project_id')
    
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
            "project_id": project_id,
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

@app.route('/parse-message', methods=['POST'])
def parse_message():
    """Single LLM call: classify create/update intent AND extract problem count."""
    data = request.get_json() or {}
    prompt = (data.get('prompt') or '').strip()
    has_existing_project = data.get('has_existing_project', False)
    project_name = (data.get('project_name') or '').strip()

    if not prompt:
        return jsonify({'intent': 'unclear', 'total': None}), 200

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        from pydantic import BaseModel, Field
        from typing import Optional, Literal

        class MessageParsing(BaseModel):
            intent: Literal['create', 'update', 'unclear'] = Field(
                description="'create' = new project, 'update' = add to existing, 'unclear' = cannot determine"
            )
            total: Optional[int] = Field(
                default=None,
                description="Number of problems explicitly requested (1-200), or null if not mentioned",
            )

        context = (
            f"The user {'has' if has_existing_project else 'does not have'} an existing project"
            + (f" named \"{project_name}\"" if project_name else "")
            + "."
        )
        llm = ChatOpenAI(temperature=0, model='gpt-4o-mini')
        parser = llm.with_structured_output(MessageParsing)

        result = parser.invoke([
            SystemMessage(content=(
                "You help users manage coding practice projects. "
                "Given the user's message, determine:\n"
                "1. intent: 'create' (new project from scratch), 'update' (add problems to existing), or 'unclear'\n"
                "2. total: the number of problems they want (if explicitly stated), else null\n\n"
                f"Context: {context}\n"
                "If the user has no existing project and intent is ambiguous, prefer 'create'.\n"
                "Only return 'unclear' if you genuinely cannot tell what the user wants."
            )),
            HumanMessage(content=prompt),
        ])

        return jsonify({'intent': result.intent, 'total': result.total}), 200

    except Exception as e:
        logger.error(f"Error in parse_message: {e}")
        return jsonify({'intent': 'unclear', 'total': None}), 200


@app.route('/extract-intent', methods=['POST'])
def extract_intent():
    """Use LLM to extract the requested problem count from a user prompt."""
    data = request.get_json() or {}
    prompt = (data.get('prompt') or '').strip()
    if not prompt:
        return jsonify({'total': None}), 200

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        from pydantic import BaseModel, Field
        from typing import Optional

        class IntentExtraction(BaseModel):
            total: Optional[int] = Field(
                default=None,
                description="Number of coding problems/questions the user explicitly wants, or null if not mentioned",
            )

        llm = ChatOpenAI(temperature=0, model='gpt-4o-mini')
        extractor = llm.with_structured_output(IntentExtraction)

        result = extractor.invoke([
            SystemMessage(content=(
                "Extract the number of coding problems or questions the user explicitly requests. "
                "Examples: '10 problems' → 10, 'give me 15' → 15, 'I want 20 questions' → 20. "
                "If no specific number is stated, return null."
            )),
            HumanMessage(content=prompt),
        ])

        return jsonify({'total': result.total}), 200

    except Exception as e:
        logger.error(f"Error in extract_intent: {e}")
        return jsonify({'total': None}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
