import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import "../styles/styles.css";
import VideoPlayer from "../components/VideoPlayer";
import axios from "axios";

function Feeds() {
  const [RTSP, setRTSP] = useState(null);
  // const rtspUrls = [
  //   "rtsp://210.99.70.120:1935/live/cctv001.stream",
  //   "rtsp://210.99.70.120:1935/live/cctv002.stream",
  //   "rtsp://210.99.70.120:1935/live/cctv003.stream",
  //   "rtsp://210.99.70.120:1935/live/cctv004.stream",
  // ];

  useEffect(() => {
    axios
      .get("/get_rtsp")
      .then((response) => {
        console.log(response.data.rtsp);
        setRTSP(response.data.rtsp);
      })
      .catch((error) => console.log(error));
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
