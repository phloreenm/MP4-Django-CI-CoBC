$(document).ready(function () {
    function showNotification(message, type) {
        const notification = document.getElementById("cart-notification");
        let summaryElem = notification.querySelector(".cart-summary");
        if (!summaryElem) {
            summaryElem = document.createElement("div");
            summaryElem.className = "cart-summary";
            notification.appendChild(summaryElem);
        }
        notification.className = `alert alert-${type}`;
        summaryElem.innerText = message;
        notification.style.display = "block";

        setTimeout(() => {
            notification.style.display = "none";
        }, 5000);
    }

    function showCartModal(total) {
        document.getElementById('cartTotalDisplay').innerText = total;
        var cartModalEl = document.getElementById('cartModal');
        var cartModal = new bootstrap.Modal(cartModalEl, { backdrop: true });
        cartModal.show();
    }

    $(".update-quantity").on("click", function () {
        const row = $(this).closest("tr");
        const itemId = row.data("item-id");
        const action = $(this).data("action");
        const quantityInput = row.find(".quantity-input");
        let newQuantity = parseInt(quantityInput.val());

        if (action === "increment") newQuantity++;
        if (action === "decrement" && newQuantity > 1) newQuantity--;

        console.log("Item ID:", itemId);
        console.log("Action:", action);
        console.log("New Quantity:", newQuantity);

        $.ajax({
            url: `/cart/update/${itemId}/`,
            method: "POST",
            data: {
                quantity: newQuantity,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (response) {
                if (response.item_total && response.cart_total) {
                    row.find(".quantity-input").val(response.item_quantity);
                    row.find(".item-total").text(`£${response.item_total.toFixed(2)}`);
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

    document.querySelectorAll(".add-to-cart-btn").forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();

            const productId = button.dataset.productId;
            const url = `/cart/add/${productId}/`;

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

                    showCartModal(`£${data.total_cost.toFixed(2)}`);
                }
            })
            .catch((error) => console.error("Error:", error));
        });
    });
});