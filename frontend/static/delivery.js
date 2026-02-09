var businesses = [];
var selectedBusiness = null;
var selectedProducts = [];
var map;
var businessMarkers = [];
var courierMarkers = [];
var deliveryFiltersBound = false;

var CATEGORIA_SLUG_TO_NAMES = {
    super: ['Supermercado', 'Tienda de Abarrotes'],
    expres: ['Tienda de Abarrotes', 'Supermercado'],
    farmacias: ['Farmacia'],
    panaderia: ['Panadería'],
    restaurantes: ['Restaurante', 'Pizzería', 'Comidas Rápidas'],
    cafe: ['Cafetería'],
    mascotas: ['Veterinaria', 'Tienda de Mascotas']
};
var CATEGORIA_SLUG_TO_LABEL = {
    super: 'Súper', expres: 'Exprés', farmacias: 'Farmacias', panaderia: 'Panadería',
    restaurantes: 'Restaurantes', cafe: 'Café', mascotas: 'Mascotas'
};
var CATEGORY_ICONS = {
    'Comidas Rápidas': '🍔', 'Pizzería': '🍕', 'Restaurante': '🍽️', 'Cafetería': '☕',
    'Farmacia': '💊', 'Panadería': '🥖', 'Supermercado': '🛒', 'Veterinaria': '🐾',
    'Tienda de Mascotas': '🐕', 'Tienda de Abarrotes': '🏪'
};
var CATEGORY_ORDER = ['Comidas Rápidas', 'Pizzería', 'Restaurante', 'Cafetería', 'Farmacia', 'Panadería', 'Supermercado', 'Veterinaria', 'Tienda de Mascotas', 'Tienda de Abarrotes'];
var FAVORITES_KEY = 'delivery_favorites';

function getCategoryFilterFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var slug = (params.get('categoria') || '').toLowerCase().trim();
    if (!slug || !CATEGORIA_SLUG_TO_NAMES[slug]) return null;
    return { slug: slug, names: CATEGORIA_SLUG_TO_NAMES[slug], label: CATEGORIA_SLUG_TO_LABEL[slug] || slug };
}
function highlightActiveCategoryChip() {
    var cat = (new URLSearchParams(window.location.search).get('categoria') || '').toLowerCase();
    document.querySelectorAll('.category-chip[data-categoria]').forEach(function (a) {
        a.classList.toggle('active', a.getAttribute('data-categoria') === cat);
    });
}

function getBusinessImageUrl(businessId, category) {
    if (typeof window.getBusinessImageUrlByCategory === 'function' && category) {
        return window.getBusinessImageUrlByCategory(category, businessId);
    }
    return 'https://picsum.photos/seed/tienda' + businessId + '/80/80';
}
function getProductImageUrl(productId, productName) {
    if (typeof window.getProductImageUrlByName === 'function') {
        var url = window.getProductImageUrlByName(productName);
        if (url) return url;
    }
    return 'https://picsum.photos/seed/prod' + productId + '/400/300';
}

function getFavorites() {
    try {
        var raw = localStorage.getItem(FAVORITES_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
}
function toggleFavorite(businessId) {
    var fav = getFavorites();
    if (fav.indexOf(businessId) >= 0) fav = fav.filter(function (id) { return id !== businessId; });
    else fav.push(businessId);
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(fav));
    displayBusinesses();
}

function setupDeliveryFilters() {
    if (deliveryFiltersBound) return;
    deliveryFiltersBound = true;
    var searchEl = document.getElementById('search-business');
    var openEl = document.getElementById('filter-open');
    var sortEl = document.getElementById('sort-businesses');
    if (searchEl) searchEl.addEventListener('input', displayBusinesses);
    if (openEl) openEl.addEventListener('change', displayBusinesses);
    if (sortEl) sortEl.addEventListener('change', displayBusinesses);
}

function updateCartBadge() {
    var badge = document.getElementById('delivery-cart-badge');
    if (badge && typeof selectedProducts !== 'undefined') {
        var totalItems = selectedProducts.reduce(function (sum, p) { return sum + p.quantity; }, 0);
        badge.textContent = totalItems;
        badge.style.display = totalItems > 0 ? 'inline-block' : 'none';
    }
    if (typeof updateDeliveryCartUI === 'function') updateDeliveryCartUI();
}

function initMap() {
    map = L.map('map', { zoomControl: true, scrollWheelZoom: true, zoomControl: false }).setView([6.2476, -75.5658], 13);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);
    L.control.zoom({ position: 'topright' }).addTo(map);
    L.control.scale({ position: 'bottomleft', metric: true, imperial: false }).addTo(map);
}

