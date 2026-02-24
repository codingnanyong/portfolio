<script>
  import { view, selectedService } from './state/appStore.js';
  import { theme } from './state/themeStore.js';
  import { locale } from './state/localeStore.js';
  import Sidebar from './layout/Sidebar.svelte';
  import Footer from './layout/Footer.svelte';
  import Overview from './pages/Overview.svelte';
  import SwaggerView from './pages/SwaggerView.svelte';

  function goToSwaggerIntegrated() {
    selectedService.set('integrated');
    view.set('swagger');
    window.location.hash = 'swagger';
  }

  function selectServiceAndOpenSwagger(name) {
    selectedService.set(name);
    view.set('swagger');
    window.location.hash = 'swagger';
  }
</script>

<div class="flex flex-col min-h-screen w-full">
  <div class="flex flex-1 min-h-0 min-w-0">
    <Sidebar onSelectService={selectServiceAndOpenSwagger} onNavSwaggerClick={goToSwaggerIntegrated} />

    <div class="flex-1 flex flex-col min-w-0" style="background: var(--bg-primary);">
  <header class="flex-shrink-0 flex justify-end items-center gap-2 min-h-[48px] py-0 px-9 mb-2">
    <button
      type="button"
      class="lang-toggle-btn px-2 py-1 rounded text-sm font-medium border cursor-pointer transition-opacity hover:opacity-100 opacity-90"
      style="background: transparent; color: var(--text-primary);"
      on:click={() => locale.toggle()}
      title={$locale === 'en' ? '한국어로 전환' : 'Switch to English'}
      aria-label="Toggle language"
    >{$locale === 'en' ? 'ENG' : '한'}</button>
    <button
      type="button"
      class="w-9 h-8 rounded-md border-0 cursor-pointer flex items-center justify-center text-sm font-semibold transition-opacity hover:opacity-100 opacity-90"
      style="background: transparent; color: var(--text-primary);"
      on:click={() => theme.toggle()}
      title={$theme === 'light' ? 'Dark mode' : 'Light mode'}
      aria-label="Toggle theme"
    >
      {#if $theme === 'light'}
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>
      {:else}
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
      {/if}
    </button>
  </header>

  <main class="flex-1 min-w-0 py-4 px-9 pb-7">
    {#if $view === 'overview'}
      <Overview onSelectService={selectServiceAndOpenSwagger} />
    {/if}
    <SwaggerView />
  </main>
    </div>
  </div>

  <Footer />
</div>
