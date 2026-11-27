/**
 * SIGAE - Controle do Frontend
 */

const API_BASE = '/api';

// Toast Notifications
class ToastManager {
    constructor() {
        this.container = document.getElementById('toast-container');
    }

    show(type, title, message, duration = 4000) {
        if (!this.container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || '•'}</span>
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
        `;

        this.container.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'toastSlideIn 0.3s ease-out reverse forwards';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    success(title, message) { this.show('success', title, message); }
    error(title, message) { this.show('error', title, message, 6000); }
    warning(title, message) { this.show('warning', title, message); }
    info(title, message) { this.show('info', title, message); }
}

const toast = new ToastManager();

// API Helper
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
        let result = {};
        try {
            result = await response.json();
        } catch (jsonErr) {
            result = { error: 'Resposta inválida do servidor' };
        }

        if (!response.ok) {
            return { success: false, error: result.error || `Erro ${response.status}: Falha na operação` };
        }

        return result;
    } catch (error) {
        console.error(`Erro na chamada API [${endpoint}]:`, error);
        return { success: false, error: error.message || 'Erro de conexão com o servidor' };
    }
}

// Tab & Subtab Navigation
function switchTab(tabId) {
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabId);
    });

    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.toggle('active', pane.id === tabId);
    });

    // Atualização sob demanda para telas ativas
    if (tabId === 'tab-doctors') {
        refreshDoctorsRoster();
    } else if (tabId === 'tab-patient-search') {
        const searchInput = document.getElementById('unified-patient-search');
        if (searchInput && searchInput.value.trim().length > 0) {
            executePatientSearch();
        }
    }
}

function switchSubtab(subtabId) {
    document.querySelectorAll('.subtab-btn').forEach(btn => {
        const isTarget = btn.dataset.subtab === subtabId || 
                         (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(subtabId));
        btn.classList.toggle('active', !!isTarget);
    });

    document.querySelectorAll('.subtab-content').forEach(content => {
        content.classList.toggle('active', content.id === subtabId);
    });
}

// Modal Support
function openModal(title, bodyHtml) {
    const container = document.getElementById('modal-container');
    const titleEl = document.getElementById('modal-title');
    const bodyEl = document.getElementById('modal-body');

    if (container && titleEl && bodyEl) {
        titleEl.textContent = title;
        bodyEl.innerHTML = bodyHtml;
        container.classList.remove('hidden');
    }
}

function closeModal() {
    const container = document.getElementById('modal-container');
    if (container) {
        container.classList.add('hidden');
    }
}

// Prioridade Manchester Formatters
function getPriorityInfo(priority) {
    const map = {
        1: { label: 'P1 • Emergência', class: 'p-1', desc: 'Atendimento Imediato (0 min)' },
        2: { label: 'P2 • Muito Urgente', class: 'p-2', desc: 'Até 10 min' },
        3: { label: 'P3 • Urgente', class: 'p-3', desc: 'Até 60 min' },
        4: { label: 'P4 • Pouco Urgente', class: 'p-4', desc: 'Até 120 min' },
        5: { label: 'P5 • Não Urgente', class: 'p-5', desc: 'Até 240 min' },
    };
    return map[priority] || { label: `P${priority}`, class: 'p-5', desc: '' };
}

function getStatusBadge(status) {
    const map = {
        'waiting': '<span class="status-chip waiting">⏳ Aguardando</span>',
        'in_attendance': '<span class="status-chip in_attendance">🩺 Em Atendimento</span>',
        'completed': '<span class="status-chip completed">✓ Concluído</span>'
    };
    return map[status] || `<span class="status-chip">${status}</span>`;
}

// Cadastro de Paciente & Médico
document.addEventListener('DOMContentLoaded', () => {
    // Form Paciente
    const patientForm = document.getElementById('patient-form');
    if (patientForm) {
        patientForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const nameInput = document.getElementById('patient-name');
            const priorityInput = document.getElementById('patient-priority');

            const name = nameInput.value.trim();
            const priority = parseInt(priorityInput.value);

            if (!name) {
                toast.warning('Atenção', 'Informe o nome do paciente');
                return;
            }

            const btn = document.getElementById('btn-register-patient');
            if (btn) btn.disabled = true;

            const res = await apiCall('/patients', 'POST', { name, priority });
            if (btn) btn.disabled = false;

            if (res.success) {
                toast.success('Paciente Cadastrado!', `${res.patient.name} cadastrado com ID #${res.patient.id} (Prioridade ${priority})`);
                nameInput.value = '';
                updateAllViews();
            } else {
                toast.error('Erro no Cadastro', res.error);
            }
        });
    }

    // Form Médico
    const doctorForm = document.getElementById('doctor-form');
    if (doctorForm) {
        doctorForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const nameInput = document.getElementById('doctor-name');
            const name = nameInput.value.trim();

            if (!name) {
                toast.warning('Atenção', 'Informe o nome do médico');
                return;
            }

            const btn = document.getElementById('btn-register-doctor');
            if (btn) btn.disabled = true;

            const res = await apiCall('/doctors', 'POST', { name });
            if (btn) btn.disabled = false;

            if (res.success) {
                toast.success('Médico Inserido!', `Dr(a). ${res.doctor.name} registrado com ID #${res.doctor.id}`);
                nameInput.value = '';
                updateAllViews();
                refreshDoctorsRoster();
            } else {
                toast.error('Erro no Cadastro', res.error);
            }
        });
    }

    // Enter no campo de busca de paciente
    const searchInput = document.getElementById('unified-patient-search');
    if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                executePatientSearch();
            }
        });
    }

    // Enter no campo de busca de médico
    const doctorSearchInput = document.getElementById('doctor-search-input');
    if (doctorSearchInput) {
        doctorSearchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                checkSpecificDoctor();
            }
        });
    }

    // Carregamento inicial completo
    updateAllViews();
    refreshDoctorsRoster();
});

