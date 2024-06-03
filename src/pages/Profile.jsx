import axios from "axios";
import { useEffect, useState } from "react";
import "../styles/styles.css";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

function Profile() {
  const [getAddresses, setGetAddresses] = useState("");
  const [RTSPName, setRTSPName] = useState("");
  const [getEmail, setGetEmail] = useState("");
  const [address, setAddress] = useState("");
  const [email, setEmail] = useState("");
  const [isUpdated, setIsUpdated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get("/get_all", { withCredentials: true })
      .then((response) => {
        console.log(response);
        if (response.status === 204) navigate("/");
        console.log(response.data.rtsp);
        setGetAddresses(response.data.addresses);
        setGetEmail(response.data.email);
      })
      .catch((error) => {
        console.log(error);
        navigate("/error", { state: { message: "정보 가져오기 실패" } });
      });
    // eslint-disable-next-line
  }, [isUpdated]);

  const rtspDeleteHandler = (id) => {
    axios
      .post("/delete_rtsp", { id: id })
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          setIsUpdated((prev) => !prev);
        }
      })
      .catch((error) => {
        console.log(error);
        navigate("/error", { state: { message: "RTSP 삭제 실패" } });
      });
  };

  const rtspSubmitHandler = (e) => {
    e.preventDefault();

    axios
      .post("/add_rtsp", { name: RTSPName, address: address })
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          setAddress("");
          setRTSPName("");
          setIsUpdated((prev) => !prev);
        } else if (response.status === 204) {
          alert("이미 존재하는 RTSP입니다.");
        }
      })
      .catch((error) => {
        console.log(error);
        navigate("/error", { state: { message: "RTSP 등록 실패" } });
      });
  };

  const emailDeleteHandler = (id) => {
    axios
      .post("/delete_email", { id: id })
      .then((response) => {
        if (response.status === 200) {
          setIsUpdated((prev) => !prev);
        }
      })
      .catch((error) => {
        console.log(error);
        navigate("/error", { state: { message: "Email 삭제 실패" } });
      });
  };

  const emailSubmitHandler = (e) => {
    e.preventDefault();

    axios
      .post("/add_email", { email: email })
      .then((response) => {
        if (response.status === 200) {
          setIsUpdated((prev) => !prev);
          setEmail("");
        } else if (response.status === 204) {
          alert("이미 존재하는 이메일입니다.");
        }
      })
      .catch((error) => {
        console.log(error);
        navigate("/error", { state: { message: "Email 등록 실패" } });
      });
  };

  return (
    <>
      <Navbar />
      <div class="profile_page_container">
        <h1>Profile</h1>
        <h2>Registered Addresses</h2>
        <ul class="address_list">
          {getAddresses &&
            getAddresses.map(([id, name, url]) => (
              <li class="address_item" key={id}>
                <span>
                  {name} : {url}
                </span>
                <button onClick={() => rtspDeleteHandler(id)}>Remove</button>
              </li>
            ))}
        </ul>

        <h2>Add a New Address</h2>
        <form method="post" onSubmit={rtspSubmitHandler} className="rtsp_form">
          <input
            className="name"
            type="text"
            name="rtsp_name"
            placeholder="name"
            onChange={(e) => setRTSPName(e.target.value)}
            required
          />
          <input
            className="url"
            type="text"
            name="address"
            placeholder="url"
            onChange={(e) => setAddress(e.target.value)}
            required
          />
          <button type="submit">Add Address</button>
        </form>

        <h2>Registered Email</h2>
        <ul class="address_list">
          {getEmail &&
            getEmail.map(([id, email]) => (
              <li class="address_item" key={id}>
                <span>{email}</span>
                <button onClick={() => emailDeleteHandler(id)}>Remove</button>
              </li>
            ))}
        </ul>

        <h2>Add a New Email</h2>
        <form
          method="post"
          onSubmit={emailSubmitHandler}
          className="email_form"
        >
          <input
            className="email"
            type="text"
            name="email"
            placeholder="email"
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <button type="submit">Add Email</button>
        </form>
      </div>
    </>
  );
}

export default Profile;
