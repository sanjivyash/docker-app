const form = document.getElementById("login-form");
let header;

const response = await fetch("http://127.0.0.1:8000");
if(response.status === 200) {
  const data = await response.json();
  console.log(data);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = form.elements["user"].value;
  const password = form.elements["pass"].value;
  const type = form.elements["type"].value;
  const attr = form.elements["attr"].value;

  const response = await fetch("http://127.0.0.1:8000/users/login", {
    method: "POST",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
    redirect: "follow",
    body: JSON.stringify({ username, password })
  });

  if(response.status === 200) {
    header = await response.json();
    sessionStorage.setItem("x-auth-token", header["x-auth-token"]);
    sessionStorage.setItem("type", type);
    sessionStorage.setItem("attr", attr);
    window.location = "./chat.html";
  } else {
    console.assert(response.status === 401) 
    const errors = await response.json();
    alert(errors.detail);
  }
});
