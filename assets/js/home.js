document.addEventListener('DOMContentLoaded',function(event){
  var last_visit = localStorage.getItem('last_visit');
  if (  last_visit == null  ) {
    localStorage.setItem('last_visit', 1 );
    var first_log = [];
    var visit_log = sanitized_date(JSON.stringify(first_log));
  } else {
    last_visit = parseInt(last_visit) + 1;
    localStorage.setItem('last_visit', last_visit);
    var visit_log = localStorage.getItem('visit_log');
    visit_log = sanitized_date(visit_log);
  }
  localStorage.setItem('visit_log',visit_log);

  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyC2KlDV4DD-gR4iXLRb05aMYRvKbD3VTfM",
    authDomain: "utility-like-system.firebaseapp.com",
    databaseURL: "https://utility-like-system.firebaseio.com",
    projectId: "utility-like-system",
    storageBucket: "",
    messagingSenderId: "830127512790"
  };
  firebase.initializeApp(config);
  var current_path = window.location.pathname.split('/');
  if (  current_path[1] == "project"  ) {
    var clicks = 0;
    var firebase_url = "https://utility-like-system.firebaseio.com/project-"+ current_path[2] + ".json";
    $.get(firebase_url).done(function(data){
      if (  data != null  ) {
        $('.m-projectContent__count').text(data['likes']);
      }
    });
    $('.m-projectContent__submit').on('click',function(){
      clicks = clicks + 1;
      $.get(firebase_url).done(function(data){
        var likes = 0;
        if (  data != null  ) {
          likes = clicks + data['likes'];
        } else {
          likes = clicks;
        }
        $('.m-projectContent__count').text(likes);
        $.ajax({
          method: "PATCH",
          url: firebase_url,
          data: JSON.stringify({"likes":likes})
        }).done(function( msg ){console.log('Thanks for your kudos.');});
      });
    })
  }
});


//
// UTILITY
//

function sanitized_date(visit_log) {
  var d = new Date();
  visit_log = JSON.parse(visit_log);
  visit_log.push(d);
  return JSON.stringify(visit_log);
}

function seed_projects(){
var projects = ['gimmegear',
 'walkback',
 'sunsama',
 'pom',
 'tunesmash',
 'firefly',
 'siempo',
 'jiffy',
 'nozzle',
 'tiptone',
 'shoshanna',
 'snowrva',
 'oesh',
 'latch',
 'teastick',
 'mother',
 'molly',
 'reachd',
 'jeffersat'];
 for (i = 0; i < projects.length; i++) {
   var firebase_url = "https://utility-like-system.firebaseio.com/project-"+ projects[i] + ".json";
   var seed_like = {'likes':1};
   console.log(firebase_url)
   // $.post(firebase_url, JSON.stringify(seed_like));
   $.ajax({
     method: "PATCH",
     url: firebase_url,
     data: JSON.stringify(seed_like)
   }).done(function( msg ){console.log('Thanks for your kudos.');});
   setTimeout(function(){}, 2000);
 }
 }
