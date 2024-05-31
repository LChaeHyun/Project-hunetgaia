import axios from "axios";
import { useEffect, useState } from "react";
import "../styles/styles.css";
import Navbar from "../components/Navbar";

function Profile() {
  const [getAddresses, setGetAddresses] = useState("");
  const [RTSPName, setRTSPName] = useState("");
  const [getEmail, setGetEmail] = useState("");
  const [address, setAddress] = useState("");
  const [email, setEmail] = useState("");
  const [isUpdated, setIsUpdated] = useState(false);

  useEffect(() => {
    axios
      .get("/get_all")
      .then((response) => {
        console.log(response);
        setGetAddresses(response.data.addresses);
        setGetEmail(response.data.email);
      })
      .then((error) => console.log(error));
  }, [isUpdated]);

  const rtspDeleteHandler = (id) => {
    axios
      .post("/delete_rtsp", { id: id }) // Assuming address has an id field
      .then((response) => {
        console.log(response);
        if (response.status === 200) {
          setIsUpdated((prev) => !prev);
        }
      })
      .catch((error) => console.log(error));
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
        }
      })
      .catch((error) => console.log(error));
  };

  const emailDeleteHandler = (id) => {
    axios
      .post("/delete_email", { id: id }) // Assuming address has an id field
      .then((response) => {
        if (response.status === 200) {
          setIsUpdated((prev) => !prev);
        }
      })
      .catch((error) => console.log(error));
  };

  const emailSubmitHandler = (e) => {
    e.preventDefault();

    axios
      .post("/add_email", { email: email })
      .then((response) => {
        if (response.status === 200) {
          setIsUpdated((prev) => !prev);
          setEmail("");
        }
      })
      .catch((error) => console.log(error));
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
        <form method="post" onSubmit={rtspSubmitHandler}>
          <input
            type="text"
            name="rtsp_name"
            placeholder="name"
            onChange={(e) => setRTSPName(e.target.value)}
            required
          />
          <input
            type="text"
            name="address"
            placeholder="url"
            onChange={(e) => setAddress(e.target.value)}
            required
          />
          <button type="submit">Add Address</button>
        </form>

        <hr />
        <br />
        <br />

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
        <form method="post" onSubmit={emailSubmitHandler}>
          <input
            type="text"
            name="email"
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
