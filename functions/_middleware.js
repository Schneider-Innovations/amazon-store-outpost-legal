// Per-domain isolation for the 9 store privacy notices.
//
// Each company's custom domain is bound to exactly one slug. Requests that
// land on a known host but a different slug get a 404, so people can't
// browse other companies' notices through someone else's domain.

const HOST_TO_SLUG = {
  "privacy.avatechcorp.us": "a2e",
  "privacy.onebrandavenue.com": "bat",
  "privacy.fancci.us": "fac",
  "privacy.cozeybrand.com": "czy",
  "privacy.schneidercare.com": "smi",
  "privacy.swifthealthessentials.com": "she",
  "privacy.titanflexsafety.com": "tsp",
  "privacy.safesavvy.com": "sns",
  "privacy.schneiderukenterprises.com": "suk",
};

export const onRequest = async ({ request, next }) => {
  const url = new URL(request.url);
  const slug = HOST_TO_SLUG[url.hostname];

  // Preview hosts (*.pages.dev) and any unknown host — pass through unchanged.
  if (!slug) return next();

  // Bare host → send to that company's notice.
  if (url.pathname === "" || url.pathname === "/") {
    return Response.redirect(`${url.origin}/${slug}/`, 302);
  }

  // Allow only the matching slug subtree on this host.
  const root = `/${slug}`;
  if (url.pathname === root || url.pathname.startsWith(`${root}/`)) {
    return next();
  }

  return new Response("Not found", {
    status: 404,
    headers: { "content-type": "text/plain; charset=utf-8" },
  });
};
