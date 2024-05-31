import React from "react";

const VideoPlayer = ({ url }) => {
  return <img src={`http://127.0.0.1:5000/webcam?url=${url}`} alt="rtsp1" />;
};

export default VideoPlayer;
