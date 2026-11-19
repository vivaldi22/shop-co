import { getCart, saveCart } from "./cartStorage.js";

// корзина

function setSummary(name, value) {
  document.querySelector(`[data-summary="${name}"]`).textContent = "$" + value;
}

const productsContainer = document.querySelector('.cart__container-products');
const subtotalEl = document.getElementById('subtotal');
const discountEl = document.getElementById('discount');
const totalEl = document.getElementById('total');

//  Получить корзину 
function getCart() {
  return JSON.parse(localStorage.getItem('cart')) || [];
}

//  Сохранить корзину 
function saveCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

//  Отрисовать корзину 
function renderCart() {
  const cart = getCart();
  productsContainer.innerHTML = '';

  if (cart.length === 0) {
    productsContainer.innerHTML = `<p class="empty-cart" style="padding:20px;">Your cart is empty</p>`;
    updateSummary(cart);
    return;
  }

  cart.forEach((item, index) => {
    const el = document.createElement('div');
    el.className = 'product__container';
    el.innerHTML = `
      <img class="product-img" src="${item.image}" alt="${item.title}" />
      <div>
        <div class="product__container-info">
          <h4 class="product-title">${item.title}</h4>
          <p class="product-info">Size: <i> ${item.size}</i></p>
          <p class="product-info">Color: <i>${item.color}</i></p>
          <span class="num">$${item.price}</span>
        </div>
      </div>
      <div class="product__container-quantity">
        <img class="corzina-img" src="./images/corzina.svg" alt="delete" data-index="${index}" />
        <div class="quantily-selector">
          <button class="quantily-selector__btn" data-action="dec" data-index="${index}">-</button>
          <span>${item.quantity}</span>
          <button class="quantily-selector__btn" data-action="inc" data-index="${index}">+</button>
        </div>
      </div>
    `;
    productsContainer.appendChild(el);

    // Разделитель (кроме последнего)
    if (index < cart.length - 1) {
      const hr = document.createElement('hr');
      hr.className = 'products-line';
      productsContainer.appendChild(hr);
    }
  });

  //  Обработчики 
  // Удаление
  productsContainer.querySelectorAll('.corzina-img').forEach((img) => {
    img.addEventListener('click', () => {
      const idx = Number(img.dataset.index);
      const cart = getCart();
      cart.splice(idx, 1);
      saveCart(cart);
      renderCart();
    });
  });

  // Количество +/-
  productsContainer.querySelectorAll('.quantily-selector__btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const idx = Number(btn.dataset.index);
      const action = btn.dataset.action;
      const cart = getCart();

      if (action === 'inc') cart[idx].quantity++;
      if (action === 'dec') {
        cart[idx].quantity--;
        if (cart[idx].quantity < 1) cart.splice(idx, 1);
      }

      saveCart(cart);
      renderCart();
    });
  });

  updateSummary(cart);
}

// Пересчёт итогов 
function updateSummary(cart) {
  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const discount = Math.round(subtotal * 0.2);
  const delivery = cart.length > 0 ? 15 : 0;
  const total = subtotal - discount + delivery;

  subtotalEl.textContent = `$${subtotal}`;
  discountEl.textContent = `-$${discount}`;
  totalEl.textContent = `$${total}`;
}

//  Инициализация 
renderCart();
