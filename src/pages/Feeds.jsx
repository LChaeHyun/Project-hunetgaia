import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import "../styles/styles.css";
import VideoPlayer from "../components/VideoPlayer";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Feeds() {
  const navigate = useNavigate();
  const [RTSP, setRTSP] = useState(null);

  useEffect(() => {
    axios
      .get("/get_rtsp", { withCredentials: true })
      .then((response) => {
        if (response.status === 204) navigate("/");
        console.log(response.data.rtsp);
        setRTSP(response.data.rtsp);
      })
      .catch((error) => console.log(error));
    // eslint-disable-next-line
  }, []);

  return (
    <>
      <Navbar />
      <div className="monitor_page_container">
        {RTSP &&
          RTSP.map(([id, name, url], index) => (
            <div className="cctv_feed" key={index}>
              <h2>
                Feed {index + 1} : {name}
              </h2>
              <VideoPlayer url={url} />
            </div>
          ))}
      </div>
    </>
  );
}

export default Feeds;
