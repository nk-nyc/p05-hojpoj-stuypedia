const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

const monthNames= ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

$(document).ready(function(){

  $('#calendar').fullCalendar({
    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'month,basicWeek, basicDay'
    },
    defaultDate: '2026-12-12',
    navLinks: true,
    editable: true,
    eventLimit: true,
    events: []
  });
});
