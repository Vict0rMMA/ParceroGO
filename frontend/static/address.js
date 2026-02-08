/**
 * address.js — Dirección de entrega, sesión simulada y perfil de usuario.
 * Todo se persiste en localStorage (sin backend real).
 */

(function () {
    // --- Constantes de almacenamiento ---
    var STORAGE_KEY = 'delivery_current_address';
    var PROFILE_KEY = 'parcero_user_profile';
    var SESSION_KEY = 'parcero_session';
    var USER_NAME_KEY = 'parcero_user_name';
    var USER_PHONE_KEY = 'parcero_user_phone';
    var ADDRESSES_KEY = 'delivery_saved_addresses';
    var DEFAULT_ADDRESS = 'Calle 39B #109-46, Medellín';

    // --- Sesión simulada ---
    window.isSessionActive = function () {
        try { return localStorage.getItem(SESSION_KEY) === 'true'; } catch (e) { return false; }
    };
    window.setSession = function (active) {
        try {
            if (active) localStorage.setItem(SESSION_KEY, 'true');
            else localStorage.removeItem(SESSION_KEY);
        } catch (e) {}
    };
    window.setSessionUser = function (name, phone) {
        try {
            if (name != null) localStorage.setItem(USER_NAME_KEY, String(name).trim());
            if (phone != null) localStorage.setItem(USER_PHONE_KEY, String(phone).trim());
        } catch (e) {}
    };
    window.getSessionUserName = function () {
        try { return localStorage.getItem(USER_NAME_KEY) || ''; } catch (e) { return ''; }
    };
    window.getSessionUserPhone = function () {
        try { return localStorage.getItem(USER_PHONE_KEY) || ''; } catch (e) { return ''; }
    };

    // --- Dirección actual ---
    window.getCurrentAddress = function () {
        try {
            var s = localStorage.getItem(STORAGE_KEY);
            return (s && s.trim()) ? s.trim() : DEFAULT_ADDRESS;
        } catch (e) { return DEFAULT_ADDRESS; }
    };
    window.setCurrentAddress = function (addr) {
        try {
            if (addr && typeof addr === 'string' && addr.trim()) {
                localStorage.setItem(STORAGE_KEY, addr.trim());
                return true;
            }
        } catch (e) {}
        return false;
    };

    // --- Perfil de usuario (nombre, teléfono, dirección) ---
    window.getUserProfile = function () {
        try {
            var s = localStorage.getItem(PROFILE_KEY);
            if (s) {
                var o = JSON.parse(s);
                return { name: o.name || '', phone: o.phone || '', address: o.address || '' };
            }
        } catch (e) {}
        return { name: '', phone: '', address: '' };
    };
    window.setUserProfile = function (profile) {
        try {
            if (profile && typeof profile === 'object') {
                var o = {
                    name: (profile.name && String(profile.name).trim()) ? String(profile.name).trim() : '',
                    phone: (profile.phone && String(profile.phone).trim()) ? String(profile.phone).trim() : '',
                    address: (profile.address && String(profile.address).trim()) ? String(profile.address).trim() : ''
                };
                localStorage.setItem(PROFILE_KEY, JSON.stringify(o));
                if (o.address) setCurrentAddress(o.address);
                return true;
            }
        } catch (e) {}
        return false;
    };
    window.isUserRegistered = function () { return isSessionActive(); };

    // --- Cerrar sesión (borra sesión, perfil, direcciones) ---
    window.clearSession = function () {
        try {
            localStorage.removeItem(SESSION_KEY);
            localStorage.removeItem(USER_NAME_KEY);
            localStorage.removeItem(USER_PHONE_KEY);
            localStorage.removeItem(PROFILE_KEY);
            localStorage.removeItem('delivery_user');
            localStorage.removeItem(ADDRESSES_KEY);
        } catch (e) {}
    };

    // --- Navbar: mostrar "Iniciar sesión" o "Perfil" según sesión ---
    window.initNavSession = function () {
        var loginLink = document.querySelector('.nav-link-login');
        var perfilLink = document.querySelector('.nav-link-perfil');
        if (loginLink && perfilLink) {
            var logged = isSessionActive();
            loginLink.style.display = logged ? 'none' : 'inline-block';
            loginLink.setAttribute('aria-hidden', logged ? 'true' : 'false');
            perfilLink.style.display = logged ? 'inline-block' : 'none';
            perfilLink.setAttribute('aria-hidden', logged ? 'false' : 'true');
        }
    };
})();

