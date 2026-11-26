"""
API Flask para o sistema de gestão hospitalar.
"""

import sys
import os

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from services.hospital_service import HospitalService

app = Flask(__name__)
CORS(app)

# Instância única do serviço
hospital_service = HospitalService()


@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')


@app.route('/api/patients', methods=['POST'])
def register_patient():
    """Cadastra um novo paciente."""
    data = request.json
    name = data.get('name')
    priority = data.get('priority')
    
    if not name or priority is None:
        return jsonify({'success': False, 'error': 'Nome e prioridade são obrigatórios'}), 400
    
    result = hospital_service.register_patient(name, priority)
    
    if result['success']:
        return jsonify(result), 201
    return jsonify(result), 400


@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Busca um paciente por ID."""
    patient = hospital_service.find_patient_by_id(patient_id)
    
    if patient:
        return jsonify({'success': True, 'patient': patient}), 200
    return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404


@app.route('/api/patients/<int:patient_id>/reclassify', methods=['PUT'])
def reclassify_patient(patient_id):
    """Reclassifica a prioridade de um paciente."""
    data = request.json
    new_priority = data.get('priority')
    
    if new_priority is None:
        return jsonify({'success': False, 'error': 'Nova prioridade é obrigatória'}), 400
    
    result = hospital_service.reclassify_patient(patient_id, new_priority)
    
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 400


@app.route('/api/patients/<int:patient_id>/cancel', methods=['DELETE'])
def cancel_patient(patient_id):
    """Cancela/remove um paciente."""
    result = hospital_service.cancel_patient(patient_id)
    
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 400


@app.route('/api/patients/arrival', methods=['GET'])
def list_patients_by_arrival():
    """Lista pacientes por ordem de chegada."""
    patients = hospital_service.list_patients_by_arrival()
    return jsonify({'success': True, 'patients': patients}), 200


@app.route('/api/patients/queue', methods=['GET'])
def get_patient_queue():
    """Retorna a fila de pacientes ordenada por prioridade."""
    queue = hospital_service.get_patient_queue()
    return jsonify({'success': True, 'queue': queue}), 200


@app.route('/api/doctors', methods=['POST'])
def register_doctor():
    """Cadastra um novo médico."""
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'success': False, 'error': 'Nome é obrigatório'}), 400
    
    result = hospital_service.register_doctor(name)
    
    if result['success']:
        return jsonify(result), 201
    return jsonify(result), 400


@app.route('/api/doctors/available', methods=['GET'])
def get_available_doctors():
    """Retorna médicos disponíveis ordenados por carga."""
    doctors = hospital_service.get_available_doctors()
    return jsonify({'success': True, 'doctors': doctors}), 200


@app.route('/api/attendance/call', methods=['POST'])
def call_next_patient():
    """Chama o próximo paciente para atendimento."""
    result = hospital_service.call_next_patient()
    
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 400


@app.route('/api/attendance/conclude', methods=['POST'])
def conclude_attendance():
    """Conclui o atendimento de um paciente."""
    data = request.json
    patient_id = data.get('patient_id')
    
    if patient_id is None:
        return jsonify({'success': False, 'error': 'ID do paciente é obrigatório'}), 400
    
    result = hospital_service.conclude_attendance(patient_id)
    
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 400


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas do sistema."""
    stats = hospital_service.get_stats()
    return jsonify({'success': True, 'stats': stats}), 200


@app.route('/api/validate', methods=['GET'])
def validate_system():
    """Valida a consistência do sistema."""
    validation = hospital_service.validate_consistency()
    return jsonify({'success': True, 'validation': validation}), 200


@app.route('/api/detailed-info', methods=['GET'])
def get_detailed_info():
    """Retorna informações detalhadas para visualização."""
    info = hospital_service.get_detailed_info()
    return jsonify({'success': True, 'info': info}), 200


@app.route('/api/test/collision', methods=['POST'])
def test_collision():
    """Teste de colisão na Hash."""
    # Força IDs que colidem com capacidade 10
    # IDs 5 e 15 colidem: 5 % 10 = 5, 15 % 10 = 5
    hospital_service.next_patient_id = 5
    
    patient1 = hospital_service.register_patient('Colisão ID 5', 3)
    
    # Força ID 15 para colidir com ID 5
    hospital_service.next_patient_id = 15
    patient2 = hospital_service.register_patient('Colisão ID 15', 3)
    
    # Força ID 25 para também colidir (25 % 10 = 5)
    hospital_service.next_patient_id = 25
    patient3 = hospital_service.register_patient('Colisão ID 25', 3)
    
    return jsonify({
        'success': True,
        'message': 'Criados pacientes com IDs 5, 15 e 25. Todos colidem no bucket 5 (capacidade 10)',
        'patients': [patient1, patient2, patient3],
        'hash_buckets': hospital_service.hash_table.get_buckets_info()
    }), 200


@app.route('/api/reset', methods=['POST'])
def reset_system():
    """Reseta o sistema (para testes)."""
    global hospital_service
    hospital_service = HospitalService()
    return jsonify({'success': True, 'message': 'Sistema resetado'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
