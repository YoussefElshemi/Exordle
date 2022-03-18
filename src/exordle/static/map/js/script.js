let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 50.7371403, lng: -3.5373362 },
    zoom: 16,
  });
}

function searchWord(e) {  
  e.preventDefault();

  const data = {
    csrfmiddlewaretoken: getCookie("csrftoken"),
    search: e.target.children[0].value
  }

  $.ajax({
    url: "/map/search/",
    method: "POST",
    data,
    success: async ({ success, lat, lng }) => {
      if (success) {
        const infoWindow = new google.maps.InfoWindow({
          content: `
          <h3>${data.search.toUpperCase()}</h3>
          <a href=https://www.google.com/maps?saddr=My+Location&daddr=${lat},${lng}>Directions</a>
          `
        });

        const marker = new google.maps.Marker({
          position: { lat, lng },
          map,
          title: e.target.children[0].value.toUpperCase(),
        });

        map.setCenter(marker.getPosition());
        map.setZoom(16);

        marker.addListener('click', () => {
          infoWindow.open({
            map, 
            anchor: marker,
            shouldFocus: false
          });
        });
      }
    },
    error: console.log
  });
}

function getCookie(name) {
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
  }
}