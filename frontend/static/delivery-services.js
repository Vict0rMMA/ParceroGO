(function (global) {
    'use strict';

    class ApiService {
        constructor(baseUrl = '') {
            this.baseUrl = baseUrl;
        }

        get(path) {
            return fetch(this.baseUrl + path).then(function (r) {
                if (!r.ok) throw new Error('HTTP ' + r.status);
                return r.json();
            });
        }

        post(path, body) {
            return fetch(this.baseUrl + path, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            }).then(function (r) {
                if (!r.ok) throw new Error('HTTP ' + r.status);
                return r.json();
            });
        }

        getBusinesses() {
            return this.get('/api/delivery/businesses');
        }

        getBusinessProducts(businessId) {
            return this.get('/api/delivery/businesses/' + businessId + '/products');
        }

        getAvailableCouriers() {
            return this.get('/api/couriers/available');
        }

        createOrder(orderPayload) {
            return this.post('/api/delivery/orders', orderPayload);
        }
    }

    class Cart {
        constructor() {
            this.items = [];
        }

        add(productId, name, price, quantity, notes) {
            quantity = quantity || 1;
            notes = notes || '';
            var existing = this.items.find(function (p) { return p.product_id === productId; });
            if (existing) {
                existing.quantity += quantity;
                existing.notes = notes || existing.notes;
            } else {
                this.items.push({
                    product_id: productId,
                    name: name,
                    price: price,
                    quantity: quantity,
                    notes: notes,
                });
            }
        }

        removeAt(index) {
            this.items.splice(index, 1);
        }

        updateQuantity(index, delta) {
            var p = this.items[index];
            if (!p) return;
            p.quantity += delta;
            if (p.quantity <= 0) this.items.splice(index, 1);
        }

        getItems() {
            return this.items.slice();
        }

        getTotal() {
            return this.items.reduce(function (sum, p) { return sum + p.price * p.quantity; }, 0);
        }

        getTotalItems() {
            return this.items.reduce(function (sum, p) { return sum + p.quantity; }, 0);
        }

        clear() {
            this.items.length = 0;
        }

        isEmpty() {
            return this.items.length === 0;
        }
    }

    class MapService {
        constructor(containerId, center, zoom) {
            this.containerId = containerId;
            this.center = center || [6.2476, -75.5658];
            this.zoom = zoom || 13;
            this.map = null;
            this.businessMarkers = [];
            this.courierMarkers = [];
            this.businessIcon = null;
            this.courierIcon = null;
        }

        init() {
            if (typeof L === 'undefined') throw new Error('Leaflet (L) no cargado');
            this.map = L.map(this.containerId, { zoomControl: true, scrollWheelZoom: true, zoomControl: false })
                .setView(this.center, this.zoom);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO',
                subdomains: 'abcd',
                maxZoom: 20,
            }).addTo(this.map);
            L.control.zoom({ position: 'topright' }).addTo(this.map);
            L.control.scale({ position: 'bottomleft', metric: true, imperial: false }).addTo(this.map);
            return this.map;
        }

        setBusinessIcon(divIcon) {
            this.businessIcon = divIcon;
        }

        setCourierIcon(divIcon) {
            this.courierIcon = divIcon;
        }

        clearBusinessMarkers() {
            this.businessMarkers.forEach(function (m) { m.remove(); });
            this.businessMarkers.length = 0;
        }

        clearCourierMarkers() {
            this.courierMarkers.forEach(function (m) { m.remove(); });
            this.courierMarkers.length = 0;
        }

        addBusinessMarker(lat, lng, popupContent, onClick) {
            if (!this.map) return null;
            var icon = this.businessIcon || undefined;
            var marker = L.marker([lat, lng], icon ? { icon: icon } : {}).addTo(this.map);
            if (popupContent) marker.bindPopup(popupContent);
            if (onClick) marker.on('click', onClick);
            this.businessMarkers.push(marker);
            return marker;
        }

        addCourierMarker(lat, lng, popupContent) {
            if (!this.map) return null;
            var icon = this.courierIcon || undefined;
            var marker = L.marker([lat, lng], icon ? { icon: icon } : {}).addTo(this.map);
            if (popupContent) marker.bindPopup(popupContent);
            this.courierMarkers.push(marker);
            return marker;
        }

        getMap() {
            return this.map;
        }
    }

    global.ParceroGO = global.ParceroGO || {};
    global.ParceroGO.ApiService = ApiService;
    global.ParceroGO.Cart = Cart;
    global.ParceroGO.MapService = MapService;

})(typeof window !== 'undefined' ? window : this);
