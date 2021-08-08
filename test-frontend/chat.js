let header;
let ws;

const token = sessionStorage.getItem("x-auth-token");
const type = sessionStorage.getItem("type");
const attr = sessionStorage.getItem("attr");

const messages = document.getElementById("messages");
const form = document.getElementById("chat-form");
const textbox = form.elements["msg"];

const response = await fetch("http://127.0.0.1:8000/auth/check", {
  method: "GET",
  mode: "cors",
  headers: { "x-auth-token": token },
  redirect: "follow"
});

if(response.status !== 200) {
  alert("Token expired, please login again");
  window.location = "./login.html";
}

if(token == null) {
  window.location = "./login.html";
} else {
  header = { "x-auth-token": token };
  console.log(header);
}

if(type === "url") {
  ws = new WebSocket(`ws://localhost:8000/ws/create/${attr}?x-auth-token=${token}`);
  ws.onopen = () => console.log("room created");
} else if(type === "token") {
  ws = new WebSocket(`ws://localhost:8000/ws/join/${attr}?x-auth-token=${token}`);
  ws.onopen = () => console.log("joined room");
} else {
  window.location = "./login.html";
}

ws.addEventListener("message", async(e) => {
  const response = JSON.parse(e.data);
  
  if(response.error) {
    alert(response.error);
    window.location = "./login.html";
  }

  if(response.token) {
    const tokenPlace = document.getElementById("token");
    tokenPlace.innerHTML = "Token is " + response.token;
    return;
  }

  if(response.event.action === "chat") {
    const user = response.sender;
    const message = response.event.load.message;
    const node = document.createElement('li');

    if(user === "bot") {
      node.innerHTML = `<i>${message}</i>`
    } else {
      node.innerHTML = `<b>${user}</b> : ${message}`;
    }

    messages.appendChild(node);
  }
});


const displayMessage = () => {
  const message = form.elements["msg"].value;
  form.elements["msg"].value = "";
  
  const node = document.createElement('li');
  node.innerHTML = `<b>You</b> : ${message}`;
  messages.appendChild(node);

  const event = {
    action: "chat",
    load: { message }
  };
  ws.send(JSON.stringify(event));
};

textbox.addEventListener("keydown", e => {
  if(e.keyCode == 13 && e.shiftKey) {
    return;
  }

  if(e.keyCode === 13) {
    e.preventDefault();
    displayMessage();
    return;
  }
});

form.addEventListener("submit", e => {
  e.preventDefault();
  displayMessage();
});
