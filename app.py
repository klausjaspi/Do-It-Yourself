from flask import Flask, jsonify, request
from http import HTTPStatus


app = Flask(__name__)

instructions = [{
    "id": 1,
    "name": "Paint a car",
    "description": "Instructions how to paint a car",
    "steps": ["Remove the old paint", "Tape the line areas like window edges etc", "Take your pressure gun and paint",
              "Remove the painter's tape"],
    "tools": ["Painter's tape", "pressure paint gun", "paint", "painting suit"],
    "cost": 1200,
    "duration": 10
},

    {"id": 2,
     "name": "Paint a house",
     "description": "Instructions how to paint a house",
     "steps": ["Sand dust the walls", "take your brush", "Paint"],
     "tools": ["paint brush", "painting gears"],
     "cost": 9,
     "duration": 9
     }]


@app.route('/instructions', methods=['GET'])
def get_instructions():
    return jsonify({'data': instructions})


@app.route('/instructions/<int:instruction_id>', methods=['GET'])
def get_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if instruction['id'] == instruction_id), None)
    if instruction:
        return jsonify(instruction)

    return jsonify({'message': 'instruction not found'}), HTTPStatus.NOT_FOUND


@app.route('/instructions', methods=['POST'])
def create_instruction():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    steps = data.get('steps')
    tools = data.get('tools')
    cost = data.get('cost')
    duration = data.get('duration')

    instruction = {
        'id': len(instructions) + 1,
        'name': name,
        'description': description,
        'steps': steps,
        'tools': tools,
        'cost': cost,
        'duration': duration
    }

    instructions.append(instruction)
    return jsonify(instruction), HTTPStatus.CREATED


@app.route('/instructions/<int:instruction_id>', methods=['DELETE'])
def delete_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if instruction['id'] == instruction_id), None)

    if not instruction:
        return jsonify({'message': 'Instruction not found'}), HTTPStatus.NOT_FOUND

    instructions.remove(instruction)

    return '', HTTPStatus.NO_CONTENT


@app.route('/instruction/<int:instruction_id>', methods=['PUT'])
def update_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if instruction['id'] == instruction_id), None)
    data = request.get_json()
    if not instruction:
        return jsonify({'message': 'instruction not found'}), HTTPStatus.NOT_FOUND

    instruction.update(
        {
            'name': data.get('name'),
            'description': data.get('description'),
            'steps': data.get('steps'),
            'tools': data.get('tools'),
            'cost': data.get('cost'),
            'duration': data.get('duration')
        }
    )

    instruction.is_publish = True

    return jsonify(instruction), HTTPStatus.OK


if __name__ == '__main__':
    app.run(port=5000, debug=True)