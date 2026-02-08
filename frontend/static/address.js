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
    /** Rellena el bloque .app-header-address y lo hace editable al clic. */
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

        function onEdit() {
            var current = getCurrentAddress();
            var newAddr = prompt('Editar dirección de entrega:', current);
            if (newAddr !== null && newAddr.trim()) {
                setCurrentAddress(newAddr.trim());
                updateDisplay();
                block.setAttribute('aria-label', 'Cambiar dirección de entrega. Actual: ' + getCurrentAddress());
            }
        }
        block.addEventListener('click', onEdit);
        block.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onEdit(); }
        });
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHeaderAddress);
    } else {
        initHeaderAddress();
    }
})();
