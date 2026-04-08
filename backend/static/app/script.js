
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
        container.innerHTML = "";
        for (let bookId in cart) {
          const item = cart[bookId];
          container.innerHTML += `
            <div>
                ${item.name} x ${item.quantity} — $${(item.price * item.quantity).toFixed(2)}
                <button onclick="removeFromCart('${bookId}')">Remove</button>
            </div>`;
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


    