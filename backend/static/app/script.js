// Полноэкранный popup Каталог
const catalogBtn = document.getElementById("catalog-btn");
const catalogPopup = document.getElementById("catalog-popup");
const closeBtn = document.getElementById("close-popup");
const overlay = catalogPopup.querySelector(".popup-overlay");

function openPopup() {
  catalogPopup.classList.add("show");
  document.body.style.overflow = "hidden";
}

function closePopup() {
  catalogPopup.classList.remove("show");
  document.body.style.overflow = "";
}

catalogBtn.addEventListener("click", function (e) {
  e.preventDefault();
  openPopup();
});

closeBtn.addEventListener("click", closePopup);
overlay.addEventListener("click", closePopup);

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && catalogPopup.classList.contains("show")) {
    closePopup();
  }
});


// ===================== 🛒 КОРЗИНА =====================

// получить корзину
function getCart() {
  return JSON.parse(localStorage.getItem("cart") || "{}");
}

// сохранить корзину
function saveCart(cart) {
  localStorage.setItem("cart", JSON.stringify(cart));
  renderCart();
}

// ➕ добавить товар (БЕЗ цены!)
function addToCart(productId, name) {
  let cart = getCart();

  if (cart[productId]) {
    cart[productId].quantity += 1;
  } else {
    cart[productId] = {
      name: name,
      quantity: 1,
    };
  }

  saveCart(cart);
}

// ❌ удалить товар
function removeFromCart(productId) {
  let cart = getCart();
  delete cart[productId];
  saveCart(cart);
}

// 🎨 отрисовка корзины
function renderCart() {
  const cart = getCart();
  const container = document.getElementById("cart-container");

  if (!container) return;

  container.innerHTML = "";

  for (let productId in cart) {
    const item = cart[productId];

    container.innerHTML += `
      <div>
        ${item.name} x ${item.quantity}
        <button onclick="removeFromCart('${productId}')">❌</button>
      </div>
    `;
  }
}

// 🔐 CSRF
function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

// 🚀 checkout (ОДНА версия, без дублей)
function checkout() {
  const cart = getCart();

  if (!cart || Object.keys(cart).length === 0) {
    alert("Корзина пуста");
    return;
  }

  fetch("/checkout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ cart }),
  })
    .then(res => {
      if (!res.ok) throw new Error("Ошибка запроса");
      return res.json();
    })
    .then(data => {
      if (data.status === "ok") {
        localStorage.removeItem("cart");
        renderCart();
        alert("Заказ оформлен!");
        window.location.href = "/orders/";
      } else {
        alert("Ошибка оформления заказа");
      }
    })
    .catch(err => {
      console.error("Checkout error:", err);
      alert("Что-то пошло не так");
    });
}

// клик по checkout
document.addEventListener("click", function (e) {
  const btn = e.target.closest(".checkout-btn");
  if (btn) checkout();
});

// отрисовать корзину при загрузке
renderCart();


// ===================== ❤️ ИЗБРАННОЕ =====================

function getFavorites() {
  return JSON.parse(localStorage.getItem("favorites") || "[]");
}

function saveFavorites(favs) {
  localStorage.setItem("favorites", JSON.stringify(favs));
}

function toggleFavorite(book) {
  let favs = getFavorites();

  const exists = favs.find(b => b.id === book.id);

  if (exists) {
    favs = favs.filter(b => b.id !== book.id);
  } else {
    favs.push(book);
  }

  saveFavorites(favs);
  renderFavoritesPage();
}

function renderFavoritesPage() {
  const favs = getFavorites();
  const container = document.getElementById("favorites-container");
  const emptyMsg = document.getElementById("empty-msg");

  if (!container) return;

  container.innerHTML = "";

  if (favs.length === 0) {
    emptyMsg.style.display = "block";
    return;
  }

  emptyMsg.style.display = "none";

  favs.forEach(book => {
    if (!book.name || !book.price) return;

    container.innerHTML += `
      <div class="book">
        <img src="${book.image}">
        <p><strong>${book.name}</strong></p>
        <p>$${book.price}</p>

        <button class="add-cart-btn"
          data-id="${book.id}"
          data-name="${book.name}">
          В корзину
        </button>

        <button class="remove-fav-btn"
          data-id="${book.id}">
          ❌ Убрать
        </button>
      </div>
    `;
  });
}

function isFavorite(bookId) {
  return getFavorites().some(b => b.id === bookId);
}

function removeFavorite(bookId) {
  let favs = getFavorites();
  favs = favs.filter(b => b.id !== bookId);
  saveFavorites(favs);
  renderFavoritesPage();
}


// ===================== EVENTS =====================

document.addEventListener("DOMContentLoaded", function () {
  renderFavoritesPage();

  document.addEventListener("click", function (e) {
    if (e.target.classList.contains("remove-fav-btn")) {
      removeFavorite(e.target.dataset.id);
    }

    if (e.target.classList.contains("add-cart-btn")) {
      const btn = e.target;
      addToCart(btn.dataset.id, btn.dataset.name);
    }

    if (e.target.classList.contains("fav-btn")) {
      const btn = e.target;

      const book = {
        id: btn.dataset.id,
        name: btn.dataset.name,
        price: Number(btn.dataset.price),
        image: btn.dataset.image
      };

      toggleFavorite(book);
      btn.style.color = isFavorite(book.id) ? "red" : "gray";
    }
  });

  document.querySelectorAll(".fav-btn").forEach(btn => {
    const id = btn.dataset.id;
    if (isFavorite(id)) {
      btn.style.color = "red";
    }
  });
});
