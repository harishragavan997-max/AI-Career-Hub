function loginUser() {

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })

    .then(response => response.json())

    .then(data => {

        console.log(data);

        if (data.user_id) {

            document.getElementById("message").innerText =
                "Login successful 🚀";

            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("user_name", data.name || "");

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1000);

        } else {

            document.getElementById("message").innerText =
                data.detail || "Login failed ❌";
        }

    })

    .catch(error => {

        console.log(error);

        document.getElementById("message").innerText =
            "Server connection error ❌";
    });
}
