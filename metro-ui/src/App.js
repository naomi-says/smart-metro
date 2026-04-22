import React, { useRef } from "react";
import Webcam from "react-webcam";

function App() {
  const webcamRef = useRef(null);

  const capture = async (url) => {
    const imageSrc = webcamRef.current.getScreenshot();
    const blob = await fetch(imageSrc).then(res => res.blob());

    const formData = new FormData();
    formData.append("image", blob, "capture.jpg");
    formData.append("name", "Naomi");

    const res = await fetch("http://127.0.0.1:5000" + url, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    alert(data.status);
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1>🚇 Smart Metro System</h1>

      <Webcam ref={webcamRef} screenshotFormat="image/jpeg" />

      <br /><br />

      <button onClick={() => capture("/register")}>
        Register Face
      </button>

      <button onClick={() => capture("/verify")}>
        Scan & Enter
      </button>
    </div>
  );
}

export default App;
