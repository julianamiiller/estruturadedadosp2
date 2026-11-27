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
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type deve ser application/json'}), 400
    
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'Dados JSON inválidos'}), 400
    
    name = data.get('name')
    priority = data.get('priority')
    
    if not name or priority is None:
        return jsonify({'success': False, 'error': 'Nome e prioridade são obrigatórios'}), 400
    
    result = hospital_service.register_patient(name, priority)
    
    if result['success']:
        return jsonify(result), 201
    return jsonify(result), 400


@app.route('/api/patients/search', methods=['GET'])
def search_patients():
    """Busca pacientes por ID ou Nome."""
    query = request.args.get('q') or request.args.get('name')
    if not query:
        return jsonify({'success': False, 'error': 'Parâmetro de busca "q" ou "name" é obrigatório'}), 400
    
    results = hospital_service.search_patients(query)
    return jsonify({
        'success': True,
        'count': len(results),
        'patients': results
    }), 200


@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Busca um paciente por ID."""
    if patient_id <= 0:
        return jsonify({'success': False, 'error': 'ID inválido'}), 400
    
    patient = hospital_service.find_patient_by_id(patient_id)
    
    if patient:
        return jsonify({'success': True, 'patient': patient}), 200
    return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404


@app.route('/api/patients/<int:patient_id>/reclassify', methods=['PUT'])
def reclassify_patient(patient_id):
    """Reclassifica a prioridade de um paciente."""
    if patient_id <= 0:
        return jsonify({'success': False, 'error': 'ID inválido'}), 400
    
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type deve ser application/json'}), 400
    
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'Dados JSON inválidos'}), 400
    
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
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type deve ser application/json'}), 400
    
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'Dados JSON inválidos'}), 400
    
    name = data.get('name')
    
    if not name:
        return jsonify({'success': False, 'error': 'Nome é obrigatório'}), 400
    
    result = hospital_service.register_doctor(name)
    
    if result['success']:
        return jsonify(result), 201
    return jsonify(result), 400


@app.route('/api/doctors', methods=['GET'])
def list_all_doctors():
    """Retorna todos os médicos cadastrados com status de disponibilidade."""
    doctors = hospital_service.get_all_doctors()
    return jsonify({'success': True, 'doctors': doctors}), 200


@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    """Busca médico por ID e verifica status."""
    result = hospital_service.check_doctor_availability(doctor_id)
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 404


@app.route('/api/doctors/check', methods=['GET'])
def check_doctor_availability():
    """Verifica disponibilidade de um médico específico por nome ou ID."""
    query = request.args.get('query') or request.args.get('q') or request.args.get('name') or request.args.get('id')
    if not query:
        return jsonify({'success': False, 'error': 'Parâmetro "query", "name" ou "id" é obrigatório'}), 400
    
    result = hospital_service.check_doctor_availability(query)
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 404


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
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type deve ser application/json'}), 400
    
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'Dados JSON inválidos'}), 400
    
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
    # Garante que IDs 5, 15, 25 sejam limpos antes se já existirem
    for pid in [5, 15, 25]:
        if hospital_service.hash_table.contains(pid):
            hospital_service.cancel_patient(pid)
    
    # IDs 5, 15 e 25 colidem no mesmo bucket (ex: com capacidade 10, resto 5)
    hospital_service.next_patient_id = 5
    patient1 = hospital_service.register_patient('Colisão ID 5', 3)
    
    hospital_service.next_patient_id = 15
    patient2 = hospital_service.register_patient('Colisão ID 15', 3)
    
    hospital_service.next_patient_id = 25
    patient3 = hospital_service.register_patient('Colisão ID 25', 3)
    
    return jsonify({
        'success': True,
        'message': 'Criados pacientes com IDs 5, 15 e 25. Todos colidem no bucket 5 (capacidade 10)',
        'patients': [patient1.get('patient'), patient2.get('patient'), patient3.get('patient')],
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
