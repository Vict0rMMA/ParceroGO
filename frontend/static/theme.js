(function () {
    var THEME_KEY = 'delivery_theme';
    var LANG_KEY = 'delivery_lang';

    function getStoredTheme() {
        return localStorage.getItem(THEME_KEY) || 'dark';
    }
    function setStoredTheme(theme) {
        theme = theme === 'light' ? 'light' : 'dark';
        localStorage.setItem(THEME_KEY, theme);
        document.documentElement.setAttribute('data-theme', theme);
    }
    function getStoredLang() {
        return localStorage.getItem(LANG_KEY) || 'es';
    }
    function setStoredLang(lang) {
        lang = lang === 'en' ? 'en' : 'es';
        localStorage.setItem(LANG_KEY, lang);
        document.documentElement.setAttribute('lang', lang);
        if (window.onLangChange) window.onLangChange(lang);
    }

    function init() {
        setStoredTheme(getStoredTheme());
        setStoredLang(getStoredLang());
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {
            navigator.serviceWorker.register('/static/sw.js').catch(function () {});
        });
    }

    window.toggleTheme = function () {
        setStoredTheme(getStoredTheme() === 'dark' ? 'light' : 'dark');
    };
    window.setTheme = setStoredTheme;
    window.getTheme = getStoredTheme;
    window.toggleLang = function () {
        setStoredLang(getStoredLang() === 'es' ? 'en' : 'es');
    };
    window.setLang = setStoredLang;
    window.getLang = getStoredLang;

    window.i18n = {
        es: {
            nav_inicio: 'Inicio', nav_delivery: 'Delivery', nav_tracking: 'Seguimiento',
            nav_perfil: 'Perfil', nav_repartidor: 'Repartidor',
            hero_title: 'Delivery para Negocios de Barrio', hero_sub: 'Pedidos rápidos desde negocios locales en Medellín',
            businesses: 'Negocios Locales', see_all: 'Ver todos', delivery_fast: 'Entrega Rápida', pay_simple: 'Pagos Simples',
            theme_dark: 'Modo oscuro', theme_light: 'Modo claro', lang_es: 'ES', lang_en: 'EN'
        },
        en: {
            nav_inicio: 'Home', nav_delivery: 'Delivery', nav_tracking: 'Tracking',
            nav_perfil: 'Profile', nav_repartidor: 'Courier',
            hero_title: 'Delivery for Local Businesses', hero_sub: 'Fast orders from local businesses in Medellín',
            businesses: 'Local Businesses', see_all: 'See all', delivery_fast: 'Fast Delivery', pay_simple: 'Simple Payments',
            theme_dark: 'Dark mode', theme_light: 'Light mode', lang_es: 'ES', lang_en: 'EN'
        }
    };
    window.t = function (key) {
        var lang = getStoredLang();
        var dict = window.i18n[lang] || window.i18n.es;
        return dict[key] != null ? dict[key] : (window.i18n.es[key] || key);
    };
})();
