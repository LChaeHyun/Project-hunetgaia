import { useState } from "react";
import "../styles/login.css";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const submitHandler = async (e) => {
    e.preventDefault();

    try {
      axios
        .post("/", {
          id: username,
          password: password,
        })
        .then((response) => {
          console.log(response);

          if (response.data.isLogin === true) {
            sessionStorage.setItem("session_id", response.data.session_id);

            navigate("/profile");
          } else {
            alert("아이디 또는 비밀번호가 유효하지 않습니다");
          }
        })
        .catch((error) => {
          console.log(error);
          navigate("/error", { state: { message: "로그인 오류" } });
        });
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <section class="login_container">
      <div class="signin">
        <div class="content">
          <h2>Sign In</h2>
          <div class="form">
            <form
              method="post"
              action="/"
              id="login-form"
              onSubmit={submitHandler}
            >
              <div class="inputBox">
                <input
                  type="text"
                  required
                  name="id"
                  onChange={(e) => setUsername(e.target.value)}
                />{" "}
                <i>id</i>
              </div>
              <div class="inputBox">
                <input
                  type="password"
                  name="password"
                  required
                  onChange={(e) => setPassword(e.target.value)}
                />
                <i>Password</i>
              </div>
              <div class="links">
                <Link to="#">Forgot Password</Link>
                <Link to="/signup">Signup</Link>
              </div>
              <div class="inputBox">
                <input type="submit" value="Login" class="submit_btn" />
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Home;