// Busca Unificada de Paciente (Por Nome ou ID)
async function executePatientSearch() {
    const input = document.getElementById('unified-patient-search');
    const query = input ? input.value.trim() : '';

    if (!query) {
        toast.warning('Busca vazia', 'Digite o nome ou o ID numérico do paciente.');
        return;
    }

    const container = document.getElementById('patient-search-results');
    container.innerHTML = '<div class="empty-state-large"><span class="empty-icon-large">⏳</span><p>Consultando Tabela Hash e registros...</p></div>';

    const res = await apiCall(`/patients/search?q=${encodeURIComponent(query)}`);

    if (res.success && res.patients && res.patients.length > 0) {
        renderPatientSearchResults(res.patients);
        toast.info('Busca Concluída', `${res.patients.length} paciente(s) localizado(s).`);
    } else {
        container.innerHTML = `
            <div class="empty-state-large">
                <span class="empty-icon-large">❌</span>
                <h3>Nenhum paciente encontrado</h3>
                <p>Nenhum prontuário correspondeu à busca: <strong>"${query}"</strong>.</p>
                <button onclick="listAllPatients()" class="btn btn-secondary btn-sm" style="margin-top: 14px;">Listar Todos os Cadastrados</button>
            </div>
        `;
        document.getElementById('search-count-label').textContent = '0 encontrados';
    }
}

function clearPatientSearch() {
    const input = document.getElementById('unified-patient-search');
    if (input) input.value = '';
    const container = document.getElementById('patient-search-results');
    if (container) {
        container.innerHTML = `
            <div class="empty-state-large">
                <span class="empty-icon-large">🔎</span>
                <h3>Pronto para buscar</h3>
                <p>Digite o nome ou ID acima para localizar pacientes.</p>
            </div>
        `;
    }
    document.getElementById('search-count-label').textContent = '0 pacientes listados';
}

