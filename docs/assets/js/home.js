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
