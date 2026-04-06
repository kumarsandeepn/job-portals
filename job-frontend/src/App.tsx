import { useState } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const res = await fetch("https://job-portals-new.onrender.com/auth/login", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      alert("Login Successful 🚀");
    } else {
      alert("Login Failed ❌");
    }
  };

  return (
    <div style={{ padding: "50px" }}>
      <h1>Job Portal Login</h1>

      <input
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />
      <br /><br />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <br /><br />

      <button onClick={() => handleLogin()}>Login</button>
    </div>
  );
}

export default App;