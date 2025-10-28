function getCSRFToken() {
  const name = 'csrftoken=';
  const cookies = document.cookie.split(';');
  for (let c of cookies) {
    while (c.charAt(0) === ' ') c = c.substring(1);
    if (c.indexOf(name) === 0) return c.substring(name.length, c.length);
  }
  return '';
}

// Create / edit form submission
document.addEventListener('submit', async (e) => {
  // handle create/edit form (modal)
  if (!e.target.matches('#product-create-form')) return;
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('button[type="submit"]');
  btn && (btn.disabled = true);

  // clear previous validation
  form.querySelectorAll('.is-invalid').forEach(x => x.classList.remove('is-invalid'));
  form.querySelectorAll('.invalid-feedback').forEach(x => x.remove());

  const editing = form.dataset.editing === 'true';
  const id = form.dataset.id;
  const fd = new FormData(form);

  try {
    const url = editing ? `/products/${id}/edit/ajax/` : '/products/create/ajax/';
    const res = await fetch(url, {
      method: 'POST',
      body: fd,
      headers: { 'X-CSRFToken': getCSRFToken() }
    });

    if (res.status === 400) {
      const data = await res.json();
      if (data.errors) {
        // show validation messages
        for (const name in data.errors) {
          const field = form.querySelector(`[name="${name}"]`);
          if (field) {
            field.classList.add('is-invalid');
            const msg = Array.isArray(data.errors[name]) ? data.errors[name].join(', ') : data.errors[name];
            const div = document.createElement('div');
            div.className = 'invalid-feedback';
            div.innerText = msg;
            field.insertAdjacentElement('afterend', div);
          }
        }
      } else {
        showToast('Validasi gagal', 'warning');
      }
    } else if (!res.ok) {
      showToast('Permintaan gagal', 'danger');
    } else {
      const data = await res.json();
      if (data.success) {
        if (editing) {
          // replace existing card
          const existing = document.getElementById(`product-${id}`);
          if (existing) existing.outerHTML = data.html;
        } else {
          // insert new card at top if grid exists
          const grid = document.getElementById('product-grid');
          if (grid) grid.insertAdjacentHTML('afterbegin', data.html);
        }
        // hide modal
        const modalEl = document.getElementById('productModal');
        const modal = bootstrap.Modal.getInstance(modalEl) || bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.hide();
        // reset form
        form.reset();
        form.dataset.editing = 'false';
        delete form.dataset.id;
        showToast(editing ? 'Produk diperbarui' : 'Produk ditambahkan', 'success');
      } else {
        showToast('Terjadi kesalahan', 'danger');
      }
    }
  } catch (err) {
    console.error(err);
    showToast('Kesalahan jaringan', 'danger');
  } finally {
    btn && (btn.disabled = false);
  }
});

async function editProductOpen(id) {
  try {
    // existing serializer endpoint: /json/<id>/ -> returns Django serializer array
    const res = await fetch(`/json/${id}/`);
    if (!res.ok) throw new Error('Failed to fetch product data');
    const data = await res.json();
    if (!Array.isArray(data) || !data[0]) throw new Error('Invalid product data');
    const fields = data[0].fields;

    const form = document.getElementById('product-create-form');
    form.querySelector('[name="name"]').value = fields.name || '';
    form.querySelector('[name="price"]').value = fields.price ?? '';
    form.querySelector('[name="stock"]').value = fields.stock ?? '';
    form.querySelector('[name="brand"]').value = fields.brand || '';
    form.querySelector('[name="category"]').value = fields.category || '';
    form.querySelector('[name="thumbnail"]').value = fields.thumbnail || '';
    form.querySelector('[name="description"]').value = fields.description || '';
    const featuredEl = form.querySelector('[name="is_featured"]');
    if (featuredEl) featuredEl.checked = fields.is_featured === true;

    // mark as editing
    form.dataset.editing = 'true';
    form.dataset.id = id;

    // update modal title/button text
    const modalEl = document.getElementById('productModal');
    modalEl.querySelector('h5') && (modalEl.querySelector('h5').innerText = 'Edit Product');
    modalEl.querySelector('button[type="submit"]').innerText = 'Save changes';

    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  } catch (err) {
    console.error(err);
    showToast('Gagal memuat data produk', 'danger');
  }
}

let deleteTargetId = null;
function confirmDelete(id, name = '') {
  deleteTargetId = id;
  const nameEl = document.getElementById('delete-modal-product-name');
  if (nameEl) nameEl.innerText = name ? `Produk: ${name}` : '';
  const modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
  modal.show();
}

