// Serves the Pocket Local page at the root of pocketlocalsg.com; everything else is static assets.
const PL_HOSTS = new Set(['pocketlocalsg.com', 'www.pocketlocalsg.com']);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/googlec9f09f3f4cdd60e4.html') {
      return new Response('google-site-verification: googlec9f09f3f4cdd60e4.html', { headers: { 'content-type': 'text/html; charset=utf-8' } });
    }
    if (url.hostname === 'www.pocketlocalsg.com') {
      url.hostname = 'pocketlocalsg.com';
      return Response.redirect(url.toString(), 301);
    }
    if (PL_HOSTS.has(url.hostname)) {
      if (url.pathname === '/sitemap.xml') {
        return env.ASSETS.fetch(new Request(new URL('/pl-sitemap.xml', url).toString(), request));
      }
      if (url.pathname === '/robots.txt') {
        return new Response('User-agent: *\nAllow: /\nSitemap: https://pocketlocalsg.com/sitemap.xml\n', { headers: { 'content-type': 'text/plain' } });
      }
      if (url.pathname === '/' || url.pathname === '/index.html' || url.pathname === '/index') {
        const page = new URL('/pocketlocal', url);
        return env.ASSETS.fetch(new Request(page.toString(), request));
      }
      if (url.pathname === '/pocketlocal' || url.pathname === '/pocketlocal.html') {
        return Response.redirect('https://pocketlocalsg.com/', 301);
      }
    }
    if (url.hostname.endsWith('thequietclimbsg.com') && url.pathname.startsWith('/guides/')) {
      return Response.redirect('https://pocketlocalsg.com' + url.pathname.replace(/\.html$/, ''), 301);
    }
    if (url.hostname.endsWith('thequietclimbsg.com') && (url.pathname === '/pocketlocal' || url.pathname === '/pocketlocal.html' || url.pathname === '/itix' || url.pathname === '/itix.html')) {
      return Response.redirect('https://pocketlocalsg.com/' + url.search, 301);
    }
    return env.ASSETS.fetch(request);
  },
};
