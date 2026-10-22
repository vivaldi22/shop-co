import { products } from "./mockProduct.js";

const newBlock = document.querySelector('[data-list="new"]');
const topBlock = document.querySelector('[data-list="top"]');
const shopBlock = document.querySelector('[data-list="shop"]');

for (let i = 0; i < products.length; i++) {
  const product = products[i];

  let price = `<span class="current-price">$${product.price}</span>`;

  if (product.oldPrice) {
    price = `
      <div class="product-price">
        <span class="current-price">$${product.price}</span>
        <span class="old-price">$${product.oldPrice}</span>
        <span class="discont-badge">${product.discount}%</span>
      </div>
    `;
  }

  const card = `
    <article class="article-productCard">
      <a class="product-card-link" href="./product.html?id=${product.id}">
        <div class="product__images">
          <img src="${product.image}" alt="${product.title}" class="clothes" />
        </div>
        <div class="container-product--info">
          <h3 class="product-title">${product.title}</h3>
          <div class="container-product--rating">
            <div class="product-stars--cart">
              <img src="${product.stars}" alt="${product.rating}/5" />
            </div>
            <span class="container-rating">${product.rating}/5</span>
          </div>
          ${price}
        </div>
      </a>
    </article>
  `;

  if (newBlock && product.lists.includes("new")) {
    newBlock.innerHTML += card;
  }

  if (topBlock && product.lists.includes("top")) {
    topBlock.innerHTML += card;
  }

  if (shopBlock && product.lists.includes("shop")) {
    shopBlock.innerHTML += `
      <div class="cart__tree">
        <a class="card" href="./product.html?id=${product.id}">
          <img class="card__img" src="${product.image}" alt="${product.title}" />
          <h3 class="card__title">${product.title}</h3>
          <div class="card__rate">
            <img src="${product.stars}" alt="${product.rating}" class="assessment-img" />
            <span class="assessment">${product.rating}/5</span>
          </div>
          ${price}
        </a>
      </div>
    `;
  }
}
