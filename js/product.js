import { products } from "./mockProduct.js";

const id = new URLSearchParams(window.location.search).get("id");

let product;

for (let i = 0; i < products.length; i++) {
  if (products[i].id == id) {
    product = products[i];
    break;
  }
}

if (!product) {
  product = products[0];
}

const smallImages = document.querySelectorAll(".img__transform");
const mainImage = document.querySelector(".main-img");
const title = document.querySelector(".container-info .title");
const rating = document.querySelector(".rating");
const starsImg = document.querySelector(".container-info--static img");
const price = document.querySelector(".current-page");
const oldPrice = document.querySelector(".old-page");
const discount = document.querySelector(".discont-page");
const text = document.querySelector(".text");
const colorItems = document.querySelectorAll(".container-info__color > div");

for (let i = 0; i < smallImages.length; i++) {
  if (product.gallery) {
    smallImages[i].src = product.gallery[i];
  } else {
    smallImages[i].src = product.image;
  }
}

mainImage.src = product.image;
title.textContent = product.title;
rating.textContent = product.rating + "/5";
starsImg.src = product.stars;
price.textContent = "$" + product.price;
text.textContent = product.description;

if (product.oldPrice) {
  oldPrice.textContent = "$" + product.oldPrice;
  discount.textContent = product.discount + "%";
  oldPrice.hidden = false;
  discount.hidden = false;
} else {
  oldPrice.hidden = true;
  discount.hidden = true;
}

// цвета товара
for (let i = 0; i < colorItems.length; i++) {
  if (product.colors[i]) {
    colorItems[i].style.backgroundColor = product.colors[i];
    colorItems[i].hidden = false;
  } else {
    colorItems[i].hidden = true;
  }
}
