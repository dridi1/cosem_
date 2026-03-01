# TODO

## Tailwind CSS Migration

1. Add Tailwind CSS with a proper build step, not the CDN script.
2. Create the Tailwind setup files:
   `tailwind.config.js`, input CSS, and compiled output under `api/static/css/`.
3. Wire the compiled Tailwind stylesheet into the Flask templates.
4. Migrate shared layout templates first:
   [api/templates/base.html](D:/cosem_/api/templates/base.html),
   [api/templates/base_fr.html](D:/cosem_/api/templates/base_fr.html),
   [api/templates/dashboard_base.html](D:/cosem_/api/templates/dashboard_base.html),
   [api/templates/_marketing_nav.html](D:/cosem_/api/templates/_marketing_nav.html),
   [api/templates/_marketing_footer.html](D:/cosem_/api/templates/_marketing_footer.html).
5. Migrate page templates gradually instead of rewriting the entire app at once.
6. Remove old CSS in phases as Tailwind replacements are confirmed stable.

## Notes

- Tailwind is a good fit for this Flask app now that the templates are more modular.
- The goal is to reduce duplicated CSS and standardize spacing, typography, and responsive behavior.
- Avoid mixing permanent Tailwind usage with all legacy CSS forever.
- Avoid a full app rewrite in one pass.
