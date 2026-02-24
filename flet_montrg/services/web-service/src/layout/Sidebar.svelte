<script>
  import { view, selectedService, availableServices } from '../state/appStore.js';
  import { locale } from '../state/localeStore.js';
  import { getLabels, getServiceLabel } from '../config/labels.js';
  import { toDisplayName, serviceCardEmoji } from '../utils/serviceHelpers.js';
  import { APP_NAME, APP_SUBTITLE } from '../config/constants.js';

  export let onSelectService = (_name) => {};
  export let onNavSwaggerClick = () => {};

  $: L = getLabels($locale);

  $: navOverviewActive = $view === 'overview';
  $: navSwaggerActive = $view === 'swagger' && $selectedService === 'integrated';
  $: serviceList = Object.keys($availableServices);

  function handleServiceClick(e, name) {
    e.preventDefault();
    const spec = $availableServices[name];
    if (spec && spec.is_available) onSelectService(name);
  }

  function navLinkClass(isActive) {
    return 'flex items-center justify-between py-2 px-3 my-0.5 rounded-md text-[0.9rem] transition-colors ' +
      (isActive ? 'font-semibold border-l-[3px] pl-[calc(0.75rem-3px)] -ml-px bg-[var(--accent-muted)] border-l-[var(--accent)]' : '');
  }
  function navLinkStyle(isActive) {
    return isActive ? 'color: var(--accent-active);' : 'color: var(--text-primary);';
  }
</script>

<aside
  class="flex flex-col flex-shrink-0 min-h-0 border-r"
  style="width: var(--sidebar-width); min-width: var(--sidebar-width); background: var(--bg-primary); border-color: var(--border);"
>
  <a href="#overview" class="flex items-center gap-3 py-6 px-5 border-b no-underline hover:no-underline" style="border-color: var(--border); color: inherit;">
    <span class="w-7 h-7 flex-shrink-0 flex items-center justify-center rounded-full overflow-hidden" style="background: var(--accent);" aria-hidden>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28" class="w-full h-full">
        <!-- 온도계 윤곽선: 흰색 -->
        <rect x="12" y="4" width="4" height="13" rx="2" fill="none" stroke="white" stroke-width="1.2"/>
        <circle cx="14" cy="19.5" r="2.2" fill="none" stroke="white" stroke-width="1.2"/>
        <!-- 수은주: 빨간색 -->
        <rect x="12.7" y="9" width="2.6" height="6" rx="0.4" fill="#e11d48"/>
        <circle cx="14" cy="19.5" r="1.2" fill="#e11d48"/>
      </svg>
    </span>
    <div class="min-w-0">
      <h1 class="m-0 text-[1.35rem] font-extrabold leading-tight tracking-tight" style="color: var(--text-primary); letter-spacing: -0.03em;">{APP_NAME}</h1>
      <span class="block mt-1 text-[0.8125rem] font-medium" style="color: var(--text-secondary);">{APP_SUBTITLE}</span>
    </div>
  </a>

  <nav class="flex flex-col flex-1 min-h-0 overflow-hidden py-4 px-2.5">
    <div class="flex-shrink-0 mb-4 py-2">
      <span class="block pb-2 mb-2 text-[0.6875rem] font-bold uppercase tracking-wider border-b" style="color: var(--text-secondary); border-color: var(--border);">{L.quickLinks}</span>
      <a
        href="#overview"
        class="{navLinkClass(navOverviewActive)} hover:bg-[var(--bg-tertiary)] flex items-center"
        style="{navLinkStyle(navOverviewActive)}"
      >
        <span class="flex-shrink-0 mr-2 text-base leading-none">📋</span>
        <span class="flex-1 min-w-0 truncate">{L.overview}</span>
        {#if navOverviewActive}<span class="flex-shrink-0 font-semibold" style="color: var(--accent-active);">›</span>{/if}
      </a>
      <a
        href="#swagger"
        class="{navLinkClass(navSwaggerActive)} hover:bg-[var(--bg-tertiary)] flex items-center"
        style="{navLinkStyle(navSwaggerActive)}"
        on:click|preventDefault={onNavSwaggerClick}
      >
        <span class="flex-shrink-0 mr-2 text-base leading-none">📄</span>
        <span class="flex-1 min-w-0 truncate">{L.swaggerUI}</span>
        {#if navSwaggerActive}<span class="flex-shrink-0 font-semibold" style="color: var(--accent-active);">›</span>{/if}
      </a>
    </div>

    <div class="flex flex-col flex-1 min-h-0 py-2 overflow-hidden">
      <span class="block pb-2 mb-2 text-[0.6875rem] font-bold uppercase tracking-wider border-b flex-shrink-0" style="color: var(--text-secondary); border-color: var(--border);">{L.tableApis}</span>
      <div class="serviceListScroll flex flex-col gap-px flex-1 min-h-0 overflow-y-auto mt-1">
        {#each serviceList as name}
          {@const spec = $availableServices[name]}
          {@const label = getServiceLabel(name, $locale, toDisplayName(name, spec))}
          {@const emoji = serviceCardEmoji(name)}
          {@const isActive = $view === 'swagger' && $selectedService === name}
          <a
            href="#swagger"
            data-service={name}
            class="{navLinkClass(isActive)} text-[0.875rem] hover:bg-[var(--bg-tertiary)] {spec && !spec.is_available ? 'opacity-50 cursor-not-allowed' : ''}"
            style="{navLinkStyle(isActive)}"
            class:pointer-events-none={spec && !spec.is_available}
            on:click={(e) => handleServiceClick(e, name)}
          >
            <span class="flex-shrink-0 mr-2 text-base leading-none">{emoji}</span>
            <span class="flex-1 min-w-0 truncate">{label}</span>
            {#if isActive}<span class="flex-shrink-0 font-semibold" style="color: var(--accent-active);">›</span>{/if}
          </a>
        {/each}
      </div>
    </div>
  </nav>
</aside>
