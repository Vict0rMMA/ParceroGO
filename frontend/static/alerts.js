var ALERT_OVERLAY_ID = 'custom-alert-overlay';
var ALERT_ICONS = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
var ALERT_TITLES = { success: '¡Éxito!', error: 'Error', warning: 'Advertencia', info: 'Información' };

function ensureAlertDOM() {
    if (document.getElementById(ALERT_OVERLAY_ID)) return;
    var overlay = document.createElement('div');
    overlay.id = ALERT_OVERLAY_ID;
    overlay.className = 'custom-alert-overlay';
    overlay.innerHTML =
        '<div class="custom-alert" id="custom-alert">' +
        '<div class="custom-alert-icon" id="custom-alert-icon">ℹ️</div>' +
        '<h3 class="custom-alert-title" id="custom-alert-title">Título</h3>' +
        '<p class="custom-alert-message" id="custom-alert-message">Mensaje</p>' +
        '<div class="custom-alert-buttons" id="custom-alert-buttons">' +
        '<button class="custom-alert-btn custom-alert-btn-primary" id="custom-alert-ok">Aceptar</button>' +
        '</div></div>';
    document.body.appendChild(overlay);
}

function getAlertElements() {
    return {
        overlay: document.getElementById(ALERT_OVERLAY_ID),
        alert: document.getElementById('custom-alert'),
        icon: document.getElementById('custom-alert-icon'),
        titleEl: document.getElementById('custom-alert-title'),
        messageEl: document.getElementById('custom-alert-message'),
        buttonsEl: document.getElementById('custom-alert-buttons')
    };
}

function closeAlert(callback) {
    var overlay = document.getElementById(ALERT_OVERLAY_ID);
    if (overlay) overlay.classList.remove('show');
    if (typeof callback === 'function') callback();
}

function showAlert(message, type, title, callback) {
    type = type || 'info';
    ensureAlertDOM();
    var el = getAlertElements();
    if (!el.overlay || !el.alert) return;

    el.alert.className = 'custom-alert ' + type;
    el.icon.textContent = ALERT_ICONS[type] || ALERT_ICONS.info;
    el.titleEl.textContent = title || ALERT_TITLES[type] || ALERT_TITLES.info;
    el.titleEl.style.display = 'block';
    el.messageEl.textContent = message;
    el.buttonsEl.innerHTML = '<button class="custom-alert-btn custom-alert-btn-primary" id="custom-alert-ok">Aceptar</button>';

    el.overlay.classList.add('show');

    document.getElementById('custom-alert-ok').onclick = function () {
        closeAlert(callback);
    };
    el.overlay.onclick = function (e) {
        if (e.target === el.overlay) closeAlert(callback);
    };
    var escHandler = function (e) {
        if (e.key === 'Escape') {
            closeAlert(callback);
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
}

function showConfirm(message, title, onConfirm, onCancel) {
    title = title || 'Confirmar';
    ensureAlertDOM();
    var el = getAlertElements();
    if (!el.overlay || !el.alert) return;

    el.alert.className = 'custom-alert warning';
    el.icon.textContent = '⚠️';
    el.titleEl.textContent = title;
    el.messageEl.textContent = message;
    el.buttonsEl.innerHTML =
        '<button class="custom-alert-btn custom-alert-btn-secondary" id="custom-alert-cancel">Cancelar</button>' +
        '<button class="custom-alert-btn custom-alert-btn-primary" id="custom-alert-confirm">Confirmar</button>';

    el.overlay.classList.add('show');

    document.getElementById('custom-alert-confirm').onclick = function () {
        closeAlert();
        if (typeof onConfirm === 'function') onConfirm();
    };
    document.getElementById('custom-alert-cancel').onclick = function () {
        closeAlert();
        if (typeof onCancel === 'function') onCancel();
    };
    el.overlay.onclick = function (e) {
        if (e.target === el.overlay) {
            closeAlert();
            if (typeof onCancel === 'function') onCancel();
        }
    };
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureAlertDOM);
} else {
    ensureAlertDOM();
}

function sendSMSNotification(orderId, phone, order) {
    var smsMessage =
        '🎉 Parcero Go\n\nTu pedido #' + orderId + ' ha sido confirmado!\n\n' +
        'Negocio: ' + order.business_name + '\nTotal: ' + (typeof formatCOP === 'function' ? formatCOP(order.total) : '$ ' + (order.total || 0).toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 })) + '\n' +
        'Tiempo estimado: ' + order.estimated_time + ' min\n\n' +
        'Rastrea tu pedido: ' + window.location.origin + '/tracking?phone=' + encodeURIComponent(phone) + '\n\n' +
        'Gracias por tu compra! 🚀';
    console.log('📱 SMS simulado enviado a', phone);
    console.log('Mensaje:', smsMessage);
    if (typeof showNotification !== 'undefined') {
        setTimeout(function () { showNotification('📱 Notificación SMS enviada a tu teléfono'); }, 2000);
    }
}
