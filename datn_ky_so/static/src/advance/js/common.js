function showLoading(title) {
    Swal.fire({
        title: title,
        allowEscapeKey: false,
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading()
        }
    });
}

function closeAlert() {
    Swal.close();
}