var businessIcon = L.divIcon({
    className: 'custom-business-icon',
    html: '<div style="background: linear-gradient(135deg, #00D9A5 0%, #00C896 100%); width: 48px; height: 48px; border-radius: 50%; border: 4px solid white; box-shadow: 0 4px 15px rgba(0, 217, 165, 0.4), 0 0 0 3px rgba(0, 217, 165, 0.1); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 22px; position: relative; animation: pulse 2s infinite;">🏪</div><style>@keyframes pulse { 0% { transform: scale(1); box-shadow: 0 4px 15px rgba(0, 217, 165, 0.4), 0 0 0 3px rgba(0, 217, 165, 0.1); } 50% { transform: scale(1.05); box-shadow: 0 6px 20px rgba(0, 217, 165, 0.6), 0 0 0 6px rgba(0, 217, 165, 0.2); } 100% { transform: scale(1); box-shadow: 0 4px 15px rgba(0, 217, 165, 0.4), 0 0 0 3px rgba(0, 217, 165, 0.1); } }</style>',
    iconSize: [48, 48],
    iconAnchor: [24, 24],
    popupAnchor: [0, -24]
});
var courierIcon = L.divIcon({
    className: 'custom-courier-icon',
    html: '<div style="background: linear-gradient(135deg, #FF6B9D 0%, #FF5A8A 100%); width: 42px; height: 42px; border-radius: 50%; border: 4px solid white; box-shadow: 0 4px 15px rgba(255, 107, 157, 0.4), 0 0 0 3px rgba(255, 107, 157, 0.1); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px; animation: bounce 2s infinite;">🚚</div><style>@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }</style>',
    iconSize: [42, 42],
    iconAnchor: [21, 21],
    popupAnchor: [0, -21]
});

function loadBusinesses() {
    var listEl = document.getElementById('businesses-list');
    if (!listEl) return;
    fetch('/api/delivery/businesses')
        .then(function (response) {
            if (!response.ok) {
                listEl.innerHTML = '<p style="color: #ff6b6b; padding: 1rem; text-align: center;">No se pudieron cargar los negocios. Comprueba que el servidor esté en marcha (puerto 8000).</p>';
                return Promise.reject();
            }
            return response.json();
        })
        .then(function (data) {
            businesses = Array.isArray(data.businesses) ? data.businesses : [];
            if (businesses.length === 0) {
                listEl.innerHTML = '<p style="color: #b8b8b8; padding: 1rem; text-align: center;">No hay negocios cargados. Ejecuta <code>python init_data.py</code> si es la primera vez.</p>';
                return;
            }
            var params = new URLSearchParams(window.location.search);
            var q = params.get('q');
            var searchEl = document.getElementById('search-business');
            if (q && searchEl) { searchEl.value = q; }
            displayBusinesses();
            addBusinessesToMap();
            loadCouriers();
            setupDeliveryFilters();
            highlightActiveCategoryChip();
        })
        .catch(function (err) {
            if (businesses.length === 0 && listEl.innerHTML.indexOf('No se pudieron') === -1) {
                console.error('Error cargando negocios:', err);
                listEl.innerHTML = '<p style="color: #ff6b6b; padding: 1rem; text-align: center;">Error de conexión. Asegúrate de abrir la app en <strong>http://127.0.0.1:8000/delivery</strong> con el servidor encendido.</p>';
            }
        });
}

