<script>
  import { loading, error, searchQuery, filteredServiceNames, availableServices, serviceCount } from '../state/appStore.js';
  import { locale } from '../state/localeStore.js';
  import { getLabels, getServiceLabel } from '../config/labels.js';
  import { toDisplayName, serviceCardEmoji } from '../utils/serviceHelpers.js';
  import { refreshSpecs } from '../api/index.js';
  import { APP_NAME } from '../config/constants.js';

  $: L = getLabels($locale);

  export let onSelectService = (_name) => {};

  function handleQuickCard(e, service) {
    e.preventDefault();
    e.stopPropagation();
    onSelectService(service || 'integrated');
  }

  function handleCardClick(e, name) {
    e.preventDefault();
    e.stopPropagation();
    const spec = $availableServices[name];
    if (spec && spec.is_available) onSelectService(name);
  }
</script>

<div class="max-w-[min(1200px,100%)]">
  <div class="mb-8">
    <h1 class="m-0 mb-1 text-[1.625rem] font-bold tracking-tight" style="color: var(--text-primary); letter-spacing: -0.02em;">{APP_NAME} API Services</h1>
    <p class="m-0 mb-1 text-[0.95rem] leading-normal" style="color: var(--text-secondary);">
      {APP_NAME} {L.apiGatewayDesc}
    </p>
    <p class="m-0 text-[0.85rem]" style="color: var(--text-tertiary);">{$serviceCount} {L.servicesIntegrated}</p>
  </div>

  {#if $loading}
    <p class="text-[0.9rem] mb-4" style="color: var(--text-secondary);">{L.loadingServices}</p>
  {/if}
  {#if $error}
    <p class="font-medium mb-4 text-red-600">{$error}</p>
  {/if}

  <section class="mb-10">
    <h2 class="m-0 mb-4 text-[1.125rem] font-bold tracking-tight" style="color: var(--text-primary);">{L.quickLinks}</h2>
    <div class="grid gap-4 grid-cols-[repeat(auto-fill,minmax(140px,1fr))]">
      <a
        href="#swagger"
        class="flex flex-col items-center py-4 px-3 rounded-xl no-underline text-inherit transition-all border min-h-0 border-l-4 hover:-translate-y-0.5 hover:border-[var(--accent)] hover:shadow-[var(--shadow-card-hover)]"
        style="background: var(--bg-card); border-color: var(--border); box-shadow: var(--shadow-card); border-left-color: var(--accent);"
        on:click={(e) => handleQuickCard(e, 'integrated')}
      >
        <span class="text-3xl leading-none mb-2">📄</span>
        <div class="flex flex-col items-center gap-0.5 text-center">
          <span class="text-[0.8rem] font-medium leading-snug" style="color: var(--text-primary);">{L.swaggerUI}</span>
          <span class="text-[0.7rem] leading-snug" style="color: var(--text-tertiary);">{L.swaggerUiCardDesc}</span>
        </div>
      </a>
    </div>
  </section>

  <section>
    <div class="flex flex-wrap items-start justify-between gap-4 mb-4">
      <div>
        <h2 class="m-0 mb-1 text-[1.125rem] font-bold tracking-tight" style="color: var(--text-primary);">{L.tableApis}</h2>
        <p class="m-0 mb-4 text-[0.9rem] leading-normal" style="color: var(--text-secondary);">{L.tableApisDesc}</p>
      </div>
      <div class="flex items-center gap-2">
        <div class="flex items-center min-w-[200px] py-2 px-3 rounded-lg border" style="background: var(--bg-secondary); border-color: var(--border);">
          <span class="mr-2 text-base opacity-70">🔍</span>
          <input
            type="search"
            class="flex-1 min-w-0 border-0 bg-transparent text-[0.9rem] outline-none"
            style="color: var(--text-primary);"
            placeholder={L.searchPlaceholder}
            bind:value={$searchQuery}
          />
        </div>
        <button
          type="button"
          class="py-2 px-3 rounded-lg border flex items-center justify-center transition-colors"
          style="background: var(--bg-secondary); border-color: var(--border); color: var(--text-primary);"
          on:click={refreshSpecs}
          title={L.refresh}
          aria-label={L.refresh}
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M23 4v6h-6M1 20v-6h6" />
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
          </svg>
        </button>
      </div>
    </div>

    {#if $filteredServiceNames.length === 0}
      <p class="py-8 text-center text-[0.95rem]" style="color: var(--text-tertiary);">{L.noServices}</p>
    {:else}
      <div class="grid gap-4 grid-cols-[repeat(auto-fill,minmax(140px,1fr))]">
        {#each $filteredServiceNames as name}
          {@const spec = $availableServices[name]}
          {@const label = getServiceLabel(name, $locale, toDisplayName(name, spec))}
          {@const emoji = serviceCardEmoji(name)}
          <button
            type="button"
            class="flex flex-col items-center py-4 px-3 rounded-xl border text-left w-full transition-all cursor-pointer hover:-translate-y-0.5 hover:border-[var(--accent)] hover:shadow-[var(--shadow-card-hover)]"
            style="background: var(--bg-card); border-color: var(--border); box-shadow: var(--shadow-card); color: inherit;"
            on:click={(e) => handleCardClick(e, name)}
          >
            <span class="text-3xl leading-none mb-2">{emoji}</span>
            <div class="flex flex-col items-center gap-0.5 text-center">
              <span class="text-[0.8rem] font-medium leading-snug" style="color: var(--text-primary);">{label}</span>
            </div>
          </button>
        {/each}
      </div>
    {/if}
  </section>
</div>
