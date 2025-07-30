import React, { useState } from "react";

function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fadeIn, setFadeIn] = useState(false);

  const handleImageChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFadeIn(false);
    setImage(URL.createObjectURL(file));
    setPrediction(null);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });
      console.log("Réponse du backend :", response);
      if (!response.ok) {
        throw new Error("Erreur lors de la prédiction.");
      }

      const data = await response.json();
      setPrediction({
        breed: data.class,
        confidence: (data.confidence * 100).toFixed(2),
      });
    } catch (error) {
      console.error("Erreur backend :", error);
      alert("Erreur lors de la prédiction. Vérifie que le backend tourne.");
    } finally {
      setLoading(false);
      setFadeIn(true);
    }
  };

  return (
    <div
      style={{
        height: "100%",
        width: "100%",
        overflow: "hidden",
        backgroundColor: "transparent",
        fontFamily:
          "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "0px 0px",
        color: "#222",
        position: "relative",
      }}
    >
      {/* IMAGE DE FOND FLOUE */}
      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100vw",
          height: "100vh",
          backgroundImage: `url('/background1.png')`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          filter: "blur(5px) brightness(0.8)",
          zIndex: -1,
          userSelect: "none",
        }}
        aria-hidden="true"
      />

      {/* Header */}
      <header style={{ textAlign: "center", marginBottom: 40 }}>
        <img
          src="/logo.png"
          alt="Logo chien"
          title="Logo Chien"
          style={{
            width: 90,
            height: 90,
            marginBottom: 12,
            userSelect: "none",
            filter: "drop-shadow(0 0 2px rgba(0,0,0,0.2))",
          }}
        />
        <h1
          style={{
            margin: 0,
            color: "#84bbfa",
            fontWeight: "900",
            fontSize: 32,
            textShadow: "1px 1px 3px rgba(0,0,0,0.15)",
          }}
        >
          Dog Breed Classifier
        </h1>
        <p
          style={{
            color: "#deebfa",
            fontStyle: "italic",
            marginTop: 8,
            fontSize: 18,
            textShadow: "1px 1px 2px rgba(0,0,0,0.05)",
          }}
        >
          Trouve la race de ton chien en un clic !
        </p>
      </header>

      {/* Upload bouton stylé */}
      <label
        htmlFor="file-upload"
        style={{
          display: "inline-block",
          background:
            "linear-gradient(145deg, #6f92ff, #486bff)",
          color: "white",
          padding: "14px 28px",
          borderRadius: 12,
          fontWeight: "600",
          fontSize: 18,
          cursor: "pointer",
          boxShadow:
            "4px 4px 10px #3c54d3, -4px -4px 10px #7fa0ff",
          transition: "box-shadow 0.3s ease",
          userSelect: "none",
          marginBottom: 30,
        }}
      >
        📁 Choisir une image de chien
      </label>
      <input
        id="file-upload"
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        style={{ display: "none" }}
        aria-label="Uploader une image de chien"
      />

      {/* Conteneur flex ligne image + carte */}
      {image && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 30,
            maxWidth: 900,
            width: "100%",
            justifyContent: "center",
            userSelect: "none",
          }}
        >
          {/* Image */}
          <img
            src={image}
            alt="Chien téléchargé"
            style={{
              width: 320,
              height: 320,
              borderRadius: 20,
              boxShadow:
                "0 15px 25px rgba(0,0,0,0.25), 0 5px 15px rgba(0,0,0,0.1)",
              objectFit: "cover",
              transform: fadeIn ? "translateX(0)" : "translateX(-40px)",
              opacity: fadeIn ? 1 : 0,
              transition: "opacity 0.2s ease, transform 0.2s ease",
            }}
          />

          {/* Carte prédiction */}
          <div
            style={{
              width: 400,
              borderRadius: 20,
              boxShadow:
                "0 15px 25px rgba(0,0,0,0.2), 0 5px 10px rgba(0,0,0,0.1)",
              overflow: "hidden",
              backgroundColor: "#fff",
              padding: 25,
              cursor: "default",
              transform: fadeIn ? "translateX(0)" : "translateX(40px)",
              opacity: fadeIn ? 1 : 0,
              transition: "opacity 3.8s ease, transform 6s ease",
              userSelect: "none",
            }}
            aria-live="polite"
          >
            {loading ? (
              <p
                style={{
                  textAlign: "center",
                  color: "#999",
                  fontStyle: "italic",
                  fontSize: 18,
                }}
              >
                🔎 Analyse en cours...
              </p>
            ) : (
              prediction && (
                <>
                  <h2
                    style={{
                      marginTop: 0,
                      marginBottom: 15,
                      fontWeight: "900",
                      fontSize: 24,
                      color: "#2c3e50",
                      textShadow:
                        "1px 1px 3px rgba(0,0,0,0.1)",
                    }}
                  >
                    Race détectée : {prediction.breed}
                  </h2>
                  <div
                    aria-label={`Confiance de ${prediction.confidence} pourcentage`}
                    style={{
                      background: "#e0e0e0",
                      borderRadius: 15,
                      height: 24,
                      overflow: "hidden",
                      boxShadow:
                        "inset 2px 2px 5px #bababa, inset -2px -2px 5px #ffffff",
                    }}
                  >
                    <div
                      style={{
                        width: `${prediction.confidence}%`,
                        background:
                          "linear-gradient(90deg, #4caf50, #81c784)",
                        height: "100%",
                        transition: "width 1s ease-in-out",
                        borderRadius: 15,
                        boxShadow:
                          "0 3px 8px rgba(76,175,80,0.6)",
                      }}
                    />
                  </div>
                  <p
                    style={{
                      marginTop: 12,
                      fontWeight: "700",
                      color: "#3b3b3b",
                      fontSize: 18,
                      textShadow: "0 1px 1px #eee",
                    }}
                  >
                    Confiance : {prediction.confidence}%
                  </p>
                </>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
