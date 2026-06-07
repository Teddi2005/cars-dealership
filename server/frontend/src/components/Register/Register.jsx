import React, { useState } from "react";
const Register = () => {
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const registerUser = async () => {
    const response = await fetch("/djangoapp/register", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({userName, firstName, lastName, email, password})});
    const data = await response.json();
    alert(data.status || "Registration successful");
  };
  return (<div className="register-container"><h1>Sign Up</h1><input type="text" placeholder="Username" value={userName} onChange={e=>setUserName(e.target.value)} /><input type="text" placeholder="First Name" value={firstName} onChange={e=>setFirstName(e.target.value)} /><input type="text" placeholder="Last Name" value={lastName} onChange={e=>setLastName(e.target.value)} /><input type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} /><input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} /><button onClick={registerUser}>Register</button></div>);
};
export default Register;
