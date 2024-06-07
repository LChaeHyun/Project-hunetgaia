import React, { useState, useEffect } from "react";
import "../styles/login.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();
  const [validPassword, setValidPassword] = useState(true);
  const [equalToconfirmPassword, setEqualToConfirmPassword] = useState(true);
  const [passwordTouched, setPasswordTouched] = useState(false);
  const [confirmPasswordTouched, setConfirmPasswordTouched] = useState(false);
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

  const handleBlur = (e) => {
    const { name } = e.target;
    if (name === "password") setPasswordTouched(true);
    if (name === "confirm_password") setConfirmPasswordTouched(true);
  };

  useEffect(() => {
    if (passwordTouched && formData.password.length < 6) {
      setValidPassword(false);
    } else {
      setValidPassword(true);
    }
  }, [formData.password, passwordTouched]);

  useEffect(() => {
    if (
      confirmPasswordTouched &&
      formData.confirm_password !== formData.password
    ) {
      setEqualToConfirmPassword(false);
    } else {
      setEqualToConfirmPassword(true);
    }
  }, [formData.confirm_password, formData.password, confirmPasswordTouched]);

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
        if (response.status === 200) {
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
    <section className="login_container">
      <div className="signin">
        <div className="content">
          <h2>Sign Up</h2>
          <div className="form">
            <form method="post" onSubmit={signupHandler}>
              <div className="inputBox">
                <input
                  type="text"
                  name="username"
                  required
                  onChange={handleChange}
                />
                <i>Username</i>
              </div>
              <div className="inputBox">
                <input
                  className={validPassword ? "" : "invalid"}
                  type="password"
                  name="password"
                  required
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
                <i>Password</i>
                {!validPassword && (
                  <p
                    style={{
                      float: "right",
                      margin: "10px 10px",
                      color: "whitesmoke",
                    }}
                  >
                    비밀번호는 6자리 이상이어야 합니다.
                  </p>
                )}
              </div>
              <div className="inputBox">
                <input
                  className={equalToconfirmPassword ? "" : "invalid"}
                  type="password"
                  name="confirm_password"
                  required
                  onChange={handleChange}
                  onBlur={handleBlur}
                />
                <i>Confirm Password</i>
                {!equalToconfirmPassword && (
                  <p
                    style={{
                      float: "right",
                      margin: "10px 10px",
                      color: "whitesmoke",
                    }}
                  >
                    비밀번호가 다릅니다.
                  </p>
                )}
              </div>
              <div className="inputBox">
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
