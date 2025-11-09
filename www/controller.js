$(document).ready(function () {
  // ✅ Function to display messages from Python
  eel.expose(DisplayMessage);
  function DisplayMessage(text) {
    document.querySelector(".text").innerText = text;
  }

  // ✅ Function to reset UI
  eel.expose(ShowHood);
  function ShowHood() {
    document.querySelector(".text").innerText = "🎧 Lunara ready again...";
  }
});
