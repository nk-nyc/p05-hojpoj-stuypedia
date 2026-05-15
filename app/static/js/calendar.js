var checkbox = document.getElementById('drop-remove');

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
    droppable: true,
    drop: function(date, jsEvent, ui){
      if (checkbox.checked){
        $(this).remove();
      }
    },
    eventLimit: true,
    nowIndicator: true,
    events: []
  });
});

document.addEventListener('DOMContentLoaded', function()
{
  var containerEl = document.getElementById('external-events');

  $('#external-events .fc-event').each(function () {
    $(this).data('event', {
      title: $(this).text(),
      stick: true
    });
    $(this).draggable({
      zIndex: 999,
      revert: true,
      revertDuration: 0
    });
  });
});
