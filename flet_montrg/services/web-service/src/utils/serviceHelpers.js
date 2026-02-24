/**
 * Service name display and filtering helpers.
 */
// 서비스별 이모지 (사이드바, Overview 카드 등 전부 이모지로 표시)
const DEFAULT_EMOJI = '📄';
const SERVICE_EMOJI = {
  aggregation: '📊',
  location: '📍',
  realtime: '⚡',
  thresholds: '📈',
  alert: '⚠️',
  alerts: '⚠️',
  'alert-subscription': '🔖',
  'alert-notification': '🔔',
  'sensor-threshold-mapping': '⚙️',
};

export function toDisplayName(name, spec) {
  if (spec?.title) return spec.title;
  return name
    .replace(/-service$/, '')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function filterServices(availableServices, searchQuery) {
  const q = (searchQuery || '').toLowerCase().trim();
  return Object.keys(availableServices).filter((name) => {
    const spec = availableServices[name];
    const label = toDisplayName(name, spec);
    return (
      label.toLowerCase().includes(q) ||
      name.toLowerCase().includes(q)
    );
  });
}

export function serviceCardEmoji(name) {
  const key = name.replace(/-service$/, '');
  return SERVICE_EMOJI[key] ?? DEFAULT_EMOJI;
}
