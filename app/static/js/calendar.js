var checkbox = document.getElementById('drop-remove');
var modal = document.getElementById('event-modal');
var infoModal = document.getElementById('info-modal');
var currentEvent = null;
var editingEventId = null;
var currentLinkedClass= null;


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
    document.getElementById('modal-public').checked = !!prefill.is_public;
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
  document.getElementById('modal-public').checked = false;
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

  var visDiv = document.getElementById('info-visibility');
  if (event.id) {
    visDiv.style.display = 'block';
    document.getElementById('info-public-toggle').checked = !!event.is_public;
  } else {
    visDiv.style.display = 'none';
  }
  infoModal.classList.add('open');
}

document.getElementById('info-public-toggle').addEventListener('change', function() {
  if (!currentEvent || !currentEvent.id) return;
  fetch('/events/' + currentEvent.id + '/visibility', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ is_public: this.checked ? 1 : 0 })
  }).then(function() {
    currentEvent.is_public = document.getElementById('info-public-toggle').checked ? 1 : 0;
  });
});

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

function saveEventToServer(title, start, end, color, linkedClass, allDay, isPublic) {
  return fetch('/events', {
    method: 'POST',
    headers: { "Content-Type": 'application/json'},
    body: JSON.stringify({ title: title, start:start, end: end, color: color, linked_class: linkedClass, allDay: allDay, is_public: isPublic ? 1 : 0})
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
    defaultView: 'month',
    header: {
      left: 'prev,next today addEventButton',
      center: 'title',
      right: 'month,agendaWeek,agendaDay,listDay,listWeek'
    },
    views:{
      listDay: {
        type: "listDay",
        buttonText: "To-Do"
      },
      listWeek: {
        type: "listWeek",
        buttonText: "To-Do(Week)"
      }
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
      saveEventToServer(event.title, start, null, '#3a87d3', null, allDay, false)
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
  
   fetch('/shared-events')
    .then(function(r) { return r.json(); })
    .then(function(events) {
      var list = document.getElementById('shared-event-list');
      if (!events.length) return; 
      list.innerHTML = '';
      events.forEach(function(e) {
        var div = document.createElement('div');
        div.className = 'shared-event-item';
        div.innerHTML =
          '<strong>' + e.title + '</strong><br>' +
          '<small>' + e.start + '</small><br>' +
          '<button class="accept-btn">Add to my calendar</button>';
        div.querySelector('.accept-btn').addEventListener('click', function() {
          saveEventToServer(e.title, e.start, e.end, e.color, e.linked_class, e.allDay, false)
            .then(function(data) {
              $('#calendar').fullCalendar('renderEvent', {
                id: data.id,
                title: e.title,
                start: e.start,
                end: e.end,
                color: e.color,
                allDay: e.allDay
              }, true);
              div.querySelector('.accept-btn').textContent = '✓ Added';
              div.querySelector('.accept-btn').disabled = true;
            });
        });
        list.appendChild(div);
      });
    });

  document.getElementById('modal-edit').addEventListener('click', function() {
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
    var isPublic = document.getElementById('modal-public').checked ? 1 : 0;

    if (!title) {alert('Please enter an event name.'); return; }
    if(!startDate) {alert('Please select a date.'); return; }
    if (isPublic && !linkedClass) {alert('Please link a class to share this event publicly.'); return; }

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
                       color: color, linked_class: linkedClass, 
                       allDay: allDay, is_public: isPublic })  
      }).then(function() {
        $('#calendar').fullCalendar('removeEvents', String(editingEventId));
        $('#calendar').fullCalendar('renderEvent', {
          id: String(editingEventId),
          title: title,
          start: start,
          end: end,
          allDay: allDay,
          color: color,
          linked_class: linkedClass,
          is_public: isPublic
        }, true);
      });
    } else {
      $('#calendar').fullCalendar('renderEvent', {
        title: title,
        start: start,
        end: end,
        allDay: allDay,
        color: color,
        linked_class: linkedClass,
        is_public: isPublic
      }, true);

      saveEventToServer(title, start, end, color, linkedClass, allDay, isPublic)
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
  $('#external-events').append($el); 
  makeDraggable($el[0]);

  input.value = '';
  input.focus();
}
});
