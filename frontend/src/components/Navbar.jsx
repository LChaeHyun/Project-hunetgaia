import axios from "axios";
import "../styles/styles.css";

function Navbar() {
  const logoutHandler = () => {
    const logout = window.confirm("로그아웃 하시겠습니까?");

    if (logout) {
      axios.post("/logout", { withCredentials: true });
      sessionStorage.removeItem("session_id");
      window.location.href = "/";
    }
  };

  return (
    <div class="navbar">
      <a href="/profile">Profile</a>
      <a href="/all">All Feeds</a>
      <button onClick={logoutHandler}>Logout</button>
    </div>
  );
}

export default Navbar;
