$(document).ready(function () {
    $(".update-quantity").on("click", function () {
        const row = $(this).closest("tr");
        const itemId = row.data("item-id");
        const action = $(this).data("action");
        const quantityInput = row.find(".quantity-input");
        let newQuantity = parseInt(quantityInput.val());

        // Increment or decrement quantity
        if (action === "increment") newQuantity++;
        if (action === "decrement" && newQuantity > 1) newQuantity--;

        // Debug: Log values
        console.log("Item ID:", itemId);
        console.log("Action:", action);
        console.log("New Quantity:", newQuantity);

        // Send AJAX request
        $.ajax({
            url: `/cart/update/${itemId}/`,
            method: "POST",
            data: {
                quantity: newQuantity,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (response) {
                if (response.item_total && response.cart_total) {
                    // Update the item's total
                    row.find(".quantity-input").val(response.item_quantity);
                    row.find(".item-total").text(`£${response.item_total.toFixed(2)}`);

                    // Update the cart total
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

        // Debug: Log values
        console.log("Item ID (on change):", itemId);
        console.log("New Quantity (on change):", newQuantity);

        // Send AJAX request
        $.ajax({
            url: `/cart/update/${itemId}/`,
            method: "POST",
            data: {
                quantity: newQuantity,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (response) {
                if (response.item_total && response.cart_total) {
                    // Update the item's total
                    row.find(".item-total").text(`£${response.item_total.toFixed(2)}`);

                    // Update the cart total
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
});