
var checkbox = document.getElementById('drop-remove');
var modal = document.getElementById('event-modal');

function openModal() {
  modal.classList.add('open');
}

function closeModal() {
  modal.classList.remove('open');
  document.getElementById('modal-title').value = '';
  document.getElementById('modal-date').value = '';
  document.getElementById('modal-time').value = '';
}

function makeDraggable(el){
  $(el).data('event', {
    title: $(el).text().trim(),
    stick: true
  });
  $(el).draggable({
    zIndex: 999,
    revert: true,
    revertDuration: 0
  });
}

$(document).ready(function () {
  fetch('/events')
    .then(r => r.json())
    .then(events => {
        events.forEach(e => $('#calendar').fullCalendar('renderEvent', e, true));
    });

  $('#calendar').fullCalendar({
    customButtons: {
      addEventButton: {
        text: '+',
        click: openModal
      }
    },
    defaultView: 'agendaWeek',
    header: {
      left: 'prev,next today addEventButton',
      center: 'title',
      right: 'month,agendaWeek,agendaDay'
    },
    navLinks: true,
    editable: true,
    dayMaxEvents: true,
    droppable: true,
    drop: function(){
      if (checkbox.checked){
        $(this).remove();
      }
    },
    eventLimit: true,
    nowIndicator: true,
    events: []
  });

  document.getElementById('modal-submit').addEventListener('click', function() {
    var title = document.getElementById('modal-title').value.trim();
    var dateStr = document.getElementById('modal-date').value;
    var timeStr = document.getElementById('modal-time').value;
    var color = document.getElementById('modal-color').value;

    if (!title) {alert('Please enter an event name.'); return; }
    if(!dateStr) {alert('Please select a date.'); return; }

    var start = timeStr? dateStr + 'T' + timeStr: dateStr;
    var allDay = !timeStr;

    $('#calendar').fullCalendar('renderEvent', {
      title: title,
      start: start,
      allDay: allDay,
      color: color
    }, true);

      fetch('/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, start, color, allDay })
      });

    closeModal();
});

document.getElementById('modal-cancel').addEventListener('click', closeModal());
modal.addEventListener('click', function (e) {
  if (e.target === modal ) closeModal();
});

document.getElementById('add-draggable-btn').addEventListener('click', addDraggableEvent);
document.getElementById('draggable-input').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') addDraggableEvent();
});


function addDraggableEvent(){
  var input = document.getElementById('draggable-input');
  var name = input.value.trim();
  if (!name) return;

  var $el = $('<div class="fc-event"></div>').text(name);
  $el.insertBefore('#external-events label');
  makeDraggable($el[0]);

  input.value = '';
  input.focus();
}
});
