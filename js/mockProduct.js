import comments from "../mocks/comments.json";

// Дублируем массив, чтобы переход был плавным без "склейки"
const doubled = [...comments, ...comments];

const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");

let index = 0;
const visibleCount = 3; // сколько карточек видно
const cardWidth = 320; // ширина карточки + gap

const carousel = document.getElementById("carousel");

// Отрисовываем ВСЕ карточки (двойной набор)
function render() {
  carousel.innerHTML = doubled
    .map(
      (c) => `
        <div class="card">
            <div class="stars">${"★".repeat(c.score)}</div>
            <b>${c.name}</b>
            <p>${c.comment}</p>
        </div>
    `,
    )
    .join("");
}

function updatePosition(animate = true) {
  carousel.style.transition = animate ? "transform 0.4s ease" : "none";
  carousel.style.transform = `translateX(-${index * cardWidth}px)`;
}

function next() {
  index++;
  updatePosition();

  // Когда дошли до конца первого набора — мгновенно прыгаем в начало
  if (index >= comments.length) {
    setTimeout(() => {
      index = 0;
      updatePosition(false); // без анимации
    }, 400); // ждём окончания анимации
  }
}

function prev() {
  if (index <= 0) {
    // Прыгаем в конец второго набора без анимации
    index = comments.length;
    updatePosition(false);
    // Форсируем reflow, потом анимируем
    carousel.offsetHeight;
  }
  index--;
  updatePosition();
}

nextButton.addEventListener("click", next);
prevButton.addEventListener("click", prev);

render();
updatePosition(false);