(function () {
    var ADDRESSES_KEY = 'delivery_saved_addresses';

    function getSavedAddresses() {
        try {
            var raw = localStorage.getItem(ADDRESSES_KEY);
            return raw ? JSON.parse(raw) : [];
        } catch (e) { return []; }
    }
    function setSavedAddresses(list) {
        try {
            localStorage.setItem(ADDRESSES_KEY, JSON.stringify(list));
            return true;
        } catch (e) { return false; }
    }

    function escapeHtml(s) {
        if (!s) return '';
        var div = document.createElement('div');
        div.textContent = s;
        return div.innerHTML;
    }

    /** Modal bonito para editar dirección (reemplaza el prompt feo del navegador). */
    function showEditAddressDialog(value, title, onDone) {
        var overlay = document.createElement('div');
        overlay.className = 'address-edit-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-label', title);
        var card = document.createElement('div');
        card.className = 'address-edit-card';
        card.innerHTML =
            '<p class="address-edit-title">' + escapeHtml(title) + '</p>' +
            '<input type="text" class="address-edit-input" value="' + escapeHtml(value || '') + '" placeholder="Ej: Calle 50 #30-20, Medellín" autocomplete="street-address">' +
            '<div class="address-edit-actions">' +
            '<button type="button" class="address-edit-btn address-edit-cancel">Cancelar</button>' +
            '<button type="button" class="address-edit-btn address-edit-ok">Aceptar</button>' +
            '</div>';
        overlay.appendChild(card);
        document.body.appendChild(overlay);
        requestAnimationFrame(function () { overlay.classList.add('show'); });

        var input = card.querySelector('.address-edit-input');
        input.focus();
        input.select();

        function close(result) {
            overlay.classList.remove('show');
            setTimeout(function () {
                if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
            }, 250);
            if (typeof onDone === 'function') onDone(result);
        }

        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) close(null);
        });
        card.querySelector('.address-edit-cancel').addEventListener('click', function () { close(null); });
        card.querySelector('.address-edit-ok').addEventListener('click', function () {
            var v = (input.value || '').trim();
            close(v || null);
        });
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') close(null);
            if (e.key === 'Enter') {
                e.preventDefault();
                var v = (input.value || '').trim();
                close(v || null);
            }
        });
    }

    /** Abre el modal de selección de dirección. onUpdateDisplay se llama al elegir una dirección. */
    window.openAddressModal = function (onUpdateDisplay) {
        onUpdateDisplay = onUpdateDisplay || function () {};
        var overlay = document.getElementById('address-modal-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'address-modal-overlay';
            overlay.className = 'address-modal-overlay';
            overlay.setAttribute('aria-modal', 'true');
            overlay.setAttribute('aria-labelledby', 'address-modal-title');
            var panel = document.createElement('div');
            panel.className = 'address-modal-panel';
            panel.innerHTML =
                '<div class="address-modal-header">' +
                '<button type="button" class="address-modal-back" aria-label="Cerrar">‹</button>' +
                '<h2 id="address-modal-title" class="address-modal-title">Selecciona una dirección</h2>' +
                '</div>' +
                '<input type="text" class="address-modal-search" placeholder="Busca para agregar una dirección" aria-label="Buscar dirección">' +
                '<div class="address-current-card">' +
                '<div class="address-current-icon">📍</div>' +
                '<div class="address-current-body">' +
                '<p class="address-current-label">Ubicación actual</p>' +
                '<p class="address-current-addr" id="address-modal-current-text"></p>' +
                '<button type="button" class="address-current-btn" id="address-modal-update-btn">Actualizar</button>' +
                '</div></div>' +
                '<p class="address-section-title">Direcciones recientes</p>' +
                '<ul class="address-list" id="address-modal-list"></ul>' +
                '<p class="address-list-empty" id="address-modal-empty" style="display:none;">No tienes direcciones guardadas. Guarda una al confirmar un pedido.</p>';
            overlay.appendChild(panel);
            document.body.appendChild(overlay);

            overlay.addEventListener('click', function (e) {
                if (e.target === overlay) closeModal();
            });
            panel.querySelector('.address-modal-back').addEventListener('click', closeModal);
            document.getElementById('address-modal-update-btn').addEventListener('click', function () {
                var current = getCurrentAddress();
                showEditAddressDialog(current, 'Editar ubicación actual', function (newAddr) {
                    if (newAddr) {
                        setCurrentAddress(newAddr);
                        var el = document.getElementById('address-modal-current-text');
                        if (el) el.textContent = getCurrentAddress();
                        onUpdateDisplay();
                    }
                });
            });
        }

        function closeModal() {
            overlay.classList.remove('show');
        }

        document.getElementById('address-modal-current-text').textContent = getCurrentAddress();
        var list = getSavedAddresses();
        var listEl = document.getElementById('address-modal-list');
        var emptyEl = document.getElementById('address-modal-empty');
        listEl.innerHTML = '';
        if (!list || list.length === 0) {
            emptyEl.style.display = 'block';
        } else {
            emptyEl.style.display = 'none';
            var currentAddr = getCurrentAddress();
            list.forEach(function (a, i) {
                var addr = (a.address || '').trim();
                if (!addr) return;
                var li = document.createElement('li');
                var isSelected = addr === currentAddr;
                if (isSelected) li.classList.add('selected');
                var shortLine = addr.length > 45 ? addr.substring(0, 45) + '…' : addr;
                li.innerHTML =
                    '<span class="addr-pin">📍</span>' +
                    '<div class="addr-content">' +
                    (a.name ? '<span class="addr-tag">' + escapeHtml(a.name) + '</span>' : '') +
                    '<p class="addr-line">' + escapeHtml(shortLine) + '</p>' +
                    '<p class="addr-detail">' + escapeHtml(addr) + '</p>' +
                    '</div>' +
                    '<button type="button" class="addr-edit" aria-label="Editar" data-index="' + i + '">✎</button>';
                li.addEventListener('click', function (e) {
                    if (e.target.closest('.addr-edit')) return;
                    setCurrentAddress(addr);
                    onUpdateDisplay();
                    closeModal();
                });
                li.querySelector('.addr-edit').addEventListener('click', function (e) {
                    e.stopPropagation();
                    showEditAddressDialog(addr, 'Editar dirección', function (newAddr) {
                        if (newAddr) {
                            list[i] = { name: a.name || 'Dirección', address: newAddr };
                            setSavedAddresses(list);
                            openAddressModal(onUpdateDisplay);
                        }
                    });
                });
                listEl.appendChild(li);
            });
        }
        overlay.classList.add('show');
    };

    /** Rellena el bloque .app-header-address y al clic abre el modal de dirección. */
    window.initHeaderAddress = function () {
        var block = document.querySelector('.app-header-address');
        if (!block) return;
        var textEl = block.querySelector('.addr-text') || block.querySelector('span:first-child');
        if (!textEl) return;

        function updateDisplay() {
            textEl.textContent = '\uD83D\uDCCD ' + getCurrentAddress();
        }
        updateDisplay();
        block.setAttribute('role', 'button');
        block.setAttribute('tabindex', '0');
        block.setAttribute('aria-label', 'Cambiar dirección de entrega. Actual: ' + getCurrentAddress());
        block.title = 'Clic para cambiar dirección';
        block.style.cursor = 'pointer';

        block.addEventListener('click', function () {
            openAddressModal(updateDisplay);
            if (block.getAttribute('aria-label')) block.setAttribute('aria-label', 'Cambiar dirección de entrega. Actual: ' + getCurrentAddress());
        });
        block.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openAddressModal(updateDisplay);
            }
        });
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHeaderAddress);
    } else {
        initHeaderAddress();
    }
})();
