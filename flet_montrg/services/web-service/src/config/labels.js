/**
 * 한/영 라벨 — 사이드바, 메인 콘텐츠, 서비스 명 적용
 */
// 서비스 키 → 한/영 표시 이름 (키는 name.replace(/-service$/, '') 와 매칭)
const serviceNames = {
  ko: {
    aggregation: '집계 서비스',
    location: '위치 서비스',
    realtime: '실시간 서비스',
    thresholds: '임계치 서비스',
    alert: '알람 서비스',
    alerts: '알람 서비스',
    'alert-subscription': '알람 구독 서비스',
    'alert-notification': '알림 서비스',
    'sensor-threshold-mapping': '센서 임계치 매핑 서비스',
  },
  en: {
    aggregation: 'Aggregation Service',
    location: 'Location Service',
    realtime: 'Realtime Service',
    thresholds: 'Thresholds Service',
    alert: 'Alert Service',
    alerts: 'Alert Service',
    'alert-subscription': 'Alert Subscription Service',
    'alert-notification': 'Alert Notification Service',
    'sensor-threshold-mapping': 'Sensor Threshold Mapping Service',
  },
};

// 서비스 키 → 한/영 설명 (Swagger UI 태그 설명에 사용)
const serviceDescriptions = {
  ko: {
    aggregation: '체감 온도 데이터 집계 및 통계 API 서비스',
    location: '센서 위치 정보 관리 API 서비스',
    realtime: '실시간 센서 데이터 모니터링 API 서비스',
    thresholds: '체감 온도 임계치 관리 API 서비스',
    alert: '알람 생성 및 관리 API 서비스',
    alerts: '알람 생성 및 관리 API 서비스',
    'alert-subscription': '알람 구독 관리 API 서비스',
    'alert-notification': '알림 발송 및 발송 이력 관리 API 서비스',
    'sensor-threshold-mapping': '센서-임계치 매핑 관리 API 서비스',
  },
  en: {
    aggregation: 'Aggregation and statistics API for perceived temperature data',
    location: 'Sensor location and management API',
    realtime: 'Real-time sensor data monitoring API',
    thresholds: 'Perceived temperature threshold management API',
    alert: 'Alert creation and management API',
    alerts: 'Alert creation and management API',
    'alert-subscription': 'Alert subscription management API',
    'alert-notification': 'Notification delivery and history API',
    'sensor-threshold-mapping': 'Sensor-threshold mapping management API',
  },
};

export const labels = {
  ko: {
    quickLinks: 'Quick Links',
    overview: '개요',
    swaggerUI: 'Swagger UI',
    tableApis: 'Table APIs',
    service: '서비스',
    integratedAll: '통합 (전체 서비스)',
    integratedShort: '통합',
    loadingSpec: 'API 스펙 불러오는 중...',
    loadingServices: '서비스 목록 불러오는 중...',
    loadFailed: 'API 스펙 로드 실패: ',
    searchPlaceholder: '서비스 검색...',
    refresh: '새로고침',
    tableApisDesc: '마스터 데이터 · 설정 · 이력 API — 카드 클릭 시 Swagger 문서',
    swaggerUiCardDesc: 'API 문서 · 전체 서비스를 한 스펙에서',
    servicesIntegrated: '개 서비스 통합',
    apiGatewayDesc: 'API Gateway — 통합 문서 및 프록시',
    noServices: '표시할 서비스가 없습니다. API 백엔드를 연결하거나 새로고침하세요.',
  },
  en: {
    quickLinks: 'Quick Links',
    overview: 'Overview',
    swaggerUI: 'Swagger UI',
    tableApis: 'Table APIs',
    service: 'Service',
    integratedAll: 'Integrated (all services)',
    integratedShort: 'Integrated',
    loadingSpec: 'Loading API spec...',
    loadingServices: 'Loading services...',
    loadFailed: 'Failed to load API spec: ',
    searchPlaceholder: 'Search services...',
    refresh: 'Refresh',
    tableApisDesc: 'Master data · Config · History APIs — Click card for Swagger docs',
    swaggerUiCardDesc: 'API docs · All services in one spec',
    servicesIntegrated: 'services integrated',
    apiGatewayDesc: 'API Gateway — Integrated docs and proxy',
    noServices: 'No services to show. Connect the API backend or use Refresh.',
  },
};

export function getLabels(localeKey) {
  return labels[localeKey] || labels.en;
}

/** locale에 맞는 서비스 표시 이름. 없으면 fallback 반환 */
export function getServiceLabel(serviceName, localeKey, fallback) {
  const key = (serviceName || '').replace(/-service$/, '');
  const map = serviceNames[localeKey] || serviceNames.en;
  return map[key] ?? fallback ?? serviceName;
}

/** Swagger UI 태그 이름 → 서비스 키 (Aggregation → aggregation) */
const tagNameToKey = {
  aggregation: 'aggregation',
  location: 'location',
  realtime: 'realtime',
  thresholds: 'thresholds',
  alert: 'alert',
  'alert subscription': 'alert-subscription',
  'alert notification': 'alert-notification',
  'sensor threshold mapping': 'sensor-threshold-mapping',
};

function tagTitleToKey(title) {
  if (!title || typeof title !== 'string') return null;
  const normalized = title.trim().toLowerCase();
  return tagNameToKey[normalized] ?? normalized.replace(/\s+/g, '-');
}

/** locale에 맞는 서비스 설명. 없으면 null */
export function getServiceDescription(serviceKey, localeKey) {
  const map = serviceDescriptions[localeKey] || serviceDescriptions.en;
  return map[serviceKey] ?? null;
}

/** Swagger UI DOM에서 태그 설명을 locale에 맞게 치환 */
export function applyServiceDescriptions(localeKey) {
  const root = document.getElementById('swagger-ui');
  if (!root) return;
  const sections = root.querySelectorAll('.opblock-tag-section');
  sections.forEach((section) => {
    const tagEl = section.querySelector('.opblock-tag, h3');
    const descEl = section.querySelector('.opblock-tag small, .opblock-tag .opblock-desc');
    if (!tagEl || !descEl) return;
    // 제목만 추출 (설명 부분 제외): descEl 텍스트를 빼면 태그명만 남음
    const full = (tagEl.textContent || '').trim();
    const descText = (descEl.textContent || '').trim();
    const tagTitle = (full.replace(descText, '') || full).trim().split('\n')[0].trim();
    const key = tagTitleToKey(tagTitle);
    if (!key) return;
    const desc = getServiceDescription(key, localeKey);
    if (desc) descEl.textContent = desc;
  });
}
