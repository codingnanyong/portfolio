<script>
  import { FOOTER_AUTHOR, FOOTER_EMAIL, GITEA_REPO_URL, FOOTER_LICENSE, LICENSE_URL } from '../config/constants.js';
</script>

<footer
  class="flex-shrink-0 py-3 px-9 border-t flex items-center justify-center flex-wrap gap-x-5 gap-y-2 text-[0.8rem]"
  style="background: var(--bg-secondary); border-color: var(--border); color: var(--text-tertiary);"
>
  <span>© {FOOTER_AUTHOR}</span>
  <a href="mailto:{FOOTER_EMAIL}" class="no-underline hover:underline" style="color: var(--accent);">Contact</a>
  <a href={LICENSE_URL} target="_blank" rel="noopener noreferrer" class="no-underline hover:underline" style="color: var(--accent);">{FOOTER_LICENSE}</a>
  <a href={GITEA_REPO_URL} target="_blank" rel="noopener noreferrer" class="no-underline hover:underline" style="color: var(--accent);">Repository</a>
</footer>
