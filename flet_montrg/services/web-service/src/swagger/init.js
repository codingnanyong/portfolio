/**
 * Swagger UI initialization using global SwaggerUIBundle (loaded via script in index.html).
 * BaseLayout: 상단 URL 입력/Explore 바 없이 스펙 로드 시 문서만 바로 표시.
 */
import { API_BASE } from '../config/config.js';
import { createRequestInterceptor } from './requestInterceptor.js';
import { applyServiceDescriptions } from '../config/labels.js';

export function initSwaggerUI(specUrl, _title, onComplete, onFailure, localeKey = 'en') {
  const SwaggerUIBundle = window.SwaggerUIBundle;
  if (!SwaggerUIBundle) {
    const err = new Error('Swagger UI not loaded');
    onFailure?.(err);
    return null;
  }

  const base = API_BASE || (typeof window !== 'undefined' ? window.location.origin : '');
  const url = specUrl.startsWith('http') ? specUrl : base + (specUrl.startsWith('/') ? specUrl : '/' + specUrl);
  const interceptor = createRequestInterceptor();

  function hideInfoAndAuth() {
    const root = document.getElementById('swagger-ui');
    if (!root) return;
    const sel = [
      '.information-container', '.info', '.auth-wrapper', '.auth-container',
      '.topbar', '.topbar-wrapper', '.download-url-wrapper', '.scheme-container'
    ];
    sel.forEach((s) => {
      root.querySelectorAll(s).forEach((el) => {
        el.style.setProperty('display', 'none', 'important');
        el.style.setProperty('visibility', 'hidden', 'important');
        el.style.setProperty('height', '0', 'important');
        el.style.setProperty('overflow', 'hidden', 'important');
      });
    });
    root.querySelectorAll('.wrapper, section').forEach((el) => {
      if (el.querySelector('.auth-wrapper, .auth-container, .information-container, .info') && !el.querySelector('.opblock-tag-section')) {
        el.style.setProperty('display', 'none', 'important');
      }
    });
  }

  const ui = SwaggerUIBundle({
    url,
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [SwaggerUIBundle.presets.apis],
    layout: 'BaseLayout',
    displayOperationId: false,
    showExtensions: false,
    showCommonExtensions: false,
    tryItOutEnabled: true,
    docExpansion: 'none',
    requestInterceptor: interceptor,
    onComplete: () => {
      hideInfoAndAuth();
      setTimeout(hideInfoAndAuth, 100);
      setTimeout(() => applyServiceDescriptions(localeKey), 150);
      onComplete?.();
    },
    onFailure: (err) => onFailure?.(err),
  });

  return ui;
}
