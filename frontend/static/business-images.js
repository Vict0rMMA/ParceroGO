(function () {
    var SIZE = '80';
    var BASE_URL = 'https://images.unsplash.com/photo-';
    var QUERY = '?w=' + SIZE + '&h=' + SIZE + '&fit=crop';

    var BY_CATEGORY = {
        'Restaurante': ['1546069901-ba9599a7e63c', '1565299624946-b28f40a0ae38', '1547592166-23ac45744acd', '1414237427423-fa1b3c6d32a2', '1517248135467-4c7edcad34c4'],
        'Comidas Rápidas': ['1568901346375-23c9450c58cd', '1626082927389-6cd097cdc6ec', '1573080496219-bb080dd4f877', '1603123853887-a92fafb7809f', '1626082927389-6cd097cdc6ec'],
        'Pizzería': ['1513104890138-7c749659a591', '1628840042765-356cda07504e', '1565299624946-b28f40a0ae38', '1574071318508-1cdbab80d002', '1571997478779-2adcbbe9ab2f'],
        'Farmacia': ['1584308666744-24d5c474f2ae', '1556228578-0d85b1a4d571', '1587859151263-8645b5c92b5b'],
        'Panadería': ['1509440159596-0249088772ff', '1558961363-fa8fdf82db35', '1608198399988-2febe69dd3eb', '1509440159596-0249088772ff'],
        'Supermercado': ['1604716313928-4e291d30d0b2', '1586201375761-83865001e31c', '1563636619-914057cff423', '1578916171725-0c5c2b463d26', '1582735689369-4fe89db711d9'],
        'Tienda de Abarrotes': ['1586201375761-83865001e31c', '1582735689369-4fe89db711d9', '1604716313928-4e291d30d0b2', '1621996346565-e3dbc646d9a9', '1559056199-641a0ac8b55c'],
        'Cafetería': ['1517487881594-2787fef5ebf7', '1572442388796-11668a67e53d', '1461023058943-07fcbe16d735', '1556679343-c7306c1976bc', '1578985545062-69928b1d9587'],
        'Veterinaria': ['1601758228041-f3b2795255f1', '1587300002278-2d4b4a0a9a8a', '1573869943247-1dc2f6d36c6e'],
        'Tienda de Mascotas': ['1601758228041-f3b2795255f1', '1587300002278-2d4b4a0a9a8a', '1573869943247-1dc2f6d36c6e']
    };
    var DEFAULT_IMAGES = ['1604716313928-4e291d30d0b2', '1586201375761-83865001e31c', '1546069901-ba9599a7e63c'];

    window.getBusinessImageUrlByCategory = function (category, businessId) {
        var list = BY_CATEGORY[category] || DEFAULT_IMAGES;
        var idx = (Math.abs(Number(businessId) || 0) % list.length);
        return BASE_URL + list[idx] + QUERY;
    };
})();
