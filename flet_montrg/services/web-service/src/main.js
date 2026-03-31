import './styles/theme.css';
import App from './App.svelte';
import { view } from './state/appStore.js';
import { loadServices } from './api/index.js';

const app = new App({ target: document.getElementById('app') });

function syncViewFromHash() {
  const hash = (window.location.hash || '#').trim().toLowerCase();
  const seg = hash.replace(/^#\/?/, '').split('/')[0] || '';
  // Swagger UI deepLinking rewrites the hash to #/paths/..., #/operations/..., etc.
  // after Try it out / Execute. The first segment is no longer "swagger", so we must
  // treat any #/... fragment as staying on the Swagger page; otherwise Svelte unmounts
  // SwaggerView and the whole UI disappears.
  const isSwaggerDeepLink = hash.startsWith('#/');
  const isSwagger =
    seg === 'swagger' || hash.includes('swagger') || isSwaggerDeepLink;
  view.set(isSwagger ? 'swagger' : 'overview');
}

syncViewFromHash();
window.addEventListener('hashchange', syncViewFromHash);
window.addEventListener('popstate', syncViewFromHash);

loadServices().then(syncViewFromHash);

export default app;
