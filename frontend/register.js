function registerUser() {

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password
        })
    })

    .then(response => response.json())

    .then(data => {

        if (data.user_id) {
            document.getElementById("message").innerText =
                "Registration successful 🚀";

            setTimeout(() => {
                window.location.href = "login.html";
            }, 1500);

        } else {
            document.getElementById("message").innerText =
                data.detail || "Registration failed";
        }

    })

    .catch(error => {

        document.getElementById("message").innerText =
            "Server connection error ❌";

        console.log(error);
    });
}
