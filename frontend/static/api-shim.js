(function () {
    'use strict';
    window.formatCOP = function (n) {
        return '$ ' + (Number(n) || 0).toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
    };
    var origin = window.location.origin || '';
    var isBackend = origin.indexOf('localhost:8000') !== -1 || origin.indexOf('127.0.0.1:8000') !== -1 || origin.indexOf('onrender.com') !== -1;
    if (isBackend) return;
    var REAL_FETCH = window.fetch;
    var DATA_PREFIX = '/data/';
    var ORDERS_KEY = 'parcerogo_orders';
    var COURIERS_KEY = 'parcerogo_couriers';

    function haversine(lat1, lng1, lat2, lng2) {
        var R = 6371;
        var dlat = (lat2 - lat1) * Math.PI / 180;
        var dlng = (lng2 - lng1) * Math.PI / 180;
        var a = Math.sin(dlat / 2) * Math.sin(dlat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dlng / 2) * Math.sin(dlng / 2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    function getStoredOrders() {
        try {
            var raw = localStorage.getItem(ORDERS_KEY);
            return raw ? JSON.parse(raw) : [];
        } catch (e) { return []; }
    }
    function setStoredOrders(arr) {
        localStorage.setItem(ORDERS_KEY, JSON.stringify(arr));
    }
    function getStoredCouriers() {
        try {
            var raw = localStorage.getItem(COURIERS_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch (e) { return null; }
    }
    function setStoredCouriers(arr) {
        localStorage.setItem(COURIERS_KEY, JSON.stringify(arr));
    }
    function normalizePhone(phone) {
        if (!phone) return '';
        var s = String(phone).replace(/\D/g, '');
        if (s.length === 12 && s.indexOf('57') === 0) return s.slice(2);
        return s;
    }
    function jsonResponse(obj, status) {
        return new Response(JSON.stringify(obj), {
            status: status || 200,
            headers: { 'Content-Type': 'application/json' }
        });
    }
    function errorResponse(detail, status) {
        return jsonResponse({ detail: detail }, status || 400);
    }

    function loadJson(path) {
        return REAL_FETCH(path).then(function (r) { return r.json(); });
    }

    window.fetch = function (input, init) {
        var url = typeof input === 'string' ? input : (input && input.url);
        if (!url || (url.indexOf('/api/') !== 0 && url.indexOf('/orders/') !== 0)) {
            return REAL_FETCH.apply(this, arguments);
        }
        init = init || {};
        var method = (init.method || 'GET').toUpperCase();

        if (url === '/api/delivery/businesses' && method === 'GET') {
            return loadJson(DATA_PREFIX + 'businesses.json').then(function (arr) {
                return jsonResponse({ businesses: Array.isArray(arr) ? arr : [] });
            }).catch(function () { return jsonResponse({ businesses: [] }); });
        }
        var m1 = url.match(/^\/api\/delivery\/businesses\/(\d+)\/products$/);
        if (m1 && method === 'GET') {
            var bid = parseInt(m1[1], 10);
            return loadJson(DATA_PREFIX + 'products.json').then(function (arr) {
                var list = (Array.isArray(arr) ? arr : []).filter(function (p) {
                    return p.business_id === bid && p.available !== false;
                });
                return jsonResponse({ products: list });
            }).catch(function () { return jsonResponse({ products: [] }); });
        }
        if (url === '/api/couriers/available' && method === 'GET') {
            return loadJson(DATA_PREFIX + 'couriers.json').then(function (arr) {
                var list = Array.isArray(arr) ? arr : [];
                var stored = getStoredCouriers();
                if (!stored || !stored.length) {
                    setStoredCouriers(JSON.parse(JSON.stringify(list)));
                    stored = list;
                } else list = stored;
                var available = list.filter(function (c) { return c.available !== false; });
                return jsonResponse({ couriers: available, count: available.length });
            }).catch(function () { return jsonResponse({ couriers: [], count: 0 }); });
        }
        if (url === '/api/couriers/' && method === 'GET') {
            return loadJson(DATA_PREFIX + 'couriers.json').then(function (arr) {
                var list = Array.isArray(arr) ? arr : [];
                var stored = getStoredCouriers();
                if (!stored || !stored.length) {
                    setStoredCouriers(JSON.parse(JSON.stringify(list)));
                    stored = list;
                } else list = stored;
                return jsonResponse({ couriers: list });
            }).catch(function () { return jsonResponse({ couriers: [] }); });
        }
        if (url.indexOf('/api/delivery/products/jumbo') === 0 && method === 'GET') {
            return loadJson(DATA_PREFIX + 'jumbo_products.json').then(function (arr) {
                var list = Array.isArray(arr) ? arr : [];
                var cats = [];
                list.forEach(function (p) {
                    var c = p.category || 'Sin categoría';
                    if (cats.indexOf(c) === -1) cats.push(c);
                });
                return jsonResponse({
                    products: list,
                    count: list.length,
                    source: 'Jumbo Colombia',
                    categories: cats,
                    category: null
                });
            }).catch(function () { return jsonResponse({ products: [], count: 0, source: 'Jumbo Colombia', categories: [], category: null }); });
        }
        if (url.indexOf('/api/delivery/orders') === 0 && method === 'GET') {
            var orders = getStoredOrders();
            var q = url.indexOf('?');
            if (q !== -1) {
                var params = new URLSearchParams(url.slice(q));
                var businessId = params.get('business_id');
                var courierId = params.get('courier_id');
                if (businessId) orders = orders.filter(function (o) { return o.business_id === parseInt(businessId, 10); });
                if (courierId) orders = orders.filter(function (o) { return o.courier_id === parseInt(courierId, 10); });
            }
            return Promise.resolve(jsonResponse({ orders: orders, count: orders.length }));
        }
        var m2 = url.match(/^\/api\/delivery\/orders\/by-phone\/(.+)$/);
        if (m2 && method === 'GET') {
            var phone = decodeURIComponent(m2[1]);
            var orders = getStoredOrders().filter(function (o) {
                return normalizePhone(o.customer_phone) === normalizePhone(phone);
            });
            orders.sort(function (a, b) { return (b.created_at || '').localeCompare(a.created_at || ''); });
            return Promise.resolve(jsonResponse({ orders: orders, count: orders.length }));
        }
        var m3 = url.match(/^\/api\/delivery\/orders\/(\d+)$/);
        if (m3 && method === 'GET') {
            var oid = parseInt(m3[1], 10);
            var orders = getStoredOrders();
            var order = orders.filter(function (o) { return o.id === oid; })[0];
            if (!order) return Promise.resolve(errorResponse('Pedido no encontrado', 404));
            return Promise.resolve(jsonResponse({ order: order }));
        }
        var m4 = url.match(/^\/api\/delivery\/orders\/(\d+)\/status$/);
        if (m4 && method === 'PATCH') {
            var oid2 = parseInt(m4[1], 10);
            var body = (init.body && typeof init.body === 'string') ? JSON.parse(init.body) : {};
            var orders = getStoredOrders();
            var idx = orders.findIndex(function (o) { return o.id === oid2; });
            if (idx === -1) return Promise.resolve(errorResponse('Pedido no encontrado', 404));
            var order = orders[idx];
            var oldStatus = order.status;
            var newStatus = body.status;
            var valid = ['pendiente', 'preparando', 'en_camino', 'entregado', 'cancelado'];
            if (valid.indexOf(newStatus) === -1) return Promise.resolve(errorResponse('Estado inválido. Válidos: ' + valid.join(', '), 400));
            order.status = newStatus;
            function applyStatusAndSave() {
                if (newStatus === 'en_camino' && !order.delivery_person) {
                    var names = ['Carlos', 'María', 'Pedro', 'Ana'];
                    order.delivery_person = names[oid2 % names.length];
                    order.courier_phone = '+57 300 ' + (1000000 + oid2);
                }
                if (!order.status_history) order.status_history = [];
                order.status_history.push({ status: newStatus, timestamp: new Date().toISOString() });
                order.updated_at = new Date().toISOString();
                setStoredOrders(orders);
                return jsonResponse({ order: order, message: "Estado actualizado de '" + oldStatus + "' a '" + newStatus + "'" });
            }
            if (newStatus === 'en_camino' && body.courier_id) {
                var couriers = getStoredCouriers();
                var loadC = (couriers && couriers.length) ? Promise.resolve(couriers) : loadJson(DATA_PREFIX + 'couriers.json').then(function (arr) {
                    var list = Array.isArray(arr) ? arr : [];
                    if (!getStoredCouriers() || !getStoredCouriers().length) setStoredCouriers(JSON.parse(JSON.stringify(list)));
                    return getStoredCouriers() || list;
                });
                return loadC.then(function (list) {
                    var c = (list || []).filter(function (x) { return x.id === body.courier_id; })[0];
                    if (c) {
                        order.courier_id = c.id;
                        order.delivery_person = c.name || '';
                        order.courier_phone = c.phone || '';
                    }
                    return applyStatusAndSave();
                });
            }
            return Promise.resolve(applyStatusAndSave());
        }
        if (url === '/api/delivery/orders' && method === 'POST') {
            var payload = (init.body && typeof init.body === 'string') ? JSON.parse(init.body) : {};
            return Promise.all([
                loadJson(DATA_PREFIX + 'businesses.json'),
                loadJson(DATA_PREFIX + 'products.json'),
                loadJson(DATA_PREFIX + 'jumbo_products.json')
            ]).then(function (res) {
                var businesses = res[0] || [];
                var products = (res[1] || []).concat(res[2] || []);
                var business = businesses.filter(function (b) { return b.id === payload.business_id; })[0];
                if (!business) return errorResponse('Negocio no encontrado', 404);
                var total = 0, orderProducts = [];
                (payload.products || []).forEach(function (item) {
                    var p = products.filter(function (x) { return x.id === item.product_id; })[0];
                    if (!p) return;
                    if (p.available === false) return;
                    var qty = item.quantity || 1;
                    var notes = (item.notes || '').trim().slice(0, 500);
                    var subtotal = p.price * qty;
                    total += subtotal;
                    orderProducts.push({
                        product_id: p.id,
                        product_name: p.name,
                        quantity: qty,
                        unit_price: p.price,
                        subtotal: subtotal,
                        notes: notes
                    });
                });
                if (!orderProducts.length) return errorResponse('El pedido debe contener al menos un producto', 400);
                var lat = payload.customer_lat, lng = payload.customer_lng;
                if (lat < 6 || lat > 6.5 || lng < -75.8 || lng > -75.4) return errorResponse('Coordenadas fuera del rango válido para Medellín', 400);
                var tipAmount = Math.max(0, parseInt(payload.tip_amount, 10) || 0);
                total += tipAmount;
                var dist = haversine(business.latitude, business.longitude, lat, lng);
                var eta = (business.delivery_time || 30) + Math.round(dist * 2);
                var orders = getStoredOrders();
                var newId = orders.length ? Math.max.apply(null, orders.map(function (o) { return o.id; })) + 1 : 1;
                var newOrder = {
                    id: newId,
                    customer_name: payload.customer_name,
                    customer_phone: payload.customer_phone,
                    customer_address: payload.customer_address,
                    customer_lat: lat,
                    customer_lng: lng,
                    business_id: business.id,
                    business_name: business.name,
                    business_lat: business.latitude,
                    business_lng: business.longitude,
                    products: orderProducts,
                    total: total,
                    distance_km: Math.round(dist * 100) / 100,
                    estimated_time: eta,
                    payment_method: payload.payment_method || 'efectivo',
                    tip_amount: tipAmount,
                    payment_status: 'pendiente',
                    status: 'pendiente',
                    delivery_person: null,
                    courier_phone: null,
                    created_at: new Date().toISOString(),
                    status_history: [{ status: 'pendiente', timestamp: new Date().toISOString() }]
                };
                orders.push(newOrder);
                setStoredOrders(orders);
                return jsonResponse({ order: newOrder, message: 'Pedido creado exitosamente' });
            }).catch(function (err) {
                return errorResponse(err.message || 'Error al crear pedido', 500);
            });
        }
        var m5 = url.match(/^\/api\/couriers\/(\d+)\/assign-order\/(\d+)$/);
        if (m5 && method === 'POST') {
            var cid = parseInt(m5[1], 10), oid3 = parseInt(m5[2], 10);
            return loadJson(DATA_PREFIX + 'couriers.json').then(function (arr) {
                var couriers = getStoredCouriers();
                if (!couriers || !couriers.length) couriers = JSON.parse(JSON.stringify(arr || []));
                setStoredCouriers(couriers);
                var orders = getStoredOrders();
                var courier = couriers.filter(function (c) { return c.id === cid; })[0];
                if (!courier) return errorResponse('Repartidor no encontrado', 404);
                if (courier.available === false) return errorResponse('El repartidor no está disponible', 400);
                var order = orders.filter(function (o) { return o.id === oid3; })[0];
                if (!order) return errorResponse('Pedido no encontrado', 404);
                if (['pendiente', 'preparando'].indexOf(order.status) === -1) return errorResponse('El pedido no puede ser asignado. Estado actual: ' + order.status, 400);
                order.courier_id = cid;
                order.courier_name = courier.name;
                order.courier_phone = courier.phone;
                order.status = 'en_camino';
                courier.available = false;
                courier.current_order_id = oid3;
                setStoredOrders(orders);
                setStoredCouriers(couriers);
                return jsonResponse({ message: 'Pedido ' + oid3 + ' asignado a ' + courier.name, order: order, courier: courier });
            });
        }
        var m6 = url.match(/^\/api\/couriers\/(\d+)\/complete-order\/(\d+)$/);
        if (m6 && method === 'POST') {
            var cid2 = parseInt(m6[1], 10), oid4 = parseInt(m6[2], 10);
            var couriers = getStoredCouriers();
            if (!couriers || !couriers.length) {
                return loadJson(DATA_PREFIX + 'couriers.json').then(function (arr) {
                    setStoredCouriers(JSON.parse(JSON.stringify(arr || [])));
                    return handleComplete();
                });
            }
            function handleComplete() {
                var couriers2 = getStoredCouriers();
                var orders = getStoredOrders();
                var courier = couriers2.filter(function (c) { return c.id === cid2; })[0];
                if (!courier) return errorResponse('Repartidor no encontrado', 404);
                var order = orders.filter(function (o) { return o.id === oid4; })[0];
                if (!order) return errorResponse('Pedido no encontrado', 404);
                if (order.courier_id !== cid2) return errorResponse('Este pedido no está asignado a este repartidor', 400);
                order.status = 'entregado';
                courier.available = true;
                courier.current_order_id = null;
                setStoredOrders(orders);
                setStoredCouriers(couriers2);
                return jsonResponse({ message: 'Pedido ' + oid4 + ' marcado como entregado', order: order, courier: courier });
            }
            return Promise.resolve(handleComplete());
        }
        if (url === '/orders/pay' && method === 'POST') {
            var payBody = (init.body && typeof init.body === 'string') ? JSON.parse(init.body) : {};
            var orders = getStoredOrders();
            var order = orders.filter(function (o) { return o.id === payBody.order_id; })[0];
            if (!order) return Promise.resolve(errorResponse('Pedido no encontrado', 404));
            if (order.payment_status === 'pagado') return Promise.resolve(errorResponse('El pedido ya está pagado', 400));
            var pm = payBody.payment_method || 'efectivo';
            if (['efectivo', 'tarjeta'].indexOf(pm) === -1) return Promise.resolve(errorResponse('Método de pago inválido. Válidos: efectivo, tarjeta', 400));
            if (pm === 'tarjeta') {
                var card = (payBody.card_number || '').replace(/\s/g, '').replace(/-/g, '');
                if (card.length < 13 || card.length > 19 || !/^\d+$/.test(card)) return Promise.resolve(errorResponse('Número de tarjeta inválido. Debe tener entre 13 y 19 dígitos', 400));
                if (!(payBody.card_holder || '').trim() || (payBody.card_holder || '').trim().length < 3) return Promise.resolve(errorResponse('Nombre del titular requerido (mínimo 3 caracteres)', 400));
                var cvv = String(payBody.cvv || '');
                if (cvv.length !== 3 || !/^\d+$/.test(cvv)) return Promise.resolve(errorResponse('CVV inválido. Debe ser un número de 3 dígitos', 400));
            }
            order.payment_method = pm;
            order.payment_status = pm === 'tarjeta' ? 'pagado' : 'pendiente';
            setStoredOrders(orders);
            var paymentRecord = {
                id: 1,
                order_id: order.id,
                amount: order.total,
                tip_amount: order.tip_amount || 0,
                payment_method: pm,
                status: order.payment_status,
                created_at: new Date().toISOString()
            };
            var msg = pm === 'tarjeta' ? 'Pago con tarjeta procesado exitosamente' : 'Pago en efectivo registrado. Se cobrará al momento de la entrega.';
            return Promise.resolve(jsonResponse({ payment: paymentRecord, message: msg, order: order }));
        }

        return REAL_FETCH.apply(this, arguments);
    };
})();
