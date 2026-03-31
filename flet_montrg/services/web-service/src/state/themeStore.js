import { writable } from 'svelte/store';

const THEME_KEY = 'felt-montrg-theme';

function getStored() {
  if (typeof window === 'undefined') return 'dark';
  return localStorage.getItem(THEME_KEY) || 'dark';
}

function applyTheme(value) {
  if (typeof document !== 'undefined') {
    document.documentElement.setAttribute('data-theme', value);
  }
}

function createThemeStore() {
  const stored = getStored();
  applyTheme(stored);
  const { subscribe, set, update } = writable(stored);
  return {
    subscribe,
    set: (value) => {
      applyTheme(value);
      if (typeof localStorage !== 'undefined') localStorage.setItem(THEME_KEY, value);
      set(value);
    },
    toggle: () => {
      update((v) => {
        const next = v === 'light' ? 'dark' : 'light';
        applyTheme(next);
        if (typeof localStorage !== 'undefined') localStorage.setItem(THEME_KEY, next);
        return next;
      });
    },
  };
}

export const theme = createThemeStore();
