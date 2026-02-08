/**
 * Build estático para Vercel: copia frontend (templates + static) y data a una carpeta "out".
 * Rutas: / -> index.html, /delivery -> delivery/index.html, etc.
 * Uso: node scripts/build-vercel.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'out');
const FRONTEND = path.join(ROOT, 'frontend');
const TEMPLATES = path.join(FRONTEND, 'templates');
const STATIC = path.join(FRONTEND, 'static');
const DATA = path.join(ROOT, 'data');

const ROUTES = [
  { file: 'index.html', path: 'index.html' },
  { file: 'onboarding.html', path: 'onboarding/index.html' },
  { file: 'delivery.html', path: 'delivery/index.html' },
  { file: 'checkout.html', path: 'checkout/index.html' },
  { file: 'order.html', path: 'order/index.html' },
  { file: 'tracking.html', path: 'tracking/index.html' },
  { file: 'panel.html', path: 'panel/index.html' },
  { file: 'repartidor.html', path: 'repartidor/index.html' },
  { file: 'perfil.html', path: 'perfil/index.html' },
  { file: 'jumbo.html', path: 'jumbo/index.html' }
];

function mkdirp(dir) {
  if (!fs.existsSync(dir)) {
    mkdirp(path.dirname(dir));
    fs.mkdirSync(dir);
  }
}

function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  mkdirp(dest);
  fs.readdirSync(src).forEach(name => {
    const s = path.join(src, name);
    const d = path.join(dest, name);
    if (fs.statSync(s).isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  });
}

// Limpiar y crear out
if (fs.existsSync(OUT)) {
  fs.rmSync(OUT, { recursive: true });
}
mkdirp(OUT);

// Copiar static -> out/static
copyDir(STATIC, path.join(OUT, 'static'));
console.log('Copiado frontend/static -> out/static');

// Copiar data -> out/data (solo JSON necesarios para lectura)
const dataFiles = ['businesses.json', 'products.json', 'couriers.json', 'jumbo_products.json', 'config.json'];
mkdirp(path.join(OUT, 'data'));
dataFiles.forEach(name => {
  const src = path.join(DATA, name);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, path.join(OUT, 'data', name));
    console.log('Copiado data/' + name + ' -> out/data/');
  }
});

// Copiar cada template a su ruta
ROUTES.forEach(({ file, path: outPath }) => {
  const src = path.join(TEMPLATES, file);
  if (!fs.existsSync(src)) {
    console.warn('No existe:', src);
    return;
  }
  const destFile = path.join(OUT, outPath);
  mkdirp(path.dirname(destFile));
  fs.copyFileSync(src, destFile);
  console.log('Copiado ' + file + ' -> out/' + outPath);
});

console.log('\nBuild listo. Carpeta de salida: out/');
