/**
 * API base URL configuration.
 * 1) ?apiBase=URL 쿼리
 * 2) VITE_API_BASE 빌드 시
 * 3) 기본값: '' (same-origin, nginx가 /api → integrated-swagger 프록시)
 */
function getApiBase() {
  if (typeof window === 'undefined') return '';
  const match = /[?&]apiBase=([^&]*)/.exec(window.location.search);
  if (match) {
    const val = decodeURIComponent(match[1].replace(/\+/g, ' '));
    if (val !== undefined && val !== null) return val; // ?apiBase= 빈 값이면 same-origin
  }
  if (import.meta.env.VITE_API_BASE) return import.meta.env.VITE_API_BASE;
  return '';
}

export const API_BASE = getApiBase();

export const SERVICE_MAPPING = {
  aggregation: 'aggregation-service',
  location: 'location-service',
  realtime: 'realtime-service',
  thresholds: 'thresholds-service',
  alerts: 'alert-service',
  subscriptions: 'alert-subscription-service',
  notifications: 'alert-notification-service',
  mappings: 'sensor-threshold-mapping-service',
};
