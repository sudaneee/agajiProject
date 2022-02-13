var exampleSocket = new WebSocket("ws://localhost:8000/ws/tableData/");
exampleSocket.onmessage = function (event) {
    var area = document.getElementById("area").value;
    var department = document.getElementById("area").value;
    //var request = new Request.json('https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyAn90sbAUNy2Em2JDA7iAUy4wO18zfclxc'); 
    fetch('https://maps.googleapis.com/maps/api/geocode/json?latlng=11.084191564431112, 7.727661521889511&key=AIzaSyAn90sbAUNy2Em2JDA7iAUy4wO18zfclxc')
    .then(res => res.json())
    .then((out) => {
    console.log(out);
    })
    .catch(err => {
    throw err
    });
    var dataRecieved = JSON.parse(event.data);
    if (dataRecieved.area == area){
    // var path = "{% static 'api/alert.mp3' %}";
    // var audio = new Audio(path);
    // audio.play();
    



    

    }

    

}