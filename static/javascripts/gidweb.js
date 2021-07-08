 
 // gps position auto
function gpsAuto(){
   navigator.geolocation.getCurrentPosition(function(position){
   var gpsLat=position.coords.latitude;
   var gpsLong=position.coords.longitude;
   document.querySelector('#gpslat').value=gpsLat;
   document.querySelector('#gpslong').value=gpsLong;
});
};
// Script to open and close sidebar
function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
}
 
function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
}