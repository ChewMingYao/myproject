function showAllReports() {
  document.getElementById("viewAllBtn").style.display = "none";
  document.getElementById("hiddenReports").style.display = "flex";
}

function showAllAnnouncements() {
  document.getElementById("viewAllBtn2").style.display = "none";
  document.getElementById("hiddenAnnouncement").style.display = "flex";
}

document.getElementById("announcement_datetime").setAttribute("readonly", "true");

// back button
function goBack() {
  window.history.back();
}

//index
const photoSlider = document.querySelector(".photo-slider");

let currentImage = 0;

function slideImages() {
  currentImage++;
  if (currentImage === 3) {
    currentImage = 0;
  }
  const translateXValue = -currentImage * 100;
  photoSlider.style.transform = `translateX(${translateXValue}%)`;
}

setInterval(slideImages, 5000);
//
