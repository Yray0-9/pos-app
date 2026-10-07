// Revalidate pages restored from browser history, including after customer reset.
window.addEventListener('pageshow', (event) => {
  if (event.persisted) window.location.reload();
});