function loadCouriers() {
    fetch('/api/couriers/available')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (!data.couriers || !map) return;
            data.couriers.forEach(function (courier) {
                var marker = L.marker([courier.lat, courier.lng], { icon: courierIcon }).addTo(map);
                marker.bindPopup(
                    '<div style="min-width: 250px; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">' +
                    '<div style="background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%); color: #0a0a0a; padding: 1rem; border-radius: 12px 12px 0 0; margin: -12px -12px 1rem -12px;">' +
                    '<h4 style="margin: 0; font-size: 1.2rem; font-weight: 700;">🚚 ' + courier.name + '</h4></div>' +
                    '<div style="padding: 0.5rem 0;">' +
                    '<div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;"><span style="font-size: 1.1rem;">🗺️</span><span style="color: #b8b8b8; font-size: 0.9rem;"><strong style="color: #D4AF37;">Zona:</strong> ' + courier.zone + '</span></div>' +
                    '<div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;"><span style="font-size: 1.1rem;">🚗</span><span style="color: #b8b8b8; font-size: 0.9rem;"><strong style="color: #D4AF37;">Vehículo:</strong> ' + courier.vehicle + '</span></div>' +
                    '<div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;"><span style="font-size: 1.1rem;">⭐</span><span style="color: #b8b8b8; font-size: 0.9rem;"><strong style="color: #D4AF37;">Rating:</strong> ' + courier.rating + '</span></div>' +
                    '<div style="margin: 1rem 0 0 0;"><span style="background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%); color: #0a0a0a; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; display: inline-block;">✓ Disponible</span></div></div></div>',
                    { maxWidth: 280, className: 'custom-popup' }
                );
                courierMarkers.push(marker);
            });
        })
        .catch(function (e) { console.error('Error cargando repartidores:', e); });
}

