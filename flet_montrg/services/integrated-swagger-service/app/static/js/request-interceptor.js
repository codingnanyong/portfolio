/**
 * Swagger UI: /api/v1/... 를 통합 게이트웨이로 그대로 보냄. /api/svc/ 변환 없음.
 */
function createRequestInterceptor() {
    return (request) => {
        if (request.url.includes('/swagger/')) return request;
        if (request.url.includes('openapi.json') || request.url.includes('/spec')) return request;
        if (request.url.includes('/api/svc/')) return request;

        let pathnameSearch = request.url;
        if (request.url.startsWith('http')) {
            const u = new URL(request.url);
            pathnameSearch = u.pathname + u.search;
        } else if (!pathnameSearch.startsWith('/')) {
            pathnameSearch = '/' + pathnameSearch;
        }

        const base = (typeof window !== 'undefined' ? window.location.origin : '').replace(/\/$/, '');
        request.url = base ? base + pathnameSearch : pathnameSearch;
        return request;
    };
}
