// Sistema de Gestão Hospitalar - Frontend

// API Base URL
const API_BASE = '/api';

// Funções auxiliares
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: 'Erro de conexão com a API' };
    }
}

// Cadastro de Paciente
document.getElementById('patient-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('patient-name').value;
    const priority = parseInt(document.getElementById('patient-priority').value);
    
    const result = await apiCall('/patients', 'POST', { name, priority });
    
    if (result.success) {
        alert(`Paciente cadastrado com sucesso! ID: ${result.patient.id}`);
        document.getElementById('patient-form').reset();
        updateAllViews();
    } else {
        alert(`Erro: ${result.error}`);
    }
});

// Cadastro de Médico
document.getElementById('doctor-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('doctor-name').value;
    
    const result = await apiCall('/doctors', 'POST', { name });
    
    if (result.success) {
        alert(`Médico cadastrado com sucesso! ID: ${result.doctor.id}`);
        document.getElementById('doctor-form').reset();
        updateAllViews();
    } else {
        alert(`Erro: ${result.error}`);
    }
});

// Buscar Paciente por ID
async function searchPatient() {
    const patientId = parseInt(document.getElementById('search-id').value);
    
    if (!patientId) {
        alert('Digite um ID válido');
        return;
    }
    
    const result = await apiCall(`/patients/${patientId}`);
    
    if (result.success) {
        const patient = result.patient;
        document.getElementById('search-result').innerHTML = `
            <div class="list-item">
                <div>
                    <strong>ID:</strong> ${patient.id}<br>
                    <strong>Nome:</strong> ${patient.name}<br>
                    <strong>Prioridade:</strong> ${patient.priority}<br>
                    <strong>Status:</strong> ${patient.status}
                </div>
            </div>
        `;
    } else {
        document.getElementById('search-result').innerHTML = `
            <div style="color: #dc3545;">Paciente não encontrado</div>
        `;
    }
}

// Reclassificar Paciente
async function reclassifyPatient() {
    const patientId = parseInt(document.getElementById('reclassify-id').value);
    const newPriority = parseInt(document.getElementById('reclassify-priority').value);
    
    if (!patientId) {
        alert('Digite um ID válido');
        return;
    }
    
    const result = await apiCall(`/patients/${patientId}/reclassify`, 'PUT', { priority: newPriority });
    
    if (result.success) {
        alert(`Paciente reclassificado para prioridade ${newPriority}`);
        updateAllViews();
    } else {
        alert(`Erro: ${result.error}`);
    }
}

// Cancelar Paciente
async function cancelPatient() {
    const patientId = parseInt(document.getElementById('cancel-id').value);
    
    if (!patientId) {
        alert('Digite um ID válido');
        return;
    }
    
    if (!confirm('Tem certeza que deseja cancelar este paciente?')) {
        return;
    }
    
    const result = await apiCall(`/patients/${patientId}/cancel`, 'DELETE');
    
    if (result.success) {
        alert('Paciente cancelado com sucesso');
        updateAllViews();
    } else {
        alert(`Erro: ${result.error}`);
    }
}

// Chamar Próximo Paciente
async function callNextPatient() {
    const result = await apiCall('/attendance/call', 'POST');
    
    if (result.success) {
        const patient = result.patient;
        const doctor = result.doctor;
        
        document.getElementById('attendance-info').innerHTML = `
            <div class="attendance-info">
                <h3>Atendimento Iniciado</h3>
                <p><strong>Paciente:</strong> ${patient.name} (ID: ${patient.id})</p>
                <p><strong>Médico:</strong> ${doctor.name} (ID: ${doctor.id})</p>
                <p><strong>Prioridade:</strong> ${patient.priority}</p>
            </div>
        `;
        
        document.getElementById('conclude-id').value = patient.id;
        updateAllViews();
    } else {
        alert(`Erro: ${result.error}`);
    }
}

