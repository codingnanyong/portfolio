<script>
  import { view, selectedService, availableServices, loading, error, swaggerUI, refreshTrigger } from '../state/appStore.js';
  import { locale } from '../state/localeStore.js';
  import { getLabels, getServiceLabel, applyServiceDescriptions } from '../config/labels.js';
  import { toDisplayName } from '../utils/serviceHelpers.js';
  import { API_BASE } from '../config/config.js';
  import { initSwaggerUI } from '../swagger/init.js';

  $: L = getLabels($locale);

  $: serviceDisplayName = $selectedService === 'integrated'
    ? L.integratedShort
    : getServiceLabel($selectedService, $locale, toDisplayName($selectedService, $availableServices[$selectedService]));

  $: serviceNames = Object.keys($availableServices);

  function getSpecUrl(service) {
    const base = API_BASE || (typeof window !== 'undefined' ? window.location.origin : '');
    if (service === 'integrated') return base + '/openapi.json';
    return base + '/api/v1/swagger/services/' + service + '/spec';
  }

  function loadSwagger() {
    error.set('');
    loading.set(true);
    const prev = $swaggerUI;
    if (prev) {
      try { prev.getSystem().getActions().clear(); } catch (_) {}
    }
    const ui = initSwaggerUI(
      getSpecUrl($selectedService),
      serviceDisplayName,
      () => loading.set(false),
      (err) => {
        error.set(L.loadFailed + (err && err.message ? err.message : String(err)));
        loading.set(false);
      },
      $locale
    );
    swaggerUI.set(ui);
  }

  function handleServiceSelect(e) {
    selectedService.set(e.target.value);
  }

  function handleReloadClick() {
    // 강제로 refreshTrigger를 변경해 Swagger UI 전체를 재초기화
    refreshTrigger.update((n) => n + 1);
  }

  // locale 변경 시 Swagger UI 내 서비스 설명 문구 갱신
  $: if ($view === 'swagger' && !$loading && $locale) {
    setTimeout(() => applyServiceDescriptions($locale), 0);
  }

  $: if ($view === 'swagger' && $selectedService) {
    const _ = $refreshTrigger;
    // Defer so #swagger-ui exists in DOM before SwaggerUIBundle mounts
    setTimeout(() => loadSwagger(), 0);
  }
</script>

{#if $view === 'swagger'}
  <section id="swagger" class="max-w-[min(1200px,100%)]">
    {#if $error}
      <p class="font-medium mb-4 text-red-600">{$error}</p>
    {/if}
    {#if $loading}
      <p class="text-[0.9rem] mb-4" style="color: var(--text-secondary);">{L.loadingSpec}</p>
    {/if}

    <nav class="mb-3 text-[0.875rem]" style="color: var(--text-secondary);">
      <a href="#overview" style="color: var(--accent);">{L.overview}</a>
      <span class="mx-1">/</span>
      <span style="color: var(--text-primary);">{serviceDisplayName}</span>
    </nav>

    <div class="flex flex-wrap items-center gap-4 mb-4">
      <label class="flex items-center gap-2">
        <span class="text-sm font-medium" style="color: var(--text-secondary);">{L.service}</span>
        <select
          class="service-select rounded px-3 py-1.5 min-w-[220px] text-sm font-medium outline-none focus:ring-1 focus:ring-[var(--accent)]"
          style="background: var(--bg-secondary); border: 1px solid var(--border); color: var(--text-primary);"
          value={$selectedService}
          on:change={handleServiceSelect}
        >
          <option value="integrated">{L.integratedAll}</option>
          {#each serviceNames as name}
            {@const spec = $availableServices[name]}
            <option value={name} disabled={spec && !spec.is_available}>
              {spec && !spec.is_available ? '(unavailable) ' : ''}{getServiceLabel(name, $locale, toDisplayName(name, spec))} (v{spec?.version || '?'})
            </option>
          {/each}
        </select>
      </label>

      <button
        type="button"
        class="text-xs px-3 py-1.5 rounded border"
        style="border-color: var(--border); color: var(--text-secondary); background: var(--bg-secondary);"
        on:click={handleReloadClick}
      >
        {L.reloadSwagger || 'Reload'}
      </button>
    </div>

    <!-- 화면 하단에서도 바로 재로딩 가능 (Cancel 이후 Execute 미표시 등) -->
    <button
      type="button"
      class="fixed bottom-5 right-5 z-[60] text-xs px-3 py-2 rounded-full border shadow"
      style="border-color: var(--border); color: var(--text-primary); background: var(--bg-secondary); box-shadow: var(--shadow-card);"
      on:click={handleReloadClick}
      aria-label={L.reloadSwagger || 'Reload'}
      title={L.reloadSwagger || 'Reload'}
    >
      ⟳ {L.reloadSwagger || 'Reload'}
    </button>

    <div id="swagger-ui-anchor" class="mt-2">
      <div id="swagger-ui" style="--swagger-ui-font-size: 14px;"></div>
    </div>
  </section>
{/if}
