// Product_list app: toggling between list view and grid view
document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("product-container");
    const listBtn = document.getElementById("toggle-list");
    const gridBtn = document.getElementById("toggle-grid");

    listBtn.addEventListener("click", () => {
        container.classList.add("list-view");
        container.classList.remove("row", "row-cols-1", "row-cols-md-2", "g-4");
    });

    gridBtn.addEventListener("click", () => {
        container.classList.remove("list-view");
        container.classList.add("row", "row-cols-1", "row-cols-md-2", "g-4");
    });
});