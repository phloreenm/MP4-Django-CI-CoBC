
document.addEventListener("DOMContentLoaded", function () {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navbarToggler = document.querySelector('.navbar-toggler');

    document.querySelectorAll('.navbar-collapse .nav-link').forEach(function (link) {
        link.addEventListener('click', function () {
            if (navbarCollapse.classList.contains('show')) {
                new bootstrap.Collapse(navbarCollapse, { toggle: false }).hide();
            }
        });
    });

    const breadcrumbToggle = document.querySelector('.breadcrumb-toggle');
    if (breadcrumbToggle) {
        breadcrumbToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            if (navbarCollapse.classList.contains('show')) {
                new bootstrap.Collapse(navbarCollapse, { toggle: false }).hide();
            } else {
                new bootstrap.Collapse(navbarCollapse, { toggle: false }).show();
            }
        });
    }

    document.addEventListener('click', function (e) {
        const isClickInsideNavbar = navbarCollapse.contains(e.target) || navbarToggler.contains(e.target);
        if (!isClickInsideNavbar && navbarCollapse.classList.contains('show')) {
            new bootstrap.Collapse(navbarCollapse, { toggle: false }).hide();
        }
    });
});
