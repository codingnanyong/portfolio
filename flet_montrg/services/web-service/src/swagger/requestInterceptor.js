/**
 * Swagger UI: /api/v1/... 요청을 통합 게이트웨이로 그대로 보냄 (동일 출처 또는 API_BASE).
 * URL에 서비스명을 넣지 않으며 /api/svc/ 프리픽스로 바꾸지 않음.
 */
import { API_BASE } from '../config/config.js';

export function createRequestInterceptor() {
  return function interceptor(request) {
    if (request.url.includes('/swagger/')) return request;
    if (request.url.includes('openapi.json') || request.url.includes('/spec')) return request;
    if (request.url.includes('/api/svc/')) return request;

    let pathnameSearch = request.url;
    if (request.url.startsWith('http')) {
      const u = new URL(request.url);
      pathnameSearch = u.pathname + u.search;
    } else if (!pathnameSearch.startsWith('/')) {
      pathnameSearch = '/' + pathnameSearch;
    }

    const base = (API_BASE || (typeof window !== 'undefined' ? window.location.origin : '')).replace(
      /\/$/,
      '',
    );
    request.url = base ? `${base}${pathnameSearch}` : pathnameSearch;
    return request;
  };
}
