// Progressive enhancement only: the server owns quantities and every money value.
(() => {
  const workspace = document.getElementById('kiosk-workspace');
  if (!workspace || !window.fetch) return;
  let busy = false;
  workspace.addEventListener('submit', async (event) => {
    const form = event.target;
    if (!form.matches('.cart-form')) return;
    event.preventDefault();
    if (busy) return;
    busy = true;
    const submitter = event.submitter;
    const focusId = submitter?.id;
    const productId = form.querySelector('[name="product_id"]')?.value;
    const data = new FormData(form);
    if (submitter?.name) data.set(submitter.name, submitter.value);
    const buttons = [...workspace.querySelectorAll('button')];
    const disabled = buttons.map((button) => button.disabled);
    buttons.forEach((button) => { button.disabled = true; });
    workspace.setAttribute('aria-busy', 'true');
    const feedback = document.getElementById('cart-feedback');
    feedback.removeAttribute('role');
    feedback.className = 'feedback feedback-info mb-5';
    feedback.textContent = 'Updating your order…';
    try {
      // The hidden field named "action" shadows HTMLFormElement.action.
      const response = await fetch(form.getAttribute('action'), {
        method: 'POST', body: data, credentials: 'same-origin',
        headers: { Accept: 'application/json' },
      });
      if (response.status !== 200 && response.status !== 400) throw new Error('Unexpected response');
      const result = await response.json();
      if (typeof result.html !== 'string') throw new Error('Missing order');
      workspace.innerHTML = result.html;
      const target = document.getElementById(focusId)
        || document.getElementById(`add-product-${productId}`)
        || document.getElementById('order-title');
      if (target && !target.disabled) target.focus({ preventScroll: true });
      else document.getElementById('order-title')?.focus({ preventScroll: true });
    } catch {
      // A lost response may follow a successful POST. Never retry automatically.
      buttons.forEach((button, index) => { button.disabled = disabled[index]; });
      feedback.setAttribute('role', 'alert');
      feedback.className = 'feedback feedback-error mb-5';
      feedback.textContent = 'Connection interrupted. Refresh to check your order before trying again. ';
      const link = document.createElement('a');
      link.href = window.location.pathname;
      link.textContent = 'Refresh order';
      feedback.append(link);
      submitter?.focus({ preventScroll: true });
    } finally {
      workspace.removeAttribute('aria-busy');
      busy = false;
    }
  });
})();
