$(document).ready(function () {
    // Funcția pentru afișarea notificărilor suplimentare
    function showNotification(message, type) {
        const notification = document.getElementById("cart-notification");
        // Asigură-te că elementul conține un copil cu clasa "cart-summary"
        // Dacă nu, poți crea unul:
        let summaryElem = notification.querySelector(".cart-summary");
        if (!summaryElem) {
            summaryElem = document.createElement("div");
            summaryElem.className = "cart-summary";
            notification.appendChild(summaryElem);
        }
        notification.className = `alert alert-${type}`;
        summaryElem.innerText = message;
        notification.style.display = "block";

        // Ascunde notificarea după 5 secunde
        setTimeout(() => {
            notification.style.display = "none";
        }, 5000);
    }

    // Funcția pentru afișarea modalei cu totalul actualizat al coșului
    function showCartModal(total) {
        // Actualizează totalul afișat în modal
        document.getElementById('cartTotalDisplay').innerText = total;
        // Inițializează și afișează modalul (asigură-te că markup-ul este în base.html)
        var cartModalEl = document.getElementById('cartModal');
        var cartModal = new bootstrap.Modal(cartModalEl, { backdrop: true });
        cartModal.show();
    }

    // Manipularea evenimentelor pentru butoanele de incrementare/decrementare
    $(".update-quantity").on("click", function () {
        const row = $(this).closest("tr");
        const itemId = row.data("item-id");
        const action = $(this).data("action");
        const quantityInput = row.find(".quantity-input");
        let newQuantity = parseInt(quantityInput.val());

        // Incrementare sau decrementare
        if (action === "increment") newQuantity++;
        if (action === "decrement" && newQuantity > 1) newQuantity--;

        // Debug: Log valori
        console.log("Item ID:", itemId);
        console.log("Action:", action);
        console.log("New Quantity:", newQuantity);

        // Trimite cererea AJAX pentru actualizarea cantității
        $.ajax({
            url: `/cart/update/${itemId}/`,
            method: "POST",
            data: {
                quantity: newQuantity,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (response) {
                if (response.item_total && response.cart_total) {
                    // Actualizează cantitatea și totalul pentru item
                    row.find(".quantity-input").val(response.item_quantity);
                    row.find(".item-total").text(`£${response.item_total.toFixed(2)}`);
                    // Actualizează totalul coșului
                    $("#cart-total").text(`Total Cost: £${response.cart_total.toFixed(2)}`);
                } else {
                    console.error("Invalid server response:", response);
                    alert("Invalid response from the server.");
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", error);
                console.error("Status:", status);
                alert("Failed to update the cart. Please try again.");
            },
        });
    });

    $(".quantity-input").on("change", function () {
        const row = $(this).closest("tr");
        const itemId = row.data("item-id");
        const newQuantity = parseInt($(this).val());

        console.log("Item ID (on change):", itemId);
        console.log("New Quantity (on change):", newQuantity);

        $.ajax({
            url: `/cart/update/${itemId}/`,
            method: "POST",
            data: {
                quantity: newQuantity,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (response) {
                if (response.item_total && response.cart_total) {
                    row.find(".item-total").text(`£${response.item_total.toFixed(2)}`);
                    $("#cart-total").text(`Total Cost: £${response.cart_total.toFixed(2)}`);
                } else {
                    console.error("Invalid server response:", response);
                    alert("Invalid response from the server.");
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", error);
                alert("Failed to update the cart. Please try again.");
            },
        });
    });

    // Evenimentul pentru butoanele "Add to Cart"
    document.querySelectorAll(".add-to-cart-btn").forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();

            const productId = button.dataset.productId;
            const url = `/cart/add/${productId}/`;

            // Trimite cererea AJAX pentru adăugarea produsului în coș
            fetch(url, {
                method: "GET",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    showNotification(data.error, "danger");
                } else {
                    showNotification(data.success, "success");

                    // Actualizează totalul coșului din navbar
                    document.getElementById("cart-total").innerText = data.total_quantity;

                    // Actualizează costul total pe pagina coșului, dacă există
                    const totalCostElement = document.getElementById("total-cost");
                    if (totalCostElement) {
                        totalCostElement.innerText = `£${data.total_cost}`;
                    }

                    // Afișează modalul cu totalul coșului (formatat ca string)
                    showCartModal(`£${data.total_cost.toFixed(2)}`);
                }
            })
            .catch((error) => console.error("Error:", error));
        });
    });
});