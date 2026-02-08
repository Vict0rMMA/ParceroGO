/**
 * Imágenes de productos por nombre (Unsplash): foto según nombre del producto.
 * Leche → leche, Pizza → pizza, etc.
 */
(function () {
    var BASE_URL = 'https://images.unsplash.com/photo-';
    var QUERY = '?w=400&h=300&fit=crop';

    var BY_NAME = {
        'leche': '1563636619-914057cff423', 'huevos': '1582722872445-44dc5f7e3c8f', 'queso': '1486297678162-eb2a19b0a32d',
        'pan de bono': '1509440159596-0249088772ff', 'almojábana': '1509440159596-0249088772ff', 'pandebono': '1509440159596-0249088772ff',
        'pan integral': '1558961363-fa8fdf82db35', 'rosca': '1509440159596-0249088772ff', 'bandeja paisa': '1546069901-ba9599a7e63c',
        'sancocho': '1547592166-23ac45744acd', 'hamburguesa': '1568901346375-23c9450c58cd', 'pizza': '1513104890138-7c749659a591',
        'pizza margherita': '1513104890138-7c749659a591', 'pizza pepperoni': '1628840042765-356cda07504e', 'pizza familiar': '1565299624946-b28f40a0ae38',
        'pizza cuatro quesos': '1513104890138-7c749659a591', 'pan tajado': '1558961363-fa8fdf82db35', 'perro caliente': '1568901346375-23c9450c58cd',
        'empanadas': '1626700051175-6818013e1d4f', 'arroz': '1586201375761-83865001e31c', 'aceite': '1474979266404-7eaacbcd87c5',
        'azúcar': '1587049352846-4a222e784d38', 'sal': '1587049352846-4a222e784d38', 'frijoles': '1586201375761-83865001e31c',
        'acetaminofén': '1584308666744-24d5c474f2ae', 'ibuprofeno': '1584308666744-24d5c474f2ae', 'alcohol': '1584308666744-24d5c474f2ae',
        'vendas': '1556228578-0d85b1a4d571', 'jabón': '1556228578-0d85b1a4d571', 'café': '1517487881594-2787fef5ebf7',
        'cappuccino': '1572442388796-11668a67e53d', 'latte': '1461023058943-07fcbe16d735', 'té': '1556679343-c7306c1976bc',
        'pastel': '1578985545062-69928b1d9587', 'yogurt': '1488477181946-6428a0291777', 'mantequilla': '1585338927000-1c787b17eb5e',
        'alimento para perro': '1601758228041-f3b2795255f1', 'alimento para gato': '1601758228041-f3b2795255f1',
        'juguete': '1601758228041-f3b2795255f1', 'correa': '1601758228041-f3b2795255f1', 'shampoo para mascotas': '1601758228041-f3b2795255f1',
        'cama para perro': '1601758228041-f3b2795255f1', 'plato comedero': '1601758228041-f3b2795255f1', 'collar': '1601758228041-f3b2795255f1',
        'snacks para perro': '1601758228041-f3b2795255f1', 'arenero': '1601758228041-f3b2795255f1', 'pasta': '1621996346565-e3dbc646d9a9',
        'chorizo': '1603123853887-a92fafb7809f', 'alitas': '1626082927389-6cd097cdc6ec', 'nachos': '1513456852971-30c0b8199d4d',
        'papas': '1573080496219-bb080dd4f877', 'arepa': '1603123853887-a92fafb7809f'
    };

    window.getProductImageUrlByName = function (productName) {
        if (!productName || typeof productName !== 'string') return '';
        var name = productName.toLowerCase().trim();
        for (var key in BY_NAME) {
            if (name.indexOf(key) !== -1) return BASE_URL + BY_NAME[key] + QUERY;
        }
        return '';
    };
})();
