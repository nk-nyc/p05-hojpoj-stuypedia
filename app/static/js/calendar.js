
var checkbox = document.getElementById('drop-remove');
var modal = document.getElementById('event-modal');
var infoModal = document.getElementById('info-modal');
var currentEvent = null;

function openModal() {
  modal.classList.add('open');
}

function closeModal() {
  modal.classList.remove('open');
  ['modal-title','modal-start-date','modal-start-time',
   'modal-end-date','modal-end-time'].forEach(function(id) {
    document.getElementById(id).value = '';
  });
}

function openInfoModal(event) {
  currentEvent = event;
  var fmt = 'MMM D, YYYY h:mm A';
  document.getElementById('info-title').textContent = event.title;
  document.getElementById('info-start').textContent =
    event.start ? event.start.format(fmt) : '—';
  document.getElementById('info-end').textContent =
    event.end   ? event.end.format(fmt)   : '—';
  document.getElementById('info-color-bar').style.background =
    event.color || '#3a87d3';
  document.getElementById('info-class').textContent = event.description;
  infoModal.classList.add('open');
}
function closeInfoModal() {
  infoModal.classList.remove('open');
  currentEvent = null;
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

function saveEventToServer(title, start, end, color, allDay) {
  return fetch('/events', {
    method: 'POST',
    headers: { "Content-Type": 'application/json'},
    body: JSON.stringify({ title: title, start:start, end: end, color: color, class: class, allDay: allDay})
  }).then(function(r) { return r.json(); });
}

$(document).ready(function () {
  $('#calendar').fullCalendar({
    customButtons: {
      addEventButton: {
        text: '+ Add',
        click: openModal
      }
    },
    timezone: 'local',
    defaultView: 'agendaWeek',
    header: {
      left: 'prev,next today addEventButton',
      center: 'title',
      right: 'month,BasicWeek,agendaWeek,agendaDay'
    },
    navLinks: true,
    editable: true,
    selectable: true,
    unselectCancel: true,
    allDaySlot: true,
    allDayText: 'All Day',
    slotEventOverlap: true,
    eventDurationEditable: true,
    dayMaxEvents: true,
    droppable: true,
    eventClick: function (event) {
      openInfoModal(event);
    },
    eventReceive: function (event) {
      var start = event.start.format();
      var allDay = event.allDay;
      saveEventToServer(event.title, start, null, '#3a87d3', allDay)
        .then(function(data) {
          event.id = data.id;
          $('#calendar').fullCalendar('updateEvent', event);
        });
      if (checkbox.checked) {
        $('#externa-events .fc-event').filter(function(){
          return $(this).text().trim() === event.title;
        }).first().remove();
      }
    },
    drop: function(){
      if (checkbox.checked){
        $(this).remove();
      }
    },
    eventLimit: true,
    nowIndicator: true,
    loading: function(bool){
      $('#loading').toggle(bool);
    },
    events: []
  });

 fetch('/events')
    .then(function(r) { return r.json(); })
    .then(function(events) {
      events.forEach(function(e) {
        $('#calendar').fullCalendar('renderEvent', e, true);
      });
    });

  document.getElementById('modal-submit').addEventListener('click', function() {
    var title = document.getElementById('modal-title').value.trim();
    var startDate = document.getElementById('modal-start-date').value;
    var startTime = document.getElementById('modal-start-time').value;
    var endDate   = document.getElementById('modal-end-date').value;
    var endTime   = document.getElementById('modal-end-time').value;
    var color = document.getElementById('modal-color').value;
    var class = document.getElementById('modal-class').value;

    if (!title) {alert('Please enter an event name.'); return; }
    if(!startDate) {alert('Please select a date.'); return; }

    var start  = startTime ? startDate + 'T' + startTime : startDate;
    var end    = endDate   ? (endTime  ? endDate + 'T' + endTime : endDate) : null;
    var allDay = !startTime;

    if(allDay && end) {
      var endMoment = moment(end).add(1, "days");
      end = endMoment.format('YYYY-MM-DD');
    }

    $('#calendar').fullCalendar('renderEvent', {
      title: title,
      start: start,
      end: end,
      allDay: allDay,
      color: color,
      class: class,
    }, true);

      fetch('/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, start, end, color, class, allDay })
      })
      .then(function(r) {return r.json(); })
      .then(function(data) {
        var rendered = $('#calendar').fullCalendar('clientEvents', function(e){
          return e.title === title && e.start.isSame(start);
        });
        if(rendered.length) {
          rendered[0].id = data.id;
          $('#calendar').fullCalendar('updateEvent', rendered[0]);
        }
      });

    closeModal();
});

document.getElementById('modal-cancel').addEventListener('click', closeModal);
modal.addEventListener('click', function (e) {
  if (e.target === modal ) closeModal();
});

document.getElementById('info-close').addEventListener('click', closeInfoModal);
infoModal.addEventListener('click', function (e) {
  if (e.target === infoModal) closeInfoModal();
});

document.getElementById('info-delete').addEventListener('click', function () {
  if (!currentEvent) return;
  fetch('/events/' + currentEvent.id, { method: 'DELETE' })
    .then(function() {
      $('#calendar').fullCalendar('removeEvents', currentEvent.id);
      closeInfoModal();
    });
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
