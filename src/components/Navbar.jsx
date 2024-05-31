import "../styles/styles.css";

function Navbar() {
  const logoutHandler = () => {
    const logout = window.confirm("로그아웃 하시겠습니까?");

    if (logout) {
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
