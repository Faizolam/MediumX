let BASE_URL = `http://127.0.0.1:8000/`;
// SignUp and SignIn, open and closed
const signUp = document.getElementById("signUp");
const signIn = document.getElementById("signIn");
const mainSignUp = document.getElementById("mainSignUp");
const mainSignIn = document.getElementById("mainSignIn");
const closeSignUp = document.getElementById("closeSignUp");
const closeSignIn = document.getElementById("closeSignIn");
const content = document.getElementById("home-articles");
const navigation = document.getElementById("navigation");
const signUpModalContent = document.querySelector("#mainSignUp .modal-content");
const signInModalContent = document.querySelector("#mainSignIn .modal-content");

signUp.addEventListener("click", function () {
  closeModal(mainSignIn);
  openModal(mainSignUp);
});

signIn.addEventListener("click", function () {
  closeModal(mainSignUp);
  openModal(mainSignIn);
});

closeSignUp.addEventListener("click", function () {
  closeModal(mainSignUp);
});

closeSignIn.addEventListener("click", function () {
  closeModal(mainSignIn);
});

mainSignUp.addEventListener("click", function (event) {
  // If the click is outside the modal content, close the modal
  if (!signUpModalContent.contains(event.target)) {
    closeModal(mainSignUp);
  }
});

mainSignIn.addEventListener("click", function (event) {
  // If the click is outside the modal content, close the modal
  if (!signInModalContent.contains(event.target)) {
    closeModal(mainSignIn);
  }
});

content.addEventListener("click", function () {
  closeModal(mainSignUp);
  closeModal(mainSignIn);
});

// Reusable functions for opening and closing modals
function closeModal(modal) {
  modal.classList.add("closed");
  modal.classList.remove("open");
  if (content) content.classList.remove("blurred");
  navigation.classList.remove("blurred");
}

function openModal(modal) {
  modal.classList.add("open");
  modal.classList.remove("closed");
  if (content) content.classList.add("blurred");
  navigation.classList.add("blurred");
}


// const signupBtn = document.getElementById('signUpBtn');
const signUpForm = document.querySelector(".mainSignUp form");
const signInForm = document.querySelector(".mainSignIn form");
const switchToSignIn = document.querySelector(".go-signIn");
const switchToSignUp = document.querySelector(".go-signUp");
const gmailInput = document.getElementById("signup-gmail");

switchToSignIn.addEventListener("click", function () {
  closeModal(mainSignUp);
  content.classList.add("blurred");
  navigation.classList.add("blurred");
  openModal(mainSignIn);
});

switchToSignUp.addEventListener("click", function () {
  closeModal(mainSignIn);
  content.classList.add("blurred");
  navigation.classList.add("blurred");
  openModal(mainSignUp);
});

// Create user
signUpForm.addEventListener("submit", function (event) {
  event.preventDefault(); 

  const userName = document.getElementById("signup-username").value;
  const gmailId = document.getElementById("signup-gmail").value;
  const passWord = document.getElementById("signup-password").value;

  // console.log("Sign Up:", { userName, gmailId, passWord });
  createUser(userName, gmailId, passWord);
});

async function createUser(userName, gmailId, passWord) {
  try {
    let response = await fetch(`${BASE_URL}users/`, {
      method: "POST",
      body: JSON.stringify({
        username: userName,
        email: gmailId,
        password: passWord,
      }),
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
      },
    });

    // console.log("Raw response: ", response);

    if (response.ok) {
      let userData = await response.json();
      // console.log("User created successfully:", userData);
      closeModal(mainSignUp);
    } else {
      console.error("Error creating user, status:", response.status);
      const errorData = await response.json();
      console.error("Error response:", errorData);
    }
  } catch (error) {
    console.error("Request failed:", error);
  }
}

signUpForm.addEventListener("submit", function (event) {
  const gmailInputVal = gmailInput.value;

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailPattern.test(gmailInputVal)) {
    event.preventDefault();
    alert("Please enter a valid email address!");
  }
});

//Login User
signInForm.addEventListener("click", function (event) {
  event.preventDefault();

  const gmailId = document.getElementById("signin-gmail").value;
  const passWord = document.getElementById("signin-password").value;

  console.log("Sing-In:", { gmailId, passWord });
  loginUser(gmailId, passWord);
});

async function loginUser(gmailId, passWord) {
  try {
    let formData = new FormData();
    formData.append("username", gmailId);
    formData.append("password", passWord);

    let response = await fetch(`${BASE_URL}login/`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      let loginData = await response.json();
      // console.log("Login Successful", loginData);
      closeModal(mainSignIn);

      localStorage.setItem("accessToken", loginData.access_token);
    } else {
      console.error("Error Login user, status: ", response.status);
    }
  } catch (error) {
    console.error("Request failed:", error);
  }
}
