$(document).ready(function () {
  // 🩵 Text animation
  $(".text").textillate({
    loop: true,
    sync: true,
    in: { effect: "bounceIn" },
    out: { effect: "bounceOut" },
  });

  // 🎵 Siri Wave setup
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
    amplitude: 1,
    speed: 0.3,
    autostart: true,
  });

  // ✨ Animated text area for Lunara’s messages
  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: { effect: "fadeInUp", sync: true },
    out: { effect: "fadeOutUp", sync: true },
  });

  // 🎙️ When mic button is clicked
  $("#micBtn").click(function () {
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    eel.playClickSound && eel.playClickSound(); // optional click sound if exists
    eel.start_lunara(); // ✅ this is the correct exposed Python function
  });

  // 🩵 Function Python will call to display Lunara’s messages
  eel.expose(show_text);
  function show_text(text) {
    console.log("From Lunara:", text);
    $(".siri-message").text(text); // show AI’s response
  }
});
