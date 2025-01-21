$(document).ready(function () {
    // Update quantity via AJAX
    $(".update-quantity").on("click", function () {
        const row = $(this).closest("tr");
        const itemId = row.data("item-id");
        const action = $(this).data("action");
        const quantityInput = row.find(".quantity-input");
        let newQuantity = parseInt(quantityInput.val());

        // Increment or decrement quantity
        if (action === "increment") newQuantity++;
        if (action === "decrement" && newQuantity > 1) newQuantity--;

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
                    alert("Invalid response from the server.");
                }
            },
            error: function () {
                alert("Failed to update the cart. Please try again.");
            },
        });
    });

    // Update total on quantity input change (focus out)
    $(".quantity-input").on("change", function () {
        const row = $(this).closest("tr");
        const itemId = row.data("item-id");
        const newQuantity = parseInt($(this).val());

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
                    alert("Invalid response from the server.");
                }
            },
            error: function () {
                alert("Failed to update the cart. Please try again.");
            },
        });
    });
});