async function listAllPatients() {
    const container = document.getElementById('patient-search-results');
    container.innerHTML = '<div class="empty-state-large"><span class="empty-icon-large">⏳</span><p>Carregando pacientes da Árvore Rubro-Negra...</p></div>';

    const res = await apiCall('/patients/arrival');

    if (res.success && res.patients && res.patients.length > 0) {
        renderPatientSearchResults(res.patients);
    } else {
        container.innerHTML = `
            <div class="empty-state-large">
                <span class="empty-icon-large">📂</span>
                <h3>Nenhum paciente registrado</h3>
                <p>Cadastre pacientes na aba "Triagem & Atendimento" para vê-los aqui.</p>
            </div>
        `;
        document.getElementById('search-count-label').textContent = '0 pacientes';
    }
}

function renderPatientSearchResults(patients) {
    const container = document.getElementById('patient-search-results');
    document.getElementById('search-count-label').textContent = `${patients.length} paciente(s) exibido(s)`;

    let html = `
        <table class="custom-table">
            <thead>
                <tr>
                    <th>ID Hash</th>
                    <th>Nome do Paciente</th>
                    <th>Classificação de Risco</th>
                    <th>Ordem Chegada</th>
                    <th>Status</th>
                    <th>Ações Rápidas</th>
                </tr>
            </thead>
            <tbody>
    `;

    patients.forEach(p => {
        const pInfo = getPriorityInfo(p.priority);
        const statusBadge = getStatusBadge(p.status || 'waiting');

        html += `
            <tr>
                <td><span class="table-id-badge">#${p.id}</span></td>
                <td><strong style="color: #FFFFFF; font-size: 0.95rem;">${p.name}</strong></td>
                <td><span class="priority-pill ${pInfo.class}">${pInfo.label}</span></td>
                <td style="font-family: var(--font-mono); color: var(--text-muted);">${p.arrival_order !== undefined ? p.arrival_order : '-'}</td>
                <td>${statusBadge}</td>
                <td>
                    <div class="table-actions">
                        <button onclick="quickPrepareReclassify(${p.id}, ${p.priority})" class="btn btn-warning btn-sm" title="Reclassificar Prioridade">
                            <span>✏️ Prioridade</span>
                        </button>
                        <button onclick="quickCancelPatient(${p.id})" class="btn btn-danger btn-sm" title="Cancelar Paciente">
                            <span>✕ Cancelar</span>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;
}

function quickPrepareReclassify(patientId, currentPriority) {
    switchTab('tab-operations');
    const input = document.getElementById('reclassify-id');
    const select = document.getElementById('reclassify-priority');
    if (input) input.value = patientId;
    if (select) select.value = currentPriority;
    input.focus();
    toast.info('Reclassificação', `Paciente #${patientId} selecionado para reclassificação.`);
}

async function quickCancelPatient(patientId) {
    if (confirm(`Deseja realmente cancelar o paciente ID #${patientId}? Ele será removido da Hash, Árvore e Heap.`)) {
        const res = await apiCall(`/patients/${patientId}/cancel`, 'DELETE');
        if (res.success) {
            toast.success('Cancelado', `Paciente #${patientId} removido com sucesso.`);
            updateAllViews();
            // Atualiza busca se estiver na tela
            executePatientSearch();
        } else {
            toast.error('Erro ao Cancelar', res.error);
        }
    }
}

// Verificação de Disponibilidade de Médico Específico
async function checkSpecificDoctor(identifier = null) {
    let query = identifier;
    if (!query) {
        const input = document.getElementById('doctor-search-input');
        query = input ? input.value.trim() : '';
    }

    if (!query) {
        toast.warning('Atenção', 'Informe o nome ou ID do médico para consultar disponibilidade.');
        return;
    }

    const banner = document.getElementById('doctor-status-card');
    banner.classList.remove('hidden');
    banner.className = 'doctor-status-banner';
    banner.innerHTML = '<span class="empty-icon">⏳</span><span>Verificando escala e status no Min-Heap...</span>';

    const res = await apiCall(`/doctors/check?query=${encodeURIComponent(query)}`);

    if (res.success) {
        const doc = res.doctor;
        const isAvailable = res.is_available;
        const currentPatient = res.current_patient;

        banner.className = `doctor-status-banner ${isAvailable ? 'is-available' : 'is-busy'}`;

        banner.innerHTML = `
            <div class="doctor-banner-details">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <h3>Dr(a). ${doc.name}</h3>
                    <span class="table-id-badge">ID #${doc.id}</span>
                </div>
                <div class="doctor-banner-meta">
                    Atendimentos Concluídos: <strong>${doc.completed_count || 0}</strong> • Ordem de Cadastro: <strong>${doc.registration_order || doc.id}</strong>
                </div>
                ${!isAvailable && currentPatient ? `
                    <div style="margin-top: 10px; font-size: 0.88rem; background: rgba(0,0,0,0.3); padding: 8px 14px; border-radius: 8px; border-left: 3px solid #EF4444;">
                        Atendendo Agora: <strong>${currentPatient.name}</strong> (ID #${currentPatient.id} • Prioridade ${currentPatient.priority})
                    </div>
                ` : ''}
            </div>
            <div>
                <span class="doctor-badge-status ${isAvailable ? 'available' : 'busy'}">
                    ${isAvailable ? '🟢 DISPONÍVEL NO HEAP' : '🔴 EM ATENDIMENTO'}
                </span>
            </div>
        `;
        toast.info('Status Atualizado', `Dr(a). ${doc.name} está ${isAvailable ? 'Disponível' : 'Ocupado(a)'}.`);
    } else {
        banner.className = 'doctor-status-banner is-busy';
        banner.innerHTML = `
            <div class="doctor-banner-details">
                <h3>Médico Não Localizado</h3>
                <p class="doctor-banner-meta">${res.error || 'Nenhum médico encontrado com esse nome ou ID.'}</p>
            </div>
        `;
        toast.error('Não Encontrado', res.error);
    }
}

async function refreshDoctorsRoster() {
    const grid = document.getElementById('doctors-roster-grid');
    const countLabel = document.getElementById('doctors-roster-count');

    const res = await apiCall('/doctors');

    if (res.success && res.doctors && res.doctors.length > 0) {
        countLabel.textContent = `${res.doctors.length} médicos na escala`;
        let html = '';

        res.doctors.forEach(doc => {
            const isAvailable = doc.status === 'available';
            html += `
                <div class="doctor-card ${isAvailable ? 'available' : 'busy'}">
                    <div class="doctor-card-top">
                        <div>
                            <div class="doctor-name-display">Dr(a). ${doc.name}</div>
                            <span class="table-id-badge" style="font-size: 0.72rem;">ID #${doc.id}</span>
                        </div>
                        <span class="status-chip ${isAvailable ? 'completed' : 'in_attendance'}">
                            ${isAvailable ? '● Disponível' : '● Ocupado'}
                        </span>
                    </div>

                    ${!isAvailable && doc.current_patient ? `
                        <div style="font-size: 0.78rem; background: rgba(0,0,0,0.2); padding: 6px 10px; border-radius: 6px; color: #F87171;">
                            Atendendo: <strong>${doc.current_patient.name}</strong> (#${doc.current_patient.id})
                        </div>
                    ` : ''}

                    <div class="doctor-stats-row">
                        <span>Atendimentos: <strong>${doc.completed_count || 0}</strong></span>
                        <button onclick="checkSpecificDoctor('${doc.name}')" class="btn btn-outline btn-sm" style="padding: 2px 8px; font-size: 0.72rem;">
                            Verificar Status
                        </button>
                    </div>
                </div>
            `;
        });
        grid.innerHTML = html;
    } else {
        countLabel.textContent = '0 médicos cadastrados';
        grid.innerHTML = `
            <div class="empty-state-large" style="grid-column: 1 / -1;">
                <span class="empty-icon-large">👨‍⚕️</span>
                <h3>Nenhum médico cadastrado</h3>
                <p>Cadastre médicos no formulário acima para compor a equipe.</p>
            </div>
        `;
    }
}

// Central de Atendimento (Chamar / Concluir)
async function callNextPatient() {
    const btn = document.getElementById('btn-call');
    if (btn) btn.disabled = true;

    const res = await apiCall('/attendance/call', 'POST');
    if (btn) btn.disabled = false;

    if (res.success) {
        const p = res.patient;
        const d = res.doctor;
        const pInfo = getPriorityInfo(p.priority);

        const container = document.getElementById('attendance-info');
        container.className = 'attendance-display active-attendance';
        container.innerHTML = `
            <div class="attendance-header-line">
                <span class="attendance-headline">
                    <span class="status-dot pulse"></span> Consulta Iniciada em Consultório
                </span>
                <span class="priority-pill ${pInfo.class}">${pInfo.label}</span>
            </div>
            <div class="attendance-participants">
                <div class="attendance-role-card">
                    <div class="attendance-role-title">Paciente Atendido</div>
                    <div class="attendance-role-name">${p.name}</div>
                    <div class="attendance-role-meta">Prontuário #${p.id}</div>
                </div>
                <div class="attendance-role-card">
                    <div class="attendance-role-title">Médico Responsável</div>
                    <div class="attendance-role-name">Dr(a). ${d.name}</div>
                    <div class="attendance-role-meta">CRM / ID #${d.id} • Atendimentos: ${d.completed_count || 0}</div>
                </div>
            </div>
        `;

        const concludeInput = document.getElementById('conclude-id');
        if (concludeInput) concludeInput.value = p.id;

        toast.success('Paciente Chamado!', `${p.name} encaminhado(a) para Dr(a). ${d.name}.`);
        updateAllViews();
        refreshDoctorsRoster();
    } else {
        toast.error('Não Foi Possível Chamar', res.error);
    }
}

async function concludeAttendance() {
    const input = document.getElementById('conclude-id');
    const patientId = parseInt(input.value);

    if (!patientId || patientId <= 0) {
        toast.warning('Atenção', 'Informe o ID do paciente para concluir a consulta.');
        return;
    }

    const btn = document.getElementById('btn-conclude');
    if (btn) btn.disabled = true;

    const res = await apiCall('/attendance/conclude', 'POST', { patient_id: patientId });
    if (btn) btn.disabled = false;

    if (res.success) {
        toast.success('Atendimento Concluído', `Consulta finalizada com sucesso. Médico liberado para novos atendimentos.`);
        const container = document.getElementById('attendance-info');
        container.className = 'attendance-display empty';
        container.innerHTML = `
            <div class="empty-state-micro">
                <span class="empty-icon">✓</span>
                <span>Último atendimento (#${patientId}) concluído com sucesso.</span>
            </div>
        `;
        input.value = '';
        updateAllViews();
        refreshDoctorsRoster();
    } else {
        toast.error('Erro na Conclusão', res.error);
    }
}

// Reclassificação & Cancelamento
async function reclassifyPatient() {
    const inputId = document.getElementById('reclassify-id');
    const selectPriority = document.getElementById('reclassify-priority');

    const patientId = parseInt(inputId.value);
    const newPriority = parseInt(selectPriority.value);

    if (!patientId || patientId <= 0) {
        toast.warning('Atenção', 'Informe um ID válido de paciente.');
        return;
    }

    const res = await apiCall(`/patients/${patientId}/reclassify`, 'PUT', { priority: newPriority });

    if (res.success) {
        toast.success('Prioridade Atualizada', `Paciente #${patientId} reclassificado para Prioridade ${newPriority} no Min-Heap.`);
        inputId.value = '';
        updateAllViews();
    } else {
        toast.error('Erro ao Reclassificar', res.error);
    }
}

async function cancelPatient() {
    const inputId = document.getElementById('cancel-id');
    const patientId = parseInt(inputId.value);

    if (!patientId || patientId <= 0) {
        toast.warning('Atenção', 'Informe um ID válido de paciente.');
        return;
    }

    if (!confirm(`Confirmar cancelamento do paciente ID #${patientId}?`)) return;

    const res = await apiCall(`/patients/${patientId}/cancel`, 'DELETE');

    if (res.success) {
        toast.success('Paciente Cancelado', `Paciente #${patientId} removido de todas as estruturas.`);
        inputId.value = '';
        updateAllViews();
    } else {
        toast.error('Erro ao Cancelar', res.error);
    }
}

// Atualização de Visualizações & Estruturas de Dados
async function updateAllViews() {
    await Promise.all([
        updateStats(),
        updatePriorityQueue(),
        updateArrivalList(),
        updateDataStructures()
    ]);
}

// Estatísticas Globais
async function updateStats() {
    const res = await apiCall('/stats');
    if (res.success) {
        const stats = res.stats;

        // Header Metrics
        document.getElementById('header-patient-count').textContent = stats.hash_stats.size;
        document.getElementById('header-queue-count').textContent = stats.patient_heap_stats.size;
        document.getElementById('header-attendance-count').textContent = stats.active_attendances;
        document.getElementById('header-doctor-count').textContent = stats.doctor_heap_stats.size;

        // Structure Tab Metrics
        document.getElementById('hash-size').textContent = stats.hash_stats.size;
        document.getElementById('hash-capacity').textContent = stats.hash_stats.capacity;
        document.getElementById('hash-load-factor').textContent = stats.hash_stats.load_factor.toFixed(2);

        document.getElementById('tree-size').textContent = stats.tree_stats.size;
        document.getElementById('tree-height').textContent = stats.tree_stats.black_height;

        document.getElementById('patient-heap-size').textContent = stats.patient_heap_stats.size;
        document.getElementById('doctor-heap-size').textContent = stats.doctor_heap_stats.size;
    }
}

// Fila por Prioridade (Min-Heap)
async function updatePriorityQueue() {
    const container = document.getElementById('priority-queue');
    const badge = document.getElementById('badge-heap-count');

    const res = await apiCall('/patients/queue');
    if (res.success && res.queue) {
        badge.textContent = `${res.queue.length} aguardando`;

        if (res.queue.length === 0) {
            container.innerHTML = '<div class="empty-state-large"><span class="empty-icon-large">✓</span><p>Fila de triagem vazia. Nenhum paciente aguardando.</p></div>';
            return;
        }

        let html = '';
        res.queue.forEach(([priority, id, patient], idx) => {
            const pInfo = getPriorityInfo(priority);
            html += `
                <div class="stream-card ${pInfo.class}">
                    <div class="stream-card-info">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-family: var(--font-mono); font-size: 0.76rem; color: var(--text-muted);">#${idx + 1}</span>
                            <span class="stream-card-name">${patient.name}</span>
                            <span class="table-id-badge">ID #${id}</span>
                        </div>
                        <div class="stream-card-meta">
                            Chegada: ordem ${patient.arrival_order !== undefined ? patient.arrival_order : '-'} • ${pInfo.desc}
                        </div>
                    </div>
                    <div>
                        <span class="priority-pill ${pInfo.class}">${pInfo.label}</span>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    }
}

// Ordem de Chegada (Árvore Rubro-Negra)
async function updateArrivalList() {
    const container = document.getElementById('arrival-list');
    const badge = document.getElementById('badge-tree-count');

    const res = await apiCall('/patients/arrival');
    if (res.success && res.patients) {
        badge.textContent = `${res.patients.length} pacientes`;

        if (res.patients.length === 0) {
            container.innerHTML = '<div class="empty-state-large"><span class="empty-icon-large">🕐</span><p>Nenhum paciente aguardando ou em triagem.</p></div>';
            return;
        }

        let html = '';
        res.patients.forEach(p => {
            const pInfo = getPriorityInfo(p.priority);
            html += `
                <div class="stream-card ${pInfo.class}">
                    <div class="stream-card-info">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span class="stream-card-name">${p.name}</span>
                            <span class="table-id-badge">ID #${p.id}</span>
                        </div>
                        <div class="stream-card-meta">
                            Timestamp de Chegada: <strong>${p.arrival_order !== undefined ? p.arrival_order : p.arrival_time}</strong>
                        </div>
                    </div>
                    <div>
                        <span class="priority-pill ${pInfo.class}">P${p.priority}</span>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    }
}

// Estruturas de Dados Detalhadas
async function updateDataStructures() {
    const res = await apiCall('/detailed-info');
    if (!res.success || !res.info) return;

    const info = res.info;

    // 1. Tabela Hash
    const hashContainer = document.getElementById('hash-buckets');
    if (hashContainer && info.hash_buckets) {
        let html = '';
        info.hash_buckets.forEach(b => {
            const hasCollision = b.chain.length > 1;
            html += `
                <div class="bucket-card ${hasCollision ? 'has-collision' : ''}">
                    <div class="bucket-card-header">
                        <span>Bucket [${b.index}]</span>
                        <span>${b.chain.length} nó(s)</span>
                    </div>
                    <div class="bucket-chain">
                        ${b.chain.length === 0 ? '<span style="font-size: 0.72rem; color: var(--text-muted); font-style: italic;">vazio</span>' : ''}
                        ${b.chain.map(item => `
                            <div class="chain-node">
                                <span class="node-key">#${item.key}</span>
                                <span style="color: var(--text-primary); font-weight: 600;">${item.value.name}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        });
        hashContainer.innerHTML = html;
    }

    // 2. Árvore Rubro-Negra
    const treeContainer = document.getElementById('tree-visualization');
    if (treeContainer && info.tree_info) {
        function renderTreeNode(node) {
            if (!node) return '';
            const isRed = node.color === 'RED';
            const nodeClass = isRed ? 'node-red' : 'node-black';
            const patientId = node.value ? node.value.id : (Array.isArray(node.key) ? node.key[1] : node.key);
            const priority = (node.value && node.value.priority !== undefined) ? node.value.priority : '-';
            const name = (node.value && node.value.name) ? node.value.name : '';
            const arrival = (node.value && node.value.arrival_order !== undefined) ? node.value.arrival_order : '-';

            return `
                <div class="tree-branch">
                    <div class="tree-node-visual ${nodeClass}" title="ID: ${patientId} • ${name} • Chegada: ${arrival}">
                        <span>#${patientId}</span>
                        <span style="font-size: 0.65rem; opacity: 0.9;">P${priority}</span>
                    </div>
                    ${(node.left || node.right) ? `
                        <div class="tree-subchildren">
                            ${renderTreeNode(node.left)}
                            ${renderTreeNode(node.right)}
                        </div>
                    ` : ''}
                </div>
            `;
        }

        if (info.tree_info.root) {
            treeContainer.innerHTML = `<div class="tree-wrapper">${renderTreeNode(info.tree_info.root)}</div>`;
        } else {
            treeContainer.innerHTML = '<div class="empty-state-large"><span class="empty-icon-large">🌳</span><p>Árvore Rubro-Negra vazia.</p></div>';
        }
    }

    // 3. Min-Heap de Pacientes
    const pHeapContainer = document.getElementById('patient-heap');
    if (pHeapContainer && info.patient_heap) {
        if (info.patient_heap.items.length === 0) {
            pHeapContainer.innerHTML = '<div class="empty-state-large" style="grid-column: 1 / -1;"><span class="empty-icon-large">📋</span><p>Heap de pacientes vazio.</p></div>';
        } else {
            let html = '';
            info.patient_heap.items.forEach((item, idx) => {
                const isRoot = idx === 0;
                const pInfo = getPriorityInfo(item.priority);
                html += `
                    <div class="heap-cell ${isRoot ? 'root-cell' : ''}">
                        <div class="heap-cell-header">
                            <span>Índice [${idx}] ${isRoot ? '★ RAIZ' : ''}</span>
                            <span>ID #${item.key}</span>
                        </div>
                        <div class="heap-cell-key">${item.value.name}</div>
                        <div class="heap-cell-priority">
                            Prioridade: <span class="priority-pill ${pInfo.class}" style="padding: 1px 6px; font-size: 0.68rem;">P${item.priority}</span>
                        </div>
                    </div>
                `;
            });
            pHeapContainer.innerHTML = html;
        }
    }

    // 4. Min-Heap de Médicos
    const dHeapContainer = document.getElementById('doctor-heap');
    if (dHeapContainer && info.doctor_heap) {
        if (info.doctor_heap.items.length === 0) {
            dHeapContainer.innerHTML = '<div class="empty-state-large" style="grid-column: 1 / -1;"><span class="empty-icon-large">👨‍⚕️</span><p>Nenhum médico disponível no heap.</p></div>';
        } else {
            let html = '';
            info.doctor_heap.items.forEach((item, idx) => {
                const isRoot = idx === 0;
                html += `
                    <div class="heap-cell ${isRoot ? 'root-cell' : ''}">
                        <div class="heap-cell-header">
                            <span>Índice [${idx}] ${isRoot ? '★ PRÓXIMO' : ''}</span>
                            <span>ID #${item.key}</span>
                        </div>
                        <div class="heap-cell-key">Dr(a). ${item.value.name}</div>
                        <div class="heap-cell-priority">
                            Atendimentos: <strong>${item.priority}</strong>
                        </div>
                    </div>
                `;
            });
            dHeapContainer.innerHTML = html;
        }
    }
}

// Testes e Diagnóstico
async function validateSystem() {
    const container = document.getElementById('validation-result');
    container.innerHTML = '<p>Executando bateria de validação nas 3 estruturas...</p>';

    const res = await apiCall('/validate');
    if (res.success && res.validation) {
        const v = res.validation;
        let html = `
            <div style="line-height: 1.8;">
                <div><strong>• Tabela Hash (Integridade & Encadeamento):</strong> ${v.hash_valid ? '✓ VÁLIDA' : '✗ INVÁLIDA'}</div>
                <div><strong>• Árvore Rubro-Negra (Propriedades e Altura Negra):</strong> ${v.tree_valid ? '✓ VÁLIDA' : '✗ INVÁLIDA'}</div>
                <div><strong>• Min-Heap de Pacientes (Propriedade de Heap):</strong> ${v.patient_heap_valid ? '✓ VÁLIDO' : '✗ INVÁLIDO'}</div>
                <div><strong>• Min-Heap de Médicos (Propriedade de Heap):</strong> ${v.doctor_heap_valid ? '✓ VÁLIDO' : '✗ INVÁLIDO'}</div>
                <div><strong>• Sincronia de IDs (Hash == Árvore == Heap):</strong> ${v.consistent_ids ? '✓ CONSISTENTES' : '✗ DIVERGENTES'}</div>
            </div>
            <div class="${v.all_valid ? 'validation-success-badge' : 'empty-state-large'}">
                ${v.all_valid ? '✓ STATUS GERAL: TODAS AS ESTRUTURAS ESTÃO ÍNTEGRAS E SINCRONIZADAS' : '⚠ ATENÇÃO: DIVERGÊNCIA DETECTADA'}
            </div>
        `;
        container.innerHTML = html;
        if (v.all_valid) toast.success('Validação Concluída', 'Sistema 100% consistente!');
        else toast.warning('Validação', 'Inconsistência encontrada.');
    }
}

async function testCollision() {
    const res = await apiCall('/test/collision', 'POST');
    if (res.success) {
        toast.info('Teste de Colisão', res.message);
        switchTab('tab-structures');
        switchSubtab('sub-hash');
        updateAllViews();
    } else {
        toast.error('Erro no Teste', res.error);
    }
}

async function confirmResetSystem() {
    if (!confirm('Deseja realmente resetar todas as estruturas de dados? Todos os cadastros serão limpos.')) return;

    const res = await apiCall('/reset', 'POST');
    if (res.success) {
        toast.success('Reset Concluído', 'Sistema redefinido com sucesso.');
        document.getElementById('validation-result').innerHTML = '';
        document.getElementById('attendance-info').className = 'attendance-display empty';
        document.getElementById('attendance-info').innerHTML = '<div class="empty-state-micro"><span class="empty-icon">🩺</span><span>Nenhum atendimento em curso.</span></div>';
        updateAllViews();
        refreshDoctorsRoster();
        clearPatientSearch();
    } else {
        toast.error('Erro no Reset', res.error);
    }
}