// Concluir Atendimento
async function concludeAttendance() {
    const patientId = parseInt(document.getElementById('conclude-id').value);
    
    if (!patientId) {
        alert('Digite um ID válido');
        return;
    }
    
    const result = await apiCall('/attendance/conclude', 'POST', { patient_id: patientId });
    
    if (result.success) {
        alert('Atendimento concluído com sucesso');
        document.getElementById('attendance-info').innerHTML = '';
        document.getElementById('conclude-id').value = '';
        updateAllViews();
    } else {
        alert(`Erro: ${result.error}`);
    }
}

// Validar Sistema
async function validateSystem() {
    const result = await apiCall('/validate');
    
    if (result.success) {
        const validation = result.validation;
        
        let html = '<h3>Resultado da Validação</h3>';
        html += `<p>Hash: ${validation.hash_valid ? '✓' : '✗'}</p>`;
        html += `<p>Árvore Rubro-Negra: ${validation.tree_valid ? '✓' : '✗'}</p>`;
        html += `<p>Heap de Pacientes: ${validation.patient_heap_valid ? '✓' : '✗'}</p>`;
        html += `<p>Heap de Médicos: ${validation.doctor_heap_valid ? '✓' : '✗'}</p>`;
        html += `<p>Consistência de IDs: ${validation.consistent_ids ? '✓' : '✗'}</p>`;
        html += `<p class="${validation.all_valid ? 'validation-success' : 'validation-error'}">
            <strong>Status Geral: ${validation.all_valid ? 'VÁLIDO' : 'INVÁLIDO'}</strong>
        </p>`;
        
        document.getElementById('validation-result').innerHTML = html;
    }
}

// Teste de Colisão
async function testCollision() {
    const result = await apiCall('/test/collision', 'POST');
    
    if (result.success) {
        alert('Teste de colisão executado! Verifique a visualização da Hash.');
        updateAllViews();
    } else {
        alert(`Erro: ${result.error}`);
    }
}

// Resetar Sistema
async function resetSystem() {
    if (!confirm('Tem certeza que deseja resetar todo o sistema?')) {
        return;
    }
    
    const result = await apiCall('/reset', 'POST');
    
    if (result.success) {
        alert('Sistema resetado com sucesso');
        updateAllViews();
    }
}

// Atualizar todas as visualizações
async function updateAllViews() {
    await updateStats();
    await updateHashBuckets();
    await updateTreeVisualization();
    await updatePatientHeap();
    await updateDoctorHeap();
    await updatePriorityQueue();
    await updateArrivalList();
    await updateDoctorsList();
}

// Atualizar estatísticas
async function updateStats() {
    const result = await apiCall('/stats');
    
    if (result.success) {
        const stats = result.stats;
        
        document.getElementById('hash-size').textContent = `Tamanho: ${stats.hash_stats.size}`;
        document.getElementById('hash-capacity').textContent = `Capacidade: ${stats.hash_stats.capacity}`;
        document.getElementById('hash-load-factor').textContent = `Fator de Carga: ${stats.hash_stats.load_factor.toFixed(2)}`;
        
        document.getElementById('tree-size').textContent = `Tamanho: ${stats.tree_stats.size}`;
        document.getElementById('tree-height').textContent = `Altura Negra: ${stats.tree_stats.black_height}`;
        
        document.getElementById('patient-heap-size').textContent = `Tamanho: ${stats.patient_heap_stats.size}`;
        document.getElementById('doctor-heap-size').textContent = `Tamanho: ${stats.doctor_heap_stats.size}`;
    }
}

// Atualizar visualização da Hash
async function updateHashBuckets() {
    const result = await apiCall('/detailed-info');
    
    if (result.success) {
        const buckets = result.info.hash_buckets;
        
        let html = '';
        buckets.forEach(bucket => {
            if (bucket.chain.length > 0) {
                html += `<div class="bucket">
                    <div class="bucket-header">Bucket ${bucket.index}</div>`;
                bucket.chain.forEach(item => {
                    html += `<div class="chain-item">ID: ${item.key} - ${item.value.name}</div>`;
                });
                html += '</div>';
            }
        });
        
        document.getElementById('hash-buckets').innerHTML = html || '<p>Nenhum item na Hash</p>';
    }
}

