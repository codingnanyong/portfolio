import { writable } from 'svelte/store';

const LOCALE_KEY = 'felt-montrg-locale';

function getStored() {
  if (typeof window === 'undefined') return 'en';
  return localStorage.getItem(LOCALE_KEY) || 'en';
}

function createLocaleStore() {
  const stored = getStored();
  const { subscribe, set, update } = writable(stored);
  return {
    subscribe,
    set: (value) => {
      if (typeof localStorage !== 'undefined') localStorage.setItem(LOCALE_KEY, value);
      set(value);
    },
    toggle: () => {
      update((v) => {
        const next = v === 'ko' ? 'en' : 'ko';
        if (typeof localStorage !== 'undefined') localStorage.setItem(LOCALE_KEY, next);
        return next;
      });
    },
  };
}

export const locale = createLocaleStore();
