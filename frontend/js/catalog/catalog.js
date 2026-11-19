import { ApiService } from "../product/apiService.js";

const API = "http://127.0.0.1:8000";

const newBlock = document.querySelector('[data-list="new"]');
const topBlock = document.querySelector('[data-list="top"]');
const shopBlock = document.querySelector('[data-list="shop"]');

function imageUrl(image) {
  return `${API}/static/images/${image}.png`;
}

function priceHtml(product) {
  if (!product.oldPrice) {
    return `<span class="current-price">$${product.price}</span>`;
  }

  return `
    <div class="product-price">
      <span class="current-price">$${product.price}</span>
      <span class="old-price">$${product.oldPrice}</span>
      <span class="discont-badge">-${product.discount}%</span>
    </div>
  `;
}

function renderHome(block, products) {
  block.innerHTML = "";

  products.forEach((product) => {
    block.innerHTML += `
      <article class="article-productCard">
        <a class="product-card-link" href="./product.html?id=${product.id}">
          <div class="product__images">
            <img src="${imageUrl(product.image)}" alt="${product.name}" class="clothes" />
          </div>
          <h3 class="product-title">${product.name}</h3>
          <span class="container-rating">${product.rating}/5</span>
          ${priceHtml(product)}
        </a>
      </article>
    `;
  });
}

function renderShop(products) {
  shopBlock.innerHTML = "";

  products.forEach((product) => {
    shopBlock.innerHTML += `
      <a class="card" href="./product.html?id=${product.id}">
        <img class="card__img" src="${imageUrl(product.image)}" alt="${product.name}" />
        <h3 class="card__title">${product.name}</h3>
        <div class="card__rate">
          <span>${product.rating}/5</span>
        </div>
        ${priceHtml(product)}
      </a>
    `;
  });
}

async function init() {
  if (!newBlock && !topBlock && !shopBlock) return;

  let data;
  try {
    data = await ApiService.GET(`${API}/products?limit=24`);
  } catch (e) {
    console.error("Не удалось загрузить товары:", e);
    return;
  }

  // В макете магазина карточки идут по id: 1…9
  const items = (data.items || [])
    .slice()
    .sort((a, b) => Number(a.id) - Number(b.id));

  if (newBlock) renderHome(newBlock, items.slice(0, 4));
  if (topBlock) renderHome(topBlock, items.slice(4, 8));
  if (shopBlock) {
    const shown = items.slice(0, 9);
    renderShop(shown);
    const count = document.querySelector(".catalog__count");
    if (count)
      count.textContent = `Showing 1-${shown.length} of ${data.total} Products`;
  }
}

init();
