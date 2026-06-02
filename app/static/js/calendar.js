var checkbox = document.getElementById('drop-remove');
var modal = document.getElementById('event-modal');
var infoModal = document.getElementById('info-modal');
var currentEvent = null;
var editingEventId = null;

function openModal(prefill) {
  editingEventId = null;
  document.getElementById('modal-title-heading').textContent = 'Add Event';
  document.getElementById('modal-submit').textContent = 'Add Event';
  if (prefill) {
    editingEventId = prefill.id;
    document.getElementById('modal-title').value = prefill.title || '';
    document.getElementById('modal-start-date').value = prefill.start ? prefill.start.format('YYYY-MM-DD') : '';
    document.getElementById('modal-start-time').value = prefill.start && !prefill.allDay ? prefill.start.format('HH:mm') : '';
    document.getElementById('modal-end-date').value = prefill.end ? prefill.end.format('YYYY-MM-DD') : '';
    document.getElementById('modal-end-time').value = prefill.end && !prefill.allDay ? prefill.end.format('HH:mm') : '';
    document.getElementById('modal-color').value = prefill.color || '#3a87d3';
    document.getElementById('modal-class').value = prefill.linked_class || '';
    document.getElementById('modal-title-heading').textContent = 'Edit Event';
    document.getElementById('modal-submit').textContent = 'Save Changes';
  }
  modal.classList.add('open');
}

function closeModal() {
  modal.classList.remove('open');
  ['modal-title','modal-start-date','modal-start-time',
   'modal-end-date','modal-end-time', 'modal-class'].forEach(function(id) {
    document.getElementById(id).value = '';
  });
}

function getClassName(classId) {
  if (!classId) return 'None';
  var select = document.getElementById('modal-class');
  for (var i = 0; i < select.options.length; i++) {
    if (select.options[i].value == classId) return select.options[i].text;
  }
  return classId;
}

function openInfoModal(event) {
  currentEvent = event;
  var fmt = 'MMM D, YYYY h:mm A';
  document.getElementById('info-title').textContent = event.title;
  document.getElementById('info-start').textContent =
    event.start ? event.start.format(fmt) : '—';
  document.getElementById('info-end').textContent =
    event.end   ? event.end.format(fmt)   : '—';
  document.getElementById('info-class').textContent =
    getClassName(event.linked_class);
  document.getElementById('info-color-bar').style.background =
    event.color || '#3a87d3';
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

function saveEventToServer(title, start, end, color, linkedClass, allDay) {
  return fetch('/events', {
    method: 'POST',
    headers: { "Content-Type": 'application/json'},
    body: JSON.stringify({ title: title, start:start, end: end, color: color, linked_class: linkedClass, allDay: allDay})
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
      saveEventToServer(event.title, start, null, '#3a87d3', null, allDay)
        .then(function(data) {
          event.id = data.id;
          $('#calendar').fullCalendar('updateEvent', event);
        });
      if (checkbox.checked) {
        $('#external-events .fc-event').filter(function(){
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

  document.getElementById('modal-edit').addEventListener('click', function(){
    openModal(currentEvent);
    closeInfoModal();
  });

  document.getElementById('modal-submit').addEventListener('click', function() {
    var title = document.getElementById('modal-title').value.trim();
    var startDate = document.getElementById('modal-start-date').value;
    var startTime = document.getElementById('modal-start-time').value;
    var endDate   = document.getElementById('modal-end-date').value;
    var endTime   = document.getElementById('modal-end-time').value;
    var color = document.getElementById('modal-color').value;
    var linkedClass = document.getElementById('modal-class').value || null;

    if (!title) {alert('Please enter an event name.'); return; }
    if(!startDate) {alert('Please select a date.'); return; }

    var start  = startTime ? startDate + 'T' + startTime : startDate;
    var end    = endDate   ? (endTime  ? endDate + 'T' + endTime : endDate) : null;
    var allDay = !startTime;

    if(allDay && end) {
      var endMoment = moment(end).add(1, "days");
      end = endMoment.format('YYYY-MM-DD');
    }

    if (editingEventId) {
      fetch('/events/' + editingEventId, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title, start: start, end: end,
                               color: color, linked_class: linkedClass, allDay: allDay })
      }).then(function() {
        var existing = $('#calendar').fullCalendar('clientEvents', editingEventId);
        if (existing.length) {
          existing[0].title        = title;
          existing[0].start        = moment(start);
          existing[0].end          = end ? moment(end) : null;
          existing[0].color        = color;
          existing[0].linked_class = linkedClass;
          existing[0].allDay       = allDay;
          $('#calendar').fullCalendar('updateEvent', existing[0]);
        }
      });
    } else {
      $('#calendar').fullCalendar('renderEvent', {
        title: title,
        start: start,
        end: end,
        allDay: allDay,
        color: color,
        linked_class: linkedClass,
      }, true);

      saveEventToServer(title, start, end, color, linkedClass, allDay)
        .then(function(data) {
          var rendered = $('#calendar').fullCalendar('clientEvents', function(e){
            return e.title === title && e.start.isSame(start);
          });
          if(rendered.length) {
            rendered[0].id = data.id;
            $('#calendar').fullCalendar('updateEvent', rendered[0]);
          }
        });
    }
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