/**
 * API client for integrated-swagger-service.
 */
import { API_BASE } from '../config/config.js';
import { availableServices, error, loading, refreshTrigger } from '../state/appStore.js';

const SERVICES_URL = `${API_BASE}/api/v1/swagger/services`;
const REFRESH_URL = `${API_BASE}/api/v1/swagger/refresh`;

export async function loadServices() {
  try {
    const res = await fetch(SERVICES_URL);
    const contentType = res.headers.get('content-type') || '';
    const text = await res.text();
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${text.slice(0, 200)}`);
    }
    if (!contentType.includes('application/json')) {
      throw new Error(`Expected JSON but got ${contentType}. URL: ${SERVICES_URL}`);
    }
    const data = JSON.parse(text);
    availableServices.set(data.services ?? {});
    error.set('');
    return data.services ?? {};
  } catch (e) {
    const msg = e?.message ? String(e.message) : String(e);
    error.set(`Failed to load services: ${msg} (API: ${SERVICES_URL})`);
    availableServices.set({});
    return {};
  }
}

export async function refreshSpecs() {
  error.set('');
  loading.set(true);
  try {
    const res = await fetch(REFRESH_URL, { method: 'POST' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const services = await loadServices();
    refreshTrigger.update((n) => n + 1);
    return services;
  } catch (e) {
    const msg = e?.message ? String(e.message) : String(e);
    error.set(`Failed to refresh: ${msg}`);
    throw e;
  } finally {
    loading.set(false);
  }
}
