import './styles/theme.css';
import App from './App.svelte';
import { view } from './state/appStore.js';
import { loadServices } from './api/index.js';

const app = new App({ target: document.getElementById('app') });

function syncViewFromHash() {
  const hash = (window.location.hash || '#').trim().toLowerCase();
  const seg = hash.replace(/^#\/?/, '').split('/')[0] || '';
  const isSwagger = seg === 'swagger' || hash.includes('swagger');
  view.set(isSwagger ? 'swagger' : 'overview');
}

syncViewFromHash();
window.addEventListener('hashchange', syncViewFromHash);
window.addEventListener('popstate', syncViewFromHash);

loadServices().then(syncViewFromHash);

export default app;
