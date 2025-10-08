function getCSRFToken() {
  const name = 'csrftoken=';
  const cookies = document.cookie.split(';');
  for (let c of cookies) {
    while (c.charAt(0) === ' ') c = c.substring(1);
    if (c.indexOf(name) === 0) return c.substring(name.length, c.length);
  }
  return '';
}

document.addEventListener('submit', async (e) => {
  if (!e.target.matches('#product-create-form')) return;
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('button[type="submit"]');
  btn.disabled = true;

  form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
  form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

  try {
    const fd = new FormData(form);

    const resp = await fetch('/products/create/ajax/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken()
      },
      body: fd
    });

    if (resp.status === 400) {
      const data = await resp.json();
      if (data.errors) {
        showFormErrors(form, data.errors);
      } else {
        showToast('Validation failed', 'danger');
      }
    } else if (!resp.ok) {
      showToast('Request failed', 'danger');
    } else {
      const data = await resp.json();
      if (data.success) {
        // insert HTML returned
        const grid = document.getElementById('product-grid');
        if (grid) {
          grid.insertAdjacentHTML('afterbegin', data.html);
        } else {
          // or refresh whole list
          await refreshProducts();
        }
        // hide modal
        const modalEl = document.getElementById('productModal');
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
        form.reset();
        showToast('Product added!', 'success');
      } else {
        showToast('Unknown error', 'danger');
      }
    }
  } catch (err) {
    console.error(err);
    showToast('Network error', 'danger');
  } finally {
    btn.disabled = false;
  }
});

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
  const list = document.getElementById("product-list");
  list.innerHTML = "<div class='text-center p-5 text-muted'>Loading...</div>";
  try {
    const res = await fetch("/products/json/");
    const data = await res.json();
    list.innerHTML = data.html;
    showToast("Product list updated!", "success");
  } catch {
    list.innerHTML = "<div class='text-center text-danger p-5'>Failed to load products.</div>";
    showToast("Failed to refresh", "danger");
  }
}

document.getElementById("product-create-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector("button[type='submit']");
  btn.disabled = true;

  const formData = new FormData(form);
  const res = await fetch("/products/create/ajax/", {
    method: "POST",
    headers: { "X-CSRFToken": getCSRFToken() },
    body: formData,
  });

  const data = await res.json();
  btn.disabled = false;

  if (data.success) {
    const grid = document.querySelector("#product-grid");
    grid.insertAdjacentHTML("afterbegin", data.html);
    showToast("Product added!", "success");
    const modal = bootstrap.Modal.getInstance(document.getElementById("productModal"));
    modal.hide();
    form.reset();
  } else {
    showToast("Failed to add product", "danger");
  }
});

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

function showToast(msg, type = "primary") {
  const container = document.getElementById("toast-container");
  const id = "toast-" + Date.now();
  const html = `
  <div id="${id}" class="toast align-items-center text-bg-${type} border-0" role="alert">
    <div class="d-flex">
      <div class="toast-body">${msg}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>
  </div>`;
  container.insertAdjacentHTML("beforeend", html);
  const toastEl = document.getElementById(id);
  new bootstrap.Toast(toastEl).show();
}
