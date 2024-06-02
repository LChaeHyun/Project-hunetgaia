import React, { useState } from "react";
import "../styles/login.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    confirm_password: "",
  });
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const signupHandler = (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirm_password) {
      alert("패스워드가 일치하지 않습니다!");
      return;
    }

    axios
      .post("/signup", { id: formData.username, password: formData.password })
      .then((response) => {
        console.log(response);
        if (response.data.signup === true) {
          alert("회원가입 성공! 로그인 해주세요.");
          navigate("/");
        } else {
          alert("회원가입 실패");
        }
      })
      .catch((error) => {
        console.log(error);
        navigate("/error", { state: { message: "회원가입 오류" } });
      });
  };

  return (
    <section class="login_container">
      <div class="signin">
        <div class="content">
          <h2>Sign Up</h2>
          <div class="form">
            <form method="post" onSubmit={signupHandler}>
              <div class="inputBox">
                <input
                  type="text"
                  name="username"
                  required
                  onChange={handleChange}
                />
                <i>Username</i>
              </div>
              <div class="inputBox">
                <input
                  type="password"
                  name="password"
                  required
                  onChange={handleChange}
                />
                <i>Password</i>
              </div>
              <div class="inputBox">
                <input
                  type="password"
                  name="confirm_password"
                  required
                  onChange={handleChange}
                />
                <i>Confirm Password</i>
              </div>
              <div class="inputBox">
                <input type="submit" value="Sign Up" />
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Signup;
