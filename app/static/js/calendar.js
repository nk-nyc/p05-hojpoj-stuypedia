$(document).ready(function () {
  $('#calendar').fullCalendar({
    customButtons: {
      addEventButton: {
        text: '+',
        click: function () {
          const title = prompt('Event name:');
          var dateStr = prompt('Enter date of event');
          var date = new Date(dateStr + 'T00:00:00');
          if (title) {
            $('#calendar').fullCalendar('renderEvent', {
              title: title,
              start: date,
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
