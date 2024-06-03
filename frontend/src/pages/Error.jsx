import React from "react";
import { useRouteError, useLocation } from "react-router-dom";
import Navbar from "../components/Navbar";

function Error() {
  const error = useRouteError();
  const location = useLocation();
  // default 404
  let message = location.state?.message || "page not found";
  if (error.status === 500) {
    message = JSON.pares(error.data).message;
  }

  return (
    <div>
      <Navbar />
      <p style={{ textAlign: "center", fontSize: "32px", marginTop: "32px" }}>
        {message}
      </p>
    </div>
  );
}

export default Error;
