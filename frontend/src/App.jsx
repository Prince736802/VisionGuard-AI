import {
  useEffect,
  useRef,
  useState
} from "react";

import "./App.css";


const API_URL =
  "http://127.0.0.1:8000";


function App() {

  // =====================================================
  // IMAGE DETECTION STATES
  // =====================================================

  const [file, setFile] =
    useState(null);

  const [preview, setPreview] =
    useState(null);

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  // =====================================================
  // CAMERA REFERENCES
  // =====================================================

  const videoRef =
    useRef(null);

  const canvasRef =
    useRef(null);

  const liveBusyRef =
    useRef(false);


  // =====================================================
  // CAMERA STATES
  // =====================================================

  const [cameraOn, setCameraOn] =
    useState(false);

  const [liveImage, setLiveImage] =
    useState(null);

  const [liveStats, setLiveStats] =
    useState({

      total_persons: 0,

      with_helmet: 0,

      without_helmet: 0,

      checking: 0,

      compliance: 0

    });


  // =====================================================
  // SELECT IMAGE
  // =====================================================

  const handleFileChange = (
    event
  ) => {

    const selectedFile =
      event.target.files[0];


    if (!selectedFile) {
      return;
    }


    setFile(
      selectedFile
    );

    setResult(null);

    setError("");


    const imageUrl =
      URL.createObjectURL(
        selectedFile
      );


    setPreview(
      imageUrl
    );
  };


  // =====================================================
  // IMAGE DETECTION
  // =====================================================

  const detectHelmet = async () => {

    if (!file) {

      setError(
        "Please select an image first."
      );

      return;
    }


    setLoading(true);

    setError("");

    setResult(null);


    try {

      const formData =
        new FormData();


      formData.append(
        "file",
        file
      );


      const response =
        await fetch(
          `${API_URL}/detect`,
          {
            method: "POST",
            body: formData
          }
        );


      if (!response.ok) {

        throw new Error(
          "Detection request failed."
        );
      }


      const data =
        await response.json();


      if (!data.success) {

        throw new Error(
          "Detection failed."
        );
      }


      setResult(
        data
      );

    } catch (err) {

      console.error(err);

      setError(
        "Could not connect to VisionGuard AI backend. Make sure FastAPI is running."
      );

    } finally {

      setLoading(false);

    }
  };


  // =====================================================
  // START CAMERA
  // =====================================================

  const startCamera =
    async () => {

      try {

        setError("");


        const stream =
          await navigator.mediaDevices.getUserMedia(
            {
              video: {
                width: {
                  ideal: 1280
                },

                height: {
                  ideal: 720
                }
              },

              audio: false
            }
          );


        if (!videoRef.current) {
          return;
        }


        videoRef.current.srcObject =
          stream;


        await videoRef.current.play();


        setCameraOn(true);


      } catch (err) {

        console.error(err);

        setError(
          "Camera permission was denied or the camera is unavailable."
        );

      }
    };


  // =====================================================
  // STOP CAMERA
  // =====================================================

  const stopCamera =
    () => {

      const video =
        videoRef.current;


      if (
        video &&
        video.srcObject
      ) {

        const tracks =
          video.srcObject.getTracks();


        tracks.forEach(
          (track) => {
            track.stop();
          }
        );


        video.srcObject =
          null;
      }


      setCameraOn(false);

      setLiveImage(null);

      setLiveStats({

        total_persons: 0,

        with_helmet: 0,

        without_helmet: 0,

        checking: 0,

        compliance: 0

      });
    };


  // =====================================================
  // PROCESS LIVE CAMERA FRAME
  // =====================================================

  const processLiveFrame =
    async () => {

      if (!cameraOn) {
        return;
      }


      if (liveBusyRef.current) {
        return;
      }


      const video =
        videoRef.current;

      const canvas =
        canvasRef.current;


      if (!video || !canvas) {
        return;
      }


      if (
        video.videoWidth === 0 ||
        video.videoHeight === 0
      ) {

        return;
      }


      liveBusyRef.current =
        true;


      try {

        canvas.width =
          video.videoWidth;

        canvas.height =
          video.videoHeight;


        const context =
          canvas.getContext(
            "2d"
          );


        context.drawImage(
          video,
          0,
          0,
          canvas.width,
          canvas.height
        );


        const blob =
          await new Promise(
            (resolve) => {

              canvas.toBlob(
                resolve,
                "image/jpeg",
                0.70
              );

            }
          );


        if (!blob) {
          return;
        }


        const formData =
          new FormData();


        formData.append(
          "file",
          blob,
          "live-frame.jpg"
        );


        const response =
          await fetch(
            `${API_URL}/live-detect`,
            {
              method: "POST",
              body: formData
            }
          );


        if (!response.ok) {

          throw new Error(
            "Live detection request failed."
          );
        }


        const data =
          await response.json();


        if (data.success) {

          setLiveImage(
            data.image
          );


          setLiveStats(
            data.statistics
          );
        }


      } catch (err) {

        console.error(
          "Live detection error:",
          err
        );

      } finally {

        liveBusyRef.current =
          false;
      }
    };


  // =====================================================
  // LIVE DETECTION TIMER
  // =====================================================

  useEffect(
    () => {

      if (!cameraOn) {
        return;
      }


      const interval =
        setInterval(
          processLiveFrame,
          700
        );


      return () => {

        clearInterval(
          interval
        );

      };

    },

    [cameraOn]
  );


  // =====================================================
  // STOP CAMERA WHEN PAGE CLOSES
  // =====================================================

  useEffect(
    () => {

      return () => {

        const video =
          videoRef.current;


        if (
          video &&
          video.srcObject
        ) {

          video.srcObject
            .getTracks()
            .forEach(
              (track) => {
                track.stop();
              }
            );
        }

      };

    },

    []
  );


  // =====================================================
  // UI
  // =====================================================

  return (

    <div className="app">


      {/* =================================================
          HEADER
          ================================================= */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            🛡️
          </div>

          <div>

            <h1>
              VisionGuard AI
            </h1>

            <p>
              AI-Powered Safety Monitoring
            </p>

          </div>

        </div>


        <div className="system-status">

          <span className="status-dot"></span>

          SYSTEM ONLINE

        </div>

      </header>


      {/* =================================================
          MAIN
          ================================================= */}

      <main className="main">


        {/* =================================================
            HERO
            ================================================= */}

        <section className="hero">

          <div className="hero-badge">
            YOLOv8 • COMPUTER VISION • AI
          </div>


          <h2>
            Intelligent Helmet Detection
          </h2>


          <p>
            Detect helmet compliance using
            real-time artificial intelligence
            and computer vision.
          </p>

        </section>


        {/* =================================================
            IMAGE DETECTION
            ================================================= */}

        <section className="upload-card">

          <div className="section-title">

            <div>

              <span className="section-number">
                01
              </span>

              <h2>
                Image Detection
              </h2>

              <p>
                Upload an image and let
                VisionGuard AI analyze
                helmet compliance.
              </p>

            </div>

          </div>


          {/* FILE INPUT */}

          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={
              handleFileChange
            }
            hidden
          />


          <label
            htmlFor="file-upload"
            className="choose-button"
          >
            📁 Choose Image
          </label>


          {/* PREVIEW */}

          {preview && (

            <div className="preview-box">

              <img
                src={preview}
                alt="Selected"
              />

            </div>

          )}


          {/* DETECT BUTTON */}

          <button
            className="detect-button"
            onClick={detectHelmet}
            disabled={
              !file ||
              loading
            }
          >

            {loading
              ? "⏳ Analyzing..."
              : "🔍 Run Detection"}

          </button>


          {/* ERROR */}

          {error && (

            <div className="error-box">

              ⚠️ {error}

            </div>

          )}


          {/* =================================================
              IMAGE RESULT
              ================================================= */}

          {result && (

            <div className="results">


              <div className="result-header">

                <div>

                  <span className="section-number">
                    RESULT
                  </span>

                  <h2>
                    Detection Results
                  </h2>

                </div>


                <div className="result-success">
                  ✓ ANALYSIS COMPLETE
                </div>

              </div>


              {/* STATISTICS */}

              <div className="stats-grid">

                <div className="stat-card">

                  <span>
                    👤
                  </span>

                  <p>
                    Total Persons
                  </p>

                  <strong>
                    {
                      result.statistics
                        .total_persons
                    }
                  </strong>

                </div>


                <div className="stat-card safe">

                  <span>
                    🪖
                  </span>

                  <p>
                    With Helmet
                  </p>

                  <strong>
                    {
                      result.statistics
                        .with_helmet
                    }
                  </strong>

                </div>


                <div className="stat-card danger">

                  <span>
                    ⚠️
                  </span>

                  <p>
                    Without Helmet
                  </p>

                  <strong>
                    {
                      result.statistics
                        .without_helmet
                    }
                  </strong>

                </div>


                <div className="stat-card">

                  <span>
                    📊
                  </span>

                  <p>
                    Compliance
                  </p>

                  <strong>
                    {
                      result.statistics
                        .compliance
                    }%
                  </strong>

                </div>

              </div>


              {/* IMAGES */}

              <div className="image-results">

                <div className="image-panel">

                  <div className="image-panel-title">
                    Original Image
                  </div>

                  <img
                    src={preview}
                    alt="Original"
                  />

                </div>


                <div className="image-panel">

                  <div className="image-panel-title">
                    AI Detection
                  </div>

                  <img
                    src={result.image}
                    alt="AI Detection"
                  />

                </div>

              </div>


              {/* DETECTION DETAILS */}

              {result.detections &&
                result.detections.length > 0 && (

                  <div className="details">

                    <h3>
                      Detection Details
                    </h3>


                    {result.detections.map(
                      (
                        detection,
                        index
                      ) => (

                        <div
                          className="detail-row"
                          key={index}
                        >

                          <span>
                            Person {index + 1}
                          </span>


                          <strong
                            className={
                              detection.status ===
                              "With Helmet"
                                ? "helmet-status"
                                : detection.status ===
                                  "Without Helmet"
                                ? "no-helmet-status"
                                : ""
                            }
                          >
                            {
                              detection.status
                            }
                          </strong>


                          <span>
                            Confidence:{" "}
                            {
                              detection.helmet_confidence
                            }
                          </span>

                        </div>

                      )
                    )}

                  </div>

                )}

            </div>

          )}

        </section>


        {/* =================================================
            LIVE CAMERA
            ================================================= */}

        <section className="live-card">


          <div className="live-header">

            <div>

              <span className="section-number">
                02
              </span>

              <h2>
                🎥 Live Camera Detection
              </h2>

              <p>
                Use your camera for real-time
                helmet monitoring.
              </p>

            </div>


            <div className="live-status">

              <span
                className={
                  cameraOn
                    ? "live-dot active"
                    : "live-dot"
                }
              ></span>


              {cameraOn
                ? "CAMERA ACTIVE"
                : "CAMERA OFF"}

            </div>

          </div>


          {/* CAMERA AREA */}

          <div className="camera-container">


            <video
              ref={videoRef}
              className="camera-video"
              muted
              playsInline
            />


            {!cameraOn && (

              <div className="camera-placeholder">

                <div className="camera-icon">
                  🎥
                </div>

                <h3>
                  Camera is Off
                </h3>

                <p>
                  Start the camera to begin
                  real-time detection.
                </p>

              </div>

            )}


            {cameraOn &&
              liveImage && (

                <img
                  src={liveImage}
                  className="live-result"
                  alt="Live AI Detection"
                />

              )}

          </div>


          {/* CAMERA BUTTON */}

          <div className="camera-buttons">


            {!cameraOn ? (

              <button
                className="start-camera"
                onClick={
                  startCamera
                }
              >
                🎥 Start Live Detection
              </button>

            ) : (

              <button
                className="stop-camera"
                onClick={
                  stopCamera
                }
              >
                ⏹ Stop Camera
              </button>

            )}

          </div>


          {/* LIVE STATISTICS */}

          <div className="live-stats">


            <div>

              <span>
                👤
              </span>

              <p>
                Persons
              </p>

              <strong>
                {
                  liveStats.total_persons
                }
              </strong>

            </div>


            <div>

              <span>
                🪖
              </span>

              <p>
                With Helmet
              </p>

              <strong>
                {
                  liveStats.with_helmet
                }
              </strong>

            </div>


            <div>

              <span>
                ⚠️
              </span>

              <p>
                No Helmet
              </p>

              <strong>
                {
                  liveStats.without_helmet
                }
              </strong>

            </div>


            <div>

              <span>
                📊
              </span>

              <p>
                Compliance
              </p>

              <strong>
                {
                  liveStats.compliance
                }%
              </strong>

            </div>


          </div>

        </section>


      </main>


      {/* =================================================
          FOOTER
          ================================================= */}

      <footer className="footer">

        <p>
          VisionGuard AI • Intelligent
          Computer Vision Safety System
        </p>

        <p>
          Powered by YOLOv8 + FastAPI +
          React
        </p>

      </footer>


      {/* =================================================
          HIDDEN CANVAS
          ================================================= */}

      <canvas
        ref={canvasRef}
        style={{
          display: "none"
        }}
      />

    </div>

  );
}


export default App;