import { writable, derived } from 'svelte/store';
import { filterServices } from '../utils/serviceHelpers.js';

export const availableServices = writable({});
export const selectedService = writable('integrated');
export const searchQuery = writable('');
export const view = writable('overview'); // 'overview' | 'swagger'
export const loading = writable(false);
export const error = writable('');
export const swaggerUI = writable(null);
/** Incremented on refresh success; SwaggerView reacts to force reload */
export const refreshTrigger = writable(0);

export const filteredServiceNames = derived(
  [availableServices, searchQuery],
  ([$availableServices, $searchQuery]) => filterServices($availableServices, $searchQuery)
);

export const serviceCount = derived(availableServices, ($s) => Object.keys($s).length);
