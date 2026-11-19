export const generateCard = (element, els) => {
  els.mainImage.src = `http://127.0.0.1:8000/static/images/${element.image}.png`;
  els.title.textContent = element.name;
  els.rating.textContent = element.rating + "/5";
  els.price.textContent = "$" + element.price;
  els.text.textContent = element.description;
};

export const generatePrice = (element, els) => {
  if (element.oldPrice) {
    els.oldPrice.textContent = "$" + element.oldPrice;
    els.discount.textContent = "-" + element.discount + "%";
    els.oldPrice.hidden = false;
    els.discount.hidden = false;
  } else {
    els.oldPrice.hidden = true;
    els.discount.hidden = true;
  }
};