function displayBusinesses() {
    var list = document.getElementById('businesses-list');
    if (!list) return;
    list.innerHTML = '';

    var categoryFilter = getCategoryFilterFromUrl();
    var searchEl = document.getElementById('search-business');
    var query = (searchEl && searchEl.value || '').toLowerCase().trim();
    var filterOpenEl = document.getElementById('filter-open');
    var onlyOpen = filterOpenEl && filterOpenEl.checked;
    var sortEl = document.getElementById('sort-businesses');
    var sortBy = (sortEl && sortEl.value) || 'name';

    var filtered = businesses.filter(function (b) {
        if (categoryFilter && categoryFilter.names.indexOf(b.category) === -1) return false;
        var match = !query || (b.name || '').toLowerCase().indexOf(query) !== -1 || (b.category || '').toLowerCase().indexOf(query) !== -1;
        var open = !onlyOpen || b.is_open;
        return match && open;
    });
    if (sortBy === 'rating') filtered.sort(function (a, b) { return (Number(b.rating) || 0) - (Number(a.rating) || 0); });
    else if (sortBy === 'time') filtered.sort(function (a, b) { return (Number(a.delivery_time) || 99) - (Number(b.delivery_time) || 99); });
    else filtered.sort(function (a, b) { return (a.name || '').localeCompare(b.name || ''); });

    var favorites = getFavorites();

    if (filtered.length === 0) {
        var msg = categoryFilter ? ('No hay tiendas de ' + categoryFilter.label + ' en este momento. Prueba otra categoría o quita el filtro.') : 'No hay negocios que coincidan con tu búsqueda.';
        list.innerHTML = '<p style="color: #b8b8b8; padding: 1rem; text-align: center;">' + msg + '</p>';
        return;
    }

    function groupByCategory(arr) {
        var byCat = {};
        arr.forEach(function (b) {
            var cat = b.category || 'Otros';
            if (!byCat[cat]) byCat[cat] = [];
            byCat[cat].push(b);
        });
        var rest = Object.keys(byCat).filter(function (c) { return CATEGORY_ORDER.indexOf(c) === -1; });
        return CATEGORY_ORDER.filter(function (c) { return byCat[c]; }).concat(rest).map(function (c) { return { category: c, list: byCat[c] }; });
    }
    function flatOrderByCategory(arr) {
        var byCat = {};
        arr.forEach(function (b) {
            var cat = b.category || 'Otros';
            if (!byCat[cat]) byCat[cat] = [];
            byCat[cat].push(b);
        });
        var rest = Object.keys(byCat).filter(function (c) { return CATEGORY_ORDER.indexOf(c) === -1; });
        return CATEGORY_ORDER.filter(function (c) { return byCat[c]; }).concat(rest).reduce(function (acc, c) { return acc.concat(byCat[c]); }, []);
    }

    var businessesToShow = categoryFilter ? filtered : flatOrderByCategory(filtered);
    var groups = categoryFilter ? [{ list: businessesToShow }] : groupByCategory(businessesToShow);

    function renderBusinessCard(business) {
        var isOpen = business.is_open
            ? '<span style="background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%); color: #0a0a0a; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">✓ Abierto</span>'
            : '<span style="background: #ff4444; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">✗ Cerrado</span>';
        var nameEscaped = (business.name || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        var categoryEscaped = (business.category || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        var isFav = favorites.indexOf(business.id) >= 0;
        var imgUrl = getBusinessImageUrl(business.id, business.category);
        var item = document.createElement('div');
        item.className = 'business-card';
        item.setAttribute('data-business-id', business.id);
        item.style.cssText = 'background: #1a1a1a; border: 2px solid #2a2a2a; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; cursor: pointer; transition: all 0.3s; display: flex; gap: 1rem; align-items: flex-start;';
        item.innerHTML = '<div style="flex: 1; min-width: 0;"><div style="display: flex; justify-content: space-between; align-items: flex-start;"><h4 style="margin: 0 0 0.5rem 0; color: #ffffff; font-size: 1.1rem;">' + nameEscaped + '</h4><button type="button" onclick="event.stopPropagation(); toggleFavorite(' + business.id + ');" aria-label="' + (isFav ? 'Quitar de favoritos' : 'Añadir a favoritos') + '" style="background: none; border: none; cursor: pointer; font-size: 1.2rem; padding: 0;">' + (isFav ? '❤️' : '🤍') + '</button></div><p style="color: #b8b8b8; margin: 0.3rem 0; font-size: 0.9rem;">' + categoryEscaped + '</p><div style="display: flex; align-items: center; gap: 1rem; margin: 0.5rem 0; flex-wrap: wrap;"><span style="color: #D4AF37; font-weight: 600;">⭐ ' + (Number(business.rating) || 0) + '</span><span style="color: #D4AF37; font-weight: 600;">⏱️ ' + (Number(business.delivery_time) || 0) + ' min</span></div><div style="margin: 0.8rem 0 0 0;">' + isOpen + '</div><button type="button" style="width: 100%; margin-top: 0.8rem; padding: 0.6rem; background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%); color: #0a0a0a; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">Ver Productos →</button></div><img src="' + imgUrl + '" alt="" style="width: 56px; height: 56px; border-radius: 50%; object-fit: cover; flex-shrink: 0;" onerror="this.style.display=\'none\'">';
        item.addEventListener('mouseenter', function () {
            this.style.borderColor = '#D4AF37';
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 15px rgba(212, 175, 55, 0.3)';
        });
        item.addEventListener('mouseleave', function () {
            if (!selectedBusiness || selectedBusiness.id !== business.id) {
                this.style.borderColor = '#2a2a2a';
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            }
        });
        item.onclick = function (e) {
            e.preventDefault();
            e.stopPropagation();
            selectBusiness(business.id);
            if (typeof map !== 'undefined' && map && business.latitude != null && business.longitude != null) {
                map.setView([business.latitude, business.longitude], 15);
            }
        };
        return item;
    }

    if (categoryFilter) {
        var categoryTitle = document.createElement('div');
        categoryTitle.style.cssText = 'margin: 0 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #D4AF37; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;';
        var icon = CATEGORY_ICONS[filtered[0] && filtered[0].category] || '🏪';
        categoryTitle.innerHTML = '<h4 style="color: #D4AF37; font-size: 1.1rem; margin: 0; font-weight: 700;">' + icon + ' Tiendas de ' + categoryFilter.label + ' (' + filtered.length + ')</h4><a href="/delivery" style="color: #D4AF37; font-size: 0.9rem; font-weight: 600;">Ver todas las tiendas</a>';
        list.appendChild(categoryTitle);
        businessesToShow.forEach(function (business) { list.appendChild(renderBusinessCard(business)); });
    } else {
        groups.forEach(function (g) {
            var category = g.category;
            var items = g.list;
            var categoryTitle = document.createElement('div');
            categoryTitle.style.cssText = 'margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #D4AF37;';
            var icon = CATEGORY_ICONS[category] || '🏪';
            categoryTitle.innerHTML = '<h4 style="color: #D4AF37; font-size: 1.1rem; margin: 0; font-weight: 700;">' + icon + ' ' + category + '</h4>';
            list.appendChild(categoryTitle);
            items.forEach(function (business) { list.appendChild(renderBusinessCard(business)); });
        });
    }
}

function selectBusiness(businessId) {
    selectedBusiness = businesses.filter(function (b) { return b.id === businessId; })[0];
    if (!selectedBusiness) return;
    selectedProducts = [];

    document.querySelectorAll('.business-card').forEach(function (card) {
        card.style.borderColor = '#2a2a2a';
        card.style.background = '#1a1a1a';
    });
    var selectedCard = document.querySelector('.business-card[data-business-id="' + businessId + '"]');
    if (selectedCard) {
        selectedCard.style.borderColor = '#D4AF37';
        selectedCard.style.background = '#151515';
    }

    document.getElementById('business-name').textContent = selectedBusiness.name;
    document.getElementById('business-info').innerHTML =
        '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem; padding: 1.5rem; background: #151515; border-radius: 12px; border: 1px solid #2a2a2a;">' +
        '<div><p style="color: #b8b8b8; margin: 0.5rem 0;"><strong style="color: #D4AF37;">Categoría:</strong> ' + selectedBusiness.category + '</p><p style="color: #b8b8b8; margin: 0.5rem 0;"><strong style="color: #D4AF37;">📍 Dirección:</strong> ' + selectedBusiness.address + '</p></div>' +
        '<div><p style="color: #b8b8b8; margin: 0.5rem 0;"><strong style="color: #D4AF37;">📞 Teléfono:</strong> ' + selectedBusiness.phone + '</p><p style="color: #b8b8b8; margin: 0.5rem 0;"><strong style="color: #D4AF37;">⭐ Rating:</strong> ' + selectedBusiness.rating + '</p><p style="color: #b8b8b8; margin: 0.5rem 0;"><strong style="color: #D4AF37;">⏱️ Tiempo:</strong> ' + selectedBusiness.delivery_time + ' min</p></div></div>';
    document.getElementById('business-details').style.display = 'block';
    var emptyEl = document.getElementById('business-details-empty');
    if (emptyEl) emptyEl.style.display = 'none';

    var listEl = document.getElementById('products-list');
    listEl.innerHTML = '<div class="products-loading" style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:3rem 1rem;color:var(--text-muted);"><div style="width:40px;height:40px;border:3px solid var(--border-color);border-top-color:var(--primary-color);border-radius:50%;animation:spin 0.8s linear infinite;"></div><p style="margin:1rem 0 0 0;font-size:1rem;">Cargando productos…</p></div>';

    fetch('/api/delivery/businesses/' + businessId + '/products')
        .then(function (r) { return r.json(); })
        .then(function (data) { displayProducts(data.products || []); })
        .catch(function (e) {
            console.error('Error cargando productos:', e);
            listEl.innerHTML = '<h4 style="margin-bottom:1rem;color:var(--primary-color);">🍽️ Productos</h4><p style="color:#ff6b6b;text-align:center;padding:2rem;">No se pudieron cargar los productos. Intenta de nuevo.</p>';
        });
}

function displayProducts(products) {
    var list = document.getElementById('products-list');
    list.innerHTML = '<h4 style="margin-bottom: 1.5rem; color: #D4AF37; font-size: 1.5rem; border-bottom: 2px solid #D4AF37; padding-bottom: 0.5rem;">🍽️ Productos Disponibles</h4>';
    if (!products.length) {
        list.innerHTML += '<p style="color: #b8b8b8; text-align: center; padding: 2rem;">No hay productos disponibles</p>';
        return;
    }
    products.forEach(function (product) {
        if (product.available === false) return;
        var item = document.createElement('div');
        item.className = 'product-card-modern';
        var productImgUrl = (typeof getProductImageUrlByName === 'function' && window.getProductImageUrlByName(product.name)) || product.image || getProductImageUrl(product.id, product.name);
        var fallbackImgUrl = 'https://picsum.photos/seed/alt' + product.id + '/400/300';
        var nameEsc = (product.name || '').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        item.innerHTML =
            '<div style="position: relative; margin-bottom: 1rem;">' +
            '<img src="' + productImgUrl + '" alt="' + nameEsc + '" style="width: 100%; height: 180px; object-fit: cover; border-radius: 12px; border: 2px solid #2a2a2a;" onerror="this.onerror=null; this.src=\'' + fallbackImgUrl + '\';">' +
            '</div><h4 style="margin: 0.5rem 0; color: #ffffff; font-size: 1rem; min-height: 2.5rem; line-height: 1.3;">' + (product.name || '') + '</h4>' +
            '<p style="color: #b8b8b8; margin: 0.3rem 0; font-size: 0.85rem; min-height: 2rem;">' + (product.description || '') + '</p>' +
            '<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">' +
            '<p class="price" style="color: #D4AF37; font-size: 1.3rem; font-weight: 700; margin: 0;">' + (typeof formatCOP === 'function' ? formatCOP(product.price || 0) : '$ ' + (product.price || 0).toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 })) + '</p>' +
            '<button type="button" onclick="openAddOptionsModal(' + product.id + ', \'' + (product.name || '').replace(/'/g, "\\'") + '\', ' + (product.price || 0) + ')" style="background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%); color: #0a0a0a; border: none; padding: 0.6rem 1.2rem; border-radius: 25px; font-weight: 600; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);">+ Agregar</button>' +
            '</div>';
        list.appendChild(item);
    });
    updateOrderTotal();
}

var addOptionsPending = null;

function openAddOptionsModal(productId, name, price) {
    addOptionsPending = { productId: productId, name: name, price: price };
    var nameEl = document.getElementById('add-options-product-name');
    var sizeEl = document.getElementById('add-options-size');
    var notesEl = document.getElementById('add-options-notes');
    if (nameEl) nameEl.textContent = name;
    if (sizeEl) sizeEl.value = '';
    if (notesEl) notesEl.value = '';
    document.getElementById('add-options-overlay').style.display = 'block';
    document.getElementById('add-options-modal').style.display = 'block';
    var btn = document.getElementById('add-options-confirm-btn');
    if (btn) {
        btn.onclick = function () {
            confirmAddWithOptions();
        };
    }
}

function closeAddOptionsModal() {
    addOptionsPending = null;
    document.getElementById('add-options-overlay').style.display = 'none';
    document.getElementById('add-options-modal').style.display = 'none';
}

function animateFlyToCart() {
    var startBtn = document.getElementById('add-options-confirm-btn');
    var endBtn = document.querySelector('.cart-icon-btn');
    if (!startBtn || !endBtn) return;
    var startR = startBtn.getBoundingClientRect();
    var endR = endBtn.getBoundingClientRect();
    var startX = startR.left + startR.width / 2;
    var startY = startR.top + startR.height / 2;
    var endX = endR.left + endR.width / 2;
    var endY = endR.top + endR.height / 2;
    var fly = document.createElement('div');
    fly.setAttribute('aria-hidden', 'true');
    fly.style.cssText = 'position:fixed;left:' + startX + 'px;top:' + startY + 'px;width:32px;height:32px;margin-left:-16px;margin-top:-16px;z-index:9999;border-radius:50%;background:linear-gradient(135deg,#D4AF37,#FF8C00);color:#1a1a1a;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(212,175,55,0.5);transition:left 0.45s cubic-bezier(0.25,0.46,0.45,0.94),top 0.45s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.45s;pointer-events:none;';
    fly.textContent = '+1';
    document.body.appendChild(fly);
    requestAnimationFrame(function() {
        requestAnimationFrame(function() {
            fly.style.left = endX + 'px';
            fly.style.top = endY + 'px';
            fly.style.transform = 'scale(0.3)';
            fly.style.opacity = '0.6';
        });
    });
    setTimeout(function() {
        fly.remove();
        if (endBtn) {
            endBtn.style.transition = 'transform 0.2s ease';
            endBtn.style.transform = 'scale(1.2)';
            setTimeout(function() { endBtn.style.transform = ''; }, 200);
        }
    }, 480);
}

function confirmAddWithOptions() {
    if (!addOptionsPending) return;
    var sizeEl = document.getElementById('add-options-size');
    var notesEl = document.getElementById('add-options-notes');
    var size = (sizeEl && sizeEl.value) ? sizeEl.value.trim() : '';
    var notes = (notesEl && notesEl.value) ? notesEl.value.trim() : '';
    var parts = [];
    if (size) parts.push('Tamaño: ' + size);
    if (notes) parts.push(notes);
    var fullNotes = parts.join('. ');
    addProduct(addOptionsPending.productId, addOptionsPending.name, addOptionsPending.price, fullNotes);
    animateFlyToCart();
    closeAddOptionsModal();
}

function addProduct(productId, name, price, notes) {
    var existing = selectedProducts.filter(function (p) { return p.product_id === productId && (p.notes || '') === (notes || ''); })[0];
    if (existing) existing.quantity += 1;
    else selectedProducts.push({ product_id: productId, name: name, price: price, quantity: 1, notes: (notes || '').trim() });
    updateSelectedProducts();
    updateOrderTotal();
    updateCartBadge();
    if (typeof showNotification !== 'undefined') showNotification(name + ' agregado al carrito');
}
function removeProduct(index) {
    selectedProducts.splice(index, 1);
    updateSelectedProducts();
    updateOrderTotal();
    updateCartBadge();
}
function updateSelectedProducts() {
    var container = document.getElementById('selected-products');
    if (!container) return;
    container.innerHTML = '<h4 style="margin-bottom: 1rem; color: #D4AF37; font-size: 1.2rem; border-bottom: 2px solid #D4AF37; padding-bottom: 0.5rem;">🛒 Productos Seleccionados</h4>';
    if (selectedProducts.length === 0) {
        container.innerHTML += '<p style="color: #b8b8b8; text-align: center; padding: 1rem;">No hay productos seleccionados</p>';
    } else {
        selectedProducts.forEach(function (product, index) {
            var item = document.createElement('div');
            item.className = 'product-item';
            item.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 1rem; margin-bottom: 0.8rem; background: #151515; border: 1px solid #2a2a2a; border-radius: 12px;';
            item.innerHTML = '<div><strong style="color: #ffffff; font-size: 1rem;">' + product.name + '</strong><p style="color: #b8b8b8; margin: 0.3rem 0; font-size: 0.9rem;">Cantidad: ' + product.quantity + ' x ' + (typeof formatCOP === 'function' ? formatCOP(product.price) : '$ ' + (product.price || 0).toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 })) + '</p><p class="price" style="color: #D4AF37; font-weight: 700; font-size: 1.1rem; margin: 0.3rem 0;">Subtotal: ' + (typeof formatCOP === 'function' ? formatCOP(product.price * product.quantity) : '$ ' + (product.price * product.quantity).toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 })) + '</p></div><button onclick="removeProduct(' + index + ')" style="background: #ff4444; color: white; border: none; padding: 0.6rem 1rem; border-radius: 8px; font-weight: 600; cursor: pointer;">Eliminar</button>';
            container.appendChild(item);
        });
    }
    updateCartBadge();
}
function updateOrderTotal() {
    var total = selectedProducts.reduce(function (sum, p) { return sum + (p.price * p.quantity); }, 0);
    var totalElement = document.getElementById('order-total');
    if (totalElement) {
        totalElement.textContent = typeof formatCOP === 'function' ? formatCOP(total) : '$ ' + total.toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
        totalElement.style.color = '#D4AF37';
    }
    var cartTotal = document.getElementById('delivery-cart-total');
    if (cartTotal) cartTotal.textContent = typeof formatCOP === 'function' ? formatCOP(total) : '$ ' + total.toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

function addBusinessesToMap() {
    if (typeof map === 'undefined' || !map || typeof L === 'undefined') return;
    businessMarkers.forEach(function (m) { try { map.removeLayer(m); } catch (e) {} });
    businessMarkers = [];
    var categoryFilter = getCategoryFilterFromUrl();
    var toShow = categoryFilter
        ? businesses.filter(function (b) { return categoryFilter.names.indexOf(b.category) !== -1; })
        : businesses;
    toShow.forEach(function (business) {
        var marker = L.marker([business.latitude, business.longitude], { icon: businessIcon }).addTo(map);
        var isOpen = business.is_open ? '<span class="badge badge-success">Abierto</span>' : '<span class="badge badge-warning">Cerrado</span>';
        marker.bindPopup(
            '<div style="min-width: 280px; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">' +
            '<div style="background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%); color: #0a0a0a; padding: 1rem; border-radius: 12px 12px 0 0; margin: -12px -12px 1rem -12px;">' +
            '<h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">' + business.name + '</h3><p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">' + business.category + '</p></div>' +
            '<div style="padding: 0.5rem 0;">' +
            '<div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;"><span style="font-size: 1.2rem;">📍</span><span style="color: #b8b8b8; font-size: 0.9rem;">' + business.address + '</span></div>' +
            '<div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;"><span style="font-size: 1.2rem;">⭐</span><span style="color: #b8b8b8; font-size: 0.9rem;"><strong style="color: #D4AF37;">' + business.rating + '</strong> rating</span></div>' +
            '<div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;"><span style="font-size: 1.2rem;">⏱️</span><span style="color: #D4AF37; font-weight: 600; font-size: 0.9rem;">' + business.delivery_time + ' min</span></div>' +
            '<div style="margin: 1rem 0 0 0;">' + isOpen + '</div></div></div>',
            { maxWidth: 300, className: 'custom-popup' }
        );
        marker.on('click', function () { selectBusiness(business.id); });
        businessMarkers.push(marker);
    });
}

try {
    if (document.getElementById('map')) initMap();
} catch (e) { console.warn('Mapa no inicializado:', e); }
loadBusinesses();
