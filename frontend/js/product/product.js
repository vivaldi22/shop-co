import { ApiService } from "./apiService.js";
import { generateCard, generatePrice } from "./productUtils.js";

const smallImages = document.querySelectorAll(".img__transform");
const mainImage = document.querySelector(".main-img");
const title = document.querySelector(".container-info .title");
const rating = document.querySelector(".rating");
const price = document.querySelector(".current-page");
const oldPrice = document.querySelector(".old-page");
const discount = document.querySelector(".discont-page");
const text = document.querySelector(".text");
const colorItems = document.querySelectorAll(".container-info__color > div");
const colorEls = document.querySelectorAll(
  ".container-info__color-purple, .container-info__color-green, .container-info__color-brown",
);
const sizeBtns = document.querySelectorAll(
  ".clothes-btn_small, .clothes-btn_medium, .clothes-btn_large, .clothes-btn_Xlarge",
);
const qtyBtns = document.querySelectorAll(".quantily-selector__btn");
const quantityValue = document.querySelector(".quantily-selector span");
const addToCartBtn = document.querySelector('[data-action="add-to-cart"]');

// нач. отчет
let selectedColor = "Green";
let selectedSize = "Large";
let quantity = 1;
const MIN_QTY = 1;
const MAX_QTY = 99;

// главная асик функция бека
async function init() {
  const idSearch = new URLSearchParams(window.location.search).get("id");
  if (!idSearch) {
    console.error("Элемент не найден");
    return;
  }

  let element;
  try {
    element = await ApiService.GET(
      `http://127.0.0.1:8000/products/${idSearch}`,
    );
  } catch (e) {
    console.error("Не удалось загрузить товар:", e);
    return;
  }

  const imageUrl = `http://127.0.0.1:8000/static/images/${element.image}.png`;
  smallImages.forEach((img) => {
    img.src = imageUrl;
  });

  generateCard(element, { mainImage, title, rating, price, text });
  generatePrice(element, { oldPrice, discount });

  //  Цветовые кружки
  colorItems.forEach((el, i) => {
    if (element.colors && element.colors[i]) {
      el.style.backgroundColor = element.colors[i];
      el.hidden = false;
    } else {
      el.hidden = true;
    }
  });

  // Выбор цвета
  colorEls.forEach((el) => {
    el.style.cursor = "pointer";
    el.addEventListener("click", () => {
      colorEls.forEach((c) => (c.style.outline = "none"));
      el.style.outline = "2px solid #000";
      el.style.outlineOffset = "2px";

      switch (selectedColor) {
        case "container-info__color-purple":
          selectedColor = "Purple";
          break;
        case "container-info__color-green":
          selectedColor = "Green";
          break;
        case "container-info__color-brown":
          selectedColor = "Brown";
          break;
      }
    });
  });

  // Выбор размера
  sizeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      sizeBtns.forEach((b) => {
        b.style.backgroundColor = "#f0f0f0";
        b.style.color = "#00000099";
      });
      btn.style.backgroundColor = "#000000";
      btn.style.color = "#ffffff";

      switch (sizeBtns) {
        case "clothes-btn_small":
          sizeBtns = "Small";
          break;
        case "clothes-btn_medium":
          sizeBtns = "Medium";
          break;
        case "clothes-btn_large":
          sizeBtns = "Large";
          break;
        case "clothes-btn_Xlarge":
          sizeBtns = "X-Large";
      }
    });
  });

  // +/-
  qtyBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.action;
      if (action === "decrement" && quantity > MIN_QTY) quantity--;
      if (action === "increment" && quantity < MAX_QTY) quantity++;
      quantityValue.textContent = quantity;
    });
  });

  // Добавление в корзину
  addToCartBtn.addEventListener("click", () => {
    const cartProduct = {
      id: element.id,
      title: element.name,
      price: element.price,
      image: imageUrl,
      size: selectedSize,
      color: selectedColor,
      quantity: quantity,
    };

    let cart;
    try {
      cart = JSON.parse(localStorage.getItem("cart")) || [];
    } catch {
      cart = [];
    }
    if (!Array.isArray(cart)) cart = [];

    const existing = cart.find(
      (item) =>
        item.id === cartProduct.id &&
        item.size === cartProduct.size &&
        item.color === cartProduct.color,
    );

    if (existing) {
      existing.quantity += cartProduct.quantity;
    } else {
      cart.push(cartProduct);
    }

    localStorage.setItem("cart", JSON.stringify(cart));

    // Фидбэк — внутри обработчика
    addToCartBtn.textContent = "✔️ Added to Cart";
    setTimeout(() => {
      addToCartBtn.textContent = "Add to Cart";
    }, 1200);
  });
}

init();
