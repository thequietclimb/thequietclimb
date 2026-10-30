// Serves the Pocket Local page at the root of pocketlocalsg.com; everything else is static assets.
const PL_HOSTS = new Set(['pocketlocalsg.com', 'www.pocketlocalsg.com']);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'www.pocketlocalsg.com') {
      url.hostname = 'pocketlocalsg.com';
      return Response.redirect(url.toString(), 301);
    }
    if (PL_HOSTS.has(url.hostname)) {
      if (url.pathname === '/' || url.pathname === '/index.html' || url.pathname === '/index') {
        const page = new URL('/pocketlocal', url);
        return env.ASSETS.fetch(new Request(page.toString(), request));
      }
      if (url.pathname === '/pocketlocal' || url.pathname === '/pocketlocal.html') {
        return Response.redirect('https://pocketlocalsg.com/', 301);
      }
    }
    return env.ASSETS.fetch(request);
  },
};