// Atualizar visualização da Árvore
async function updateTreeVisualization() {
    const result = await apiCall('/detailed-info');
    
    if (result.success) {
        const treeInfo = result.info.tree_info;
        
        let html = '';
        
        function renderNode(node, depth = 0) {
            if (!node) return '';
            const colorClass = node.color === 'RED' ? 'red' : 'black';
            return `<div class="tree-node ${colorClass}" style="margin-left: ${depth * 20}px">
                ID: ${node.value.id} - ${node.value.name}
            </div>
            ${renderNode(node.left, depth + 1)}
            ${renderNode(node.right, depth + 1)}`;
        }
        
        if (treeInfo.root) {
            html = renderNode(treeInfo.root);
        }
        
        document.getElementById('tree-visualization').innerHTML = html || '<p>Árvore vazia</p>';
    }
}

// Atualizar Heap de Pacientes
async function updatePatientHeap() {
    const result = await apiCall('/detailed-info');
    
    if (result.success) {
        const heap = result.info.patient_heap;
        
        let html = '';
        heap.items.forEach((item, index) => {
            html += `<div class="heap-item priority-${item.priority}">
                <strong>[${index}]</strong> ID: ${item.key} - ${item.value.name} (P: ${item.priority})
            </div>`;
        });
        
        document.getElementById('patient-heap').innerHTML = html || '<p>Heap vazio</p>';
    }
}

// Atualizar Heap de Médicos
async function updateDoctorHeap() {
    const result = await apiCall('/detailed-info');
    
    if (result.success) {
        const heap = result.info.doctor_heap;
        
        let html = '';
        heap.items.forEach((item, index) => {
            html += `<div class="heap-item">
                <strong>[${index}]</strong> ID: ${item.key} - ${item.value.name} (Atendimentos: ${item.priority})
            </div>`;
        });
        
        document.getElementById('doctor-heap').innerHTML = html || '<p>Heap vazio</p>';
    }
}

// Atualizar Fila por Prioridade
async function updatePriorityQueue() {
    const result = await apiCall('/patients/queue');
    
    if (result.success) {
        const queue = result.queue;
        
        let html = '';
        queue.forEach(([priority, id, patient]) => {
            html += `<div class="list-item priority-${priority}">
                <div>
                    <strong>ID:</strong> ${id}<br>
                    <strong>Nome:</strong> ${patient.name}
                </div>
                <span class="priority-badge p${priority}">P${priority}</span>
            </div>`;
        });
        
        document.getElementById('priority-queue').innerHTML = html || '<p>Fila vazia</p>';
    }
}

// Atualizar Lista por Chegada
async function updateArrivalList() {
    const result = await apiCall('/patients/arrival');
    
    if (result.success) {
        const patients = result.patients;
        
        let html = '';
        patients.forEach(patient => {
            html += `<div class="list-item priority-${patient.priority}">
                <div>
                    <strong>ID:</strong> ${patient.id}<br>
                    <strong>Nome:</strong> ${patient.name}<br>
                    <strong>Chegada:</strong> ${patient.arrival_order}
                </div>
                <span class="priority-badge p${patient.priority}">P${patient.priority}</span>
            </div>`;
        });
        
        document.getElementById('arrival-list').innerHTML = html || '<p>Nenhum paciente</p>';
    }
}

// Atualizar Lista de Médicos
async function updateDoctorsList() {
    const result = await apiCall('/doctors/available');
    
    if (result.success) {
        const doctors = result.doctors;
        
        let html = '';
        doctors.forEach(([count, id, doctor]) => {
            html += `<div class="list-item">
                <div>
                    <strong>ID:</strong> ${id}<br>
                    <strong>Nome:</strong> ${doctor.name}
                </div>
                <span>Atendimentos: ${count}</span>
            </div>`;
        });
        
        document.getElementById('doctors-list').innerHTML = html || '<p>Nenhum médico disponível</p>';
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    updateAllViews();
});
