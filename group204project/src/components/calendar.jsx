import React from 'react';
import FullCalendar from '@fullcalendar/react'; // must go before plugins
import timeGridPlugin from '@fullcalendar/timegrid'; // a plugin!

export default class Calendar extends React.Component {
  render() {
    return (
      <FullCalendar
        plugins={[timeGridPlugin]}
        initialView="timeGrid"
        dayCount={5}
        dayHeaderFormat={{ weekday: 'long' }}
        stickyHeaderDates
        weekends={false}
        headerToolbar={false}
        allDaySlot={false}
        showNonCurrentDates
        initialDate="2022-10-31"
        handleWindowResize
        slotMinTime="08:00"
        slotMaxTime="24:00"
        aspectRatio={1.5}
      />
    );
  }
}
