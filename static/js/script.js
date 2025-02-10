
document.addEventListener("DOMContentLoaded", function () {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');

    // 1. Close the menu when any nav-link inside the collapse is clicked.
    document.querySelectorAll('.navbar-collapse .nav-link').forEach(function (link) {
        link.addEventListener('click', function () {
            if (navbarCollapse.classList.contains('show')) {
                new bootstrap.Collapse(navbarCollapse, { toggle: false }).hide();
            }
        });
    });

    // 2. Toggle the menu when clicking on the breadcrumb toggle button.
    //    Make sure your breadcrumb button has the class "breadcrumb-toggle"
    const breadcrumbToggle = document.querySelector('.breadcrumb-toggle');
    if (breadcrumbToggle) {
        breadcrumbToggle.addEventListener('click', function (e) {
            // Prevent the click from bubbling up to the document.
            e.stopPropagation();
            if (navbarCollapse.classList.contains('show')) {
                new bootstrap.Collapse(navbarCollapse, { toggle: false }).hide();
            } else {
                new bootstrap.Collapse(navbarCollapse, { toggle: false }).show();
            }
        });
    }

    // 3. Close the menu when clicking anywhere outside the navbar collapse.
    document.addEventListener('click', function (e) {
        // Check if the click occurred inside the navbar collapse or on the toggler button.
        const isClickInsideNavbar = navbarCollapse.contains(e.target) || navbarToggler.contains(e.target);
        if (!isClickInsideNavbar && navbarCollapse.classList.contains('show')) {
            new bootstrap.Collapse(navbarCollapse, { toggle: false }).hide();
        }
    });
});
