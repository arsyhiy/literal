
    // Полноэкранный popup Каталог
    const catalogBtn = document.getElementById("catalog-btn");
    const catalogPopup = document.getElementById("catalog-popup");
    const closeBtn = document.getElementById("close-popup");
    const overlay = catalogPopup.querySelector(".popup-overlay");

    function openPopup() {
      catalogPopup.classList.add("show");
      document.body.style.overflow = "hidden"; // блокируем скролл страницы
    }

    function closePopup() {
      catalogPopup.classList.remove("show");
      document.body.style.overflow = ""; // возвращаем скролл
    }

    // Открытие по клику
    catalogBtn.addEventListener("click", function (e) {
      e.preventDefault();
      openPopup();
    });

    // Закрытие
    closeBtn.addEventListener("click", closePopup);
    overlay.addEventListener("click", closePopup);

    // Закрытие по Esc
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && catalogPopup.classList.contains("show")) {
        closePopup();
      }
    });




         // --- Корзина на стороне клиента ---
      function getCart() {
        return JSON.parse(localStorage.getItem("cart") || "{}");
      }

      function saveCart(cart) {
        localStorage.setItem("cart", JSON.stringify(cart));
        renderCart();
      }

      function addToCart(bookId, name, price) {
        let cart = getCart();
        if (cart[bookId]) {
          cart[bookId].quantity += 1;
        } else {
          cart[bookId] = { name: name, price: price, quantity: 1 };
        }
        saveCart(cart);
      }

      function removeFromCart(bookId) {
        let cart = getCart();
        delete cart[bookId];
        saveCart(cart);
      }

function renderCart() {
  const cart = getCart();
  const container = document.getElementById("cart-container");

  if (!container) return; // 👈 ВАЖНО

  container.innerHTML = "";

  for (let bookId in cart) {
    const item = cart[bookId];
    container.innerHTML += `
      <div>
        ${item.title} x ${item.quantity}
      </div>
    `;
  }
}

      // --- Отправка корзины на сервер ---
      function checkout() {
        const cart = getCart();
        if (Object.keys(cart).length === 0) {
          alert("Cart is empty");
          return;
        }

        fetch("/checkout/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}",
          },
          body: JSON.stringify({ cart }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.status === "ok") {
              alert("Order received!");
              localStorage.removeItem("cart");
              renderCart();
            }
          });
      }

      // --- Рендер корзины при загрузке страницы ---
      renderCart();

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
  renderFavoritesPage(); // 👈 обновляем страницу
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
      if (!book.name || !book.price) return; // 👈 защита
    container.innerHTML += `
      <div class="book">
        <img src="${book.image}">
        <p><strong>${book.name}</strong></p>
        <p>$${book.price}</p>

        <button class="add-cart-btn"
          data-id="${book.id}"
          data-name="${book.name}"
          data-price="${book.price}">
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

document.addEventListener("DOMContentLoaded", function () {
  renderFavoritesPage();

  document.addEventListener("click", function (e) {
    // удалить из избранного
    if (e.target.classList.contains("remove-fav-btn")) {
      const id = e.target.dataset.id;
      toggleFavorite({ id });
    }

    // добавить в корзину
    if (e.target.classList.contains("add-cart-btn")) {
      const btn = e.target;
      addToCart(btn.dataset.id, btn.dataset.name, Number(btn.dataset.price));
    }

    // ❤️ кнопка (на других страницах)
    if (e.target.classList.contains("fav-btn")) {
      const btn = e.target;

      const book = {
        id: btn.dataset.id,
        name: btn.dataset.name,
        price: Number(btn.dataset.price),
        image: btn.dataset.image
      };

      toggleFavorite(book);

      // меняем цвет
      btn.style.color = isFavorite(book.id) ? "red" : "gray";
    }
  });

  // покрасить сердечки при загрузке
  document.querySelectorAll(".fav-btn").forEach(btn => {
    const id = btn.dataset.id;
    if (isFavorite(id)) {
      btn.style.color = "red";
    }
  });
});


function removeFavorite(bookId) {
  let favs = getFavorites();
  favs = favs.filter(b => b.id !== bookId);
  saveFavorites(favs);
  renderFavoritesPage();
}


document.addEventListener("click", function (e) {
  if (e.target.classList.contains("remove-fav-btn")) {
    const id = e.target.dataset.id;
    removeFavorite(id);
  }
});


document.addEventListener("click", function (e) {
  const btn = e.target.closest(".add-cart-btn");

  if (btn) {
    addToCart(
      btn.dataset.id,
      btn.dataset.name,
      Number(btn.dataset.price)
    );
  }
});

function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

function checkout() {
  const cart = getCart();

  // 🔒 защита от пустой корзины
  if (!cart || Object.keys(cart).length === 0) {
    alert("Корзина пуста");
    return;
  }

  // 🧪 дебаг (можешь потом убрать)
  console.log("CHECKOUT:", cart);

  fetch("/checkout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ cart }),
  })
    .then(res => {
      if (!res.ok) {
        throw new Error("Ошибка запроса");
      }
      return res.json();
    })
    .then(data => {
      if (data.status === "ok") {
        // ✅ очищаем корзину
        localStorage.removeItem("cart");

        // 🔄 обновляем UI (если есть)
        if (typeof renderCart === "function") {
          renderCart();
        }

        // 💬 сообщение
        alert("Заказ оформлен!");

        // 🚀 редирект (опционально)
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


document.addEventListener("click", function (e) {
  const btn = e.target.closest(".checkout-btn");

  if (btn) {
    console.log("CLICKED CHECKOUT"); // 👈
    checkout();
  }
});