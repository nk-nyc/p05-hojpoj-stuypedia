$(document).ready(function () {
  $('#calendar').fullCalendar({
    customButtons: {
      addEventButton: {
        text: '+',
        click: function () {
          const title = prompt('Event name:');
          if (title) {
            $('#calendar').fullCalendar('renderEvent', {
              title: title,
              start: new Date(),  
              allDay: true
            }, true); 
          }
        }
      }
    },
    header: {
      left: 'prev,next today addEventButton', 
      center: 'title',
      right: 'month,basicWeek,basicDay'
    },
    navLinks: true,
    editable: true,
    eventLimit: true,
    nowIndicator: true,
    events: []
  });
});