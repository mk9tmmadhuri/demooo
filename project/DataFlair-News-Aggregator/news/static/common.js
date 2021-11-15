console.log("hello");
function redirect(){
    var e = document.getElementById("selectedValue");
      var strUser = e.value;
      console.log(strUser)
      if(strUser == 2){
          window.location.href = 'http://127.0.0.1:8000/nytimes'
      }else if(strUser == 3){
        window.location.href = 'http://127.0.0.1:8000/chicagoReader'
      }else if(strUser == 4  ){
        window.location.href = 'http://127.0.0.1:8000/losAngels'
      }else if(strUser == 5){
        window.location.href = 'http://127.0.0.1:8000/indiaToday'
      }else if(strUser == 6){
        window.location.href = 'http://127.0.0.1:8000/nbc'
      }else if(strUser == 7){
        window.location.href = 'http://127.0.0.1:8000/ndtv'
      }else if(strUser == 8){
        window.location.href = 'http://127.0.0.1:8000/republic'
      }else if(strUser == 9){
        window.location.href = 'http://127.0.0.1:8000/sanDeigo'
      }else if(strUser == 10){
        window.location.href = 'http://127.0.0.1:8000/statesMan'
      }else{
        window.location.href = 'http://127.0.0.1:8000/'
      }

    }

function redirectSignup(){
  window.location.href = 'http://127.0.0.1:8000/register'
}

function logout(){
  window.location.href = 'http://127.0.0.1:8000/logout'
}