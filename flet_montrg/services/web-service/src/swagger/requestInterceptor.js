/**
 * Swagger UI request interceptor to proxy /api/v1/... calls via integrated-swagger proxy.
 */
import { API_BASE, SERVICE_MAPPING } from '../config/config.js';

function extractServiceFromPath(path) {
  const segments = path.split('/').filter(Boolean);
  if (segments.length >= 3 && segments[0] === 'api' && segments[1] === 'v1') {
    const key = segments[2];
    return SERVICE_MAPPING[key] ?? key;
  }
  return null;
}

export function createRequestInterceptor() {
  return function interceptor(request) {
    if (request.url.includes('/swagger/')) return request;
    if (request.url.includes('openapi.json') || request.url.includes('/spec')) return request;
    if (request.url.startsWith(API_BASE + '/api/proxy/') || request.url.includes('/api/proxy/')) return request;

    let pathToConvert = request.url;
    if (request.url.startsWith('http')) {
      const u = new URL(request.url);
      pathToConvert = u.pathname + u.search;
    } else if (!pathToConvert.startsWith('/')) {
      pathToConvert = '/' + pathToConvert;
    }
    const serviceName = extractServiceFromPath(pathToConvert);
    if (serviceName) {
      const pathOnly = pathToConvert.replace(/^\//, '');
      const base = API_BASE || (typeof window !== 'undefined' ? window.location.origin : '');
      request.url = `${base}/api/proxy/${serviceName}/${pathOnly}`;
    }
    return request;
  };
}
