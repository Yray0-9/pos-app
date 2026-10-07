// Touch entry and visible processing only. Django validates and completes the sale.
(() => {
  const form = document.getElementById('payment-form');
  if (!form) return;
  const input = document.getElementById('amount-paid');
  if (input) {
    form.querySelectorAll('[data-key]').forEach((button) => {
      button.addEventListener('click', () => {
        const key = button.dataset.key;
        let value = input.value;
        if (key === 'backspace') value = value.slice(0, -1);
        else if (key === '.') { if (!value.includes('.')) value = (value || '0') + '.'; }
        else if (value.length < 12 && (!value.includes('.') || value.split('.')[1].length < 2)) value += key;
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
      });
    });
    document.getElementById('clear-cash').addEventListener('click', () => { input.value = ''; input.focus(); });
    document.getElementById('exact-cash').addEventListener('click', (event) => {
      input.value = event.currentTarget.dataset.exact;
      input.focus();
    });
  }
  let busy = false;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (busy) return;
    busy = true;
    form.setAttribute('aria-busy', 'true');
    form.querySelectorAll('button').forEach((button) => { button.disabled = true; });
    if (input) input.readOnly = true;
    document.getElementById('processing-feedback').hidden = false;
    // Keep card processing visible without pretending to contact a real reader.
    if (form.dataset.method === 'card') await new Promise((resolve) => setTimeout(resolve, 1200));
    HTMLFormElement.prototype.submit.call(form);
  });
})();
