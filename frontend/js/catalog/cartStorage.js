const STORAGE_KEY = "cart";

export function getCart() {
  try {
    const cart = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    return Array.isArray(cart) ? cart : [];
  } catch {
    return [];
  }
}

export function saveCart(cart) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
}

export function addToCart(product) {
  const cart = getCart();

  const existing = cart.find(
    (item) =>
      item.id === product.id &&
      item.size === product.size &&
      item.color === product.color,
  );

  if (existing) {
    existing.quantity += product.quantity;
  } else {
    cart.push(product);
  }

  saveCart(cart);
  return cart;
}