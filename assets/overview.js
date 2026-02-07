window.dash_clientside = Object.assign(
  {},
  window.dash_clientside,
  {
    overview: {
      init: function (n) {
        // βρίσκουμε όλα τα overview boxes (service-scoped)
        const boxes = document.querySelectorAll("[id$='-box']");

        boxes.forEach((box) => {
          // bind μόνο μία φορά
          if (box.dataset.bound === "true") return;
          box.dataset.bound = "true";

          // derive service id
          const serviceId = box.id.replace("-box", "");
          const cursorOut = document.getElementById(
            `${serviceId}-cursor-position`
          );

          // local JS state (όπως παλιά)
          let currentImage = 1;

          // mouse move → cursor tracking
          box.addEventListener("mousemove", (e) => {
            const rect = box.getBoundingClientRect();
            const x = Math.round(e.clientX - rect.left);
            const y = Math.round(e.clientY - rect.top);

            if (cursorOut) {
              cursorOut.innerText = `cursor: x=${x}, y=${y}`;
            }
          });

          // mouse down → image toggle (ίδιο behavior με πριν)
          box.addEventListener("mousedown", (e) => {
            if (e.button !== 0) return;

            if (currentImage === 1) {
              box.style.backgroundImage =
                'url("/assets/subsea-cables-internet-ai-spooky-pooka-illustration.jpg")';
              currentImage = 2;
            } else {
              box.style.backgroundImage =
                'url("/assets/Undersea-Cables.jpeg")';
              currentImage = 1;
            }
          });

          // disable right-click
          box.addEventListener("contextmenu", (e) =>
            e.preventDefault()
          );
        });

        return "";
      },
    },
  }
);