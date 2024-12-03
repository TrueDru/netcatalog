// Подтверждение удаления ресурса
document.addEventListener("DOMContentLoaded", function () {
    const deleteLinks = document.querySelectorAll(".delete-link");
    deleteLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            if (!confirm("Are you sure you want to delete this resource?")) {
                event.preventDefault();
            }
        });
    });
});