document.getElementById && document.getElementById('delete-confirm-btn')?.addEventListener('click', async (e) => {
  if (!deleteTargetId) return;
  const btn = e.target;
  btn.disabled = true;
  try {
    const res = await fetch(`/products/${deleteTargetId}/delete/ajax/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCSRFToken() }
    });
    const data = await res.json();
    if (res.ok && data.success) {
      const el = document.getElementById(`product-${deleteTargetId}`);
      if (el) el.remove();
      showToast('Produk dihapus', 'warning');
    } else if (res.status === 403) {
      showToast('Aksi tidak diizinkan', 'danger');
    } else {
      showToast('Gagal menghapus produk', 'danger');
    }
  } catch (err) {
    console.error(err);
    showToast('Kesalahan jaringan', 'danger');
  } finally {
    btn.disabled = false;
    deleteTargetId = null;
    const modalEl = document.getElementById('confirmDeleteModal');
    bootstrap.Modal.getInstance(modalEl)?.hide();
  }
});

// Login / register AJAX
document.addEventListener('submit', async (e) => {
  if (e.target.matches('#login-form') || e.target.matches('#register-form')) {
    e.preventDefault();
    const form = e.target;
    form.querySelectorAll('.is-invalid').forEach(x => x.classList.remove('is-invalid'));
    form.querySelectorAll('.invalid-feedback').forEach(x => x.remove());
    const fd = new FormData(form);
    const url = form.matches('#login-form') ? '/login/ajax/' : '/register/ajax/';
    const btn = form.querySelector('button[type="submit"]');
    btn && (btn.disabled = true);
    try {
      const res = await fetch(url, {
        method: 'POST',
        body: fd,
        headers: { 'X-CSRFToken': getCSRFToken() }
      });
      if (res.status === 400) {
        const data = await res.json();
        if (data.errors) {
          // render field errors or non-field errors
          for (const name in data.errors) {
            const field = form.querySelector(`[name="${name}"]`);
            if (field) {
              field.classList.add('is-invalid');
              const el = document.createElement('div');
              el.className = 'invalid-feedback';
              el.innerText = Array.isArray(data.errors[name]) ? data.errors[name].join(', ') : data.errors[name];
              field.insertAdjacentElement('afterend', el);
            } else {
              // non-field error -> toast
              showToast(Array.isArray(data.errors[name]) ? data.errors[name].join(', ') : data.errors[name], 'warning');
            }
          }
        } else {
          showToast('Validasi gagal', 'warning');
        }
      } else if (!res.ok) {
        showToast('Permintaan gagal', 'danger');
      } else {
        const data = await res.json();
        if (data.success) {
          showToast(form.matches('#login-form') ? 'Login berhasil' : 'Register berhasil', 'success');
          if (data.redirect) {
            window.location.href = data.redirect;
          } else {
            // fallback reload
            window.location.reload();
          }
        } else {
          showToast('Gagal', 'danger');
        }
      }
    } catch (err) {
      console.error(err);
      showToast('Kesalahan jaringan', 'danger');
    } finally {
      btn && (btn.disabled = false);
    }
  }
});

// wire refresh button
document.getElementById('refresh-btn')?.addEventListener('click', refreshProducts);

function showFormErrors(form, errors) {
  for (const name in errors) {
    const field = form.querySelector(`[name="${name}"]`);
    if (field) {
      field.classList.add('is-invalid');
      const msg = Array.isArray(errors[name]) ? errors[name].join(', ') : errors[name];
      const el = document.createElement('div');
      el.className = 'invalid-feedback';
      el.innerText = msg;
      field.insertAdjacentElement('afterend', el);
    }
  }
}


async function refreshProducts() {
  const grid = document.getElementById('product-grid');
  const btn = document.getElementById('refresh-btn');
  if (!grid) return;
  // show loading placeholder
  grid.innerHTML = `<div class="text-center p-5 text-muted"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div><div class="mt-2">Memuat produk...</div></div>`;
  btn && btn.setAttribute('disabled', 'disabled');
  try {
    const res = await fetch('/products/json/');
    if (!res.ok) throw new Error('Fetch failed');
    const data = await res.json();
    grid.innerHTML = data.html || `<div class="text-center p-5 text-muted">Tidak ada produk.</div>`;
    showToast('Daftar produk diperbarui', 'info');
  } catch (err) {
    console.error(err);
    grid.innerHTML = `<div class="text-center text-danger p-5">Gagal memuat produk. Coba lagi.</div>`;
    showToast('Gagal memuat produk', 'danger');
  } finally {
    btn && btn.removeAttribute('disabled');
  }
}

async function confirmDelete(id) {
  if (!confirm("Are you sure you want to delete this product?")) return;
  const res = await fetch(`/products/${id}/delete/ajax/`, {
    method: "POST",
    headers: { "X-CSRFToken": getCSRFToken() },
  });
  const data = await res.json();
  if (data.success) {
    document.getElementById(`product-${id}`).remove();
    showToast("Product deleted!", "danger");
  } else {
    showToast("Delete failed", "warning");
  }
}


function showToast(message, type = 'success', autohide = true) {
  // type: 'success'|'danger'|'warning'|'info'
  const container = document.getElementById('toast-container') || (() => {
    const d = document.createElement('div');
    d.id = 'toast-container';
    d.className = 'position-fixed bottom-0 end-0 p-3';
    d.style.zIndex = 2000;
    document.body.appendChild(d);
    return d;
  })();

  const id = 'toast-' + Date.now();
  const html = `
    <div id="${id}" class="toast align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>`;
  container.insertAdjacentHTML('beforeend', html);
  const el = document.getElementById(id);
  const t = new bootstrap.Toast(el, { autohide });
  t.show();
  }