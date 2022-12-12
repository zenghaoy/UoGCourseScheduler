import React from 'react';
import AddButtonOnClick from './addButton';
// Should also display meeting times?
function updateDate(day) {
  let vret;
  if (day.endsWith('AM')) {
    vret = day.replace('AM', ':00');
  } else if (day.endsWith('PM') && day.substring(0, 2) === '12') {
    vret = day.replace('PM', ':00');
  } else {
    vret = day.replace('PM', ':00');
    vret = (parseInt(vret.substring(0, 2), 10) + 12) + vret.substring(2);
  }

  return vret;
}
export default function ClassCard(props) {
  const prop = props;
  const c = JSON.parse(prop.course);
  const code = c.course_code;
  const name = c.course_name;
  const sectioncode = c.section_code;
  const meetingInfo = c.meeting_information;
  const eventObj = [];
  let listItems;
  // const eventObj = [{
  //     title:code,
  //     date:'2022-11-07T08:00:00',
  // }]
  if (meetingInfo) {
    const lecLab = meetingInfo.filter((d) => (d.type === 'LEC' || d.type === 'LAB' || d.type === 'SEM') && d.time !== 'TBA');
    lecLab.forEach((element) => {
      const times = element.time.split('-');
      const timeStart = updateDate(times[0]);
      const timeEnd = updateDate(times[1]);
      element.days.forEach((d) => {
        let day;
        // eslint-disable-next-line default-case
        switch (d) {
          case 'Mon': day = '2022-11-07'; break;
          case 'Tues': day = '2022-11-08'; break;
          case 'Wed': day = '2022-11-09'; break;
          case 'Thur': day = '2022-11-10'; break;
          case 'Fri': day = '2022-11-11'; break;
        }
        eventObj.push({
          title: `${code} ${element.type}`,
          start: `${day}T${timeStart}`,
          end: `${day}T${timeEnd}`,
          course_code: code,
          section_code: sectioncode,
          full_time: element.time,
          time0: times[0],
          time1: times[1],
        });
      });
    });

    listItems = lecLab.map((d) => (
      <div>
        <p>
          <b>Type:</b>
          {' '}
          <span>
            {' '}
            {d.type}
            {' '}
          </span>
        </p>
        <p>
          <b>
            Times:
            {d.days}
          </b>
          {' '}
          <span>
            {' '}
            {d.time}
            {' '}
          </span>
        </p>
      </div>
    ));
  }

  let sectionnumber = c.section_number.toString();
  sectionnumber = sectionnumber.slice(1, sectionnumber.length - 1);
  const { term } = c;

  return (
    <div key={sectioncode} className="form-group container" id="display_area">
      <div className="row">
        <div className="col">
          <div className="card w-100">
            <div className="card-body">
              <p>
                <b>Course Code:</b>
                {' '}
                <span>
                  {' '}
                  {code}
                  {' '}
                </span>
              </p>
              <p>
                <b>Course Name:</b>
                {' '}
                <span>
                  {' '}
                  {name}
                  {' '}
                </span>
              </p>
              <p>
                <b>Section Code:</b>
                {' '}
                <span>
                  {' '}
                  {sectioncode}
                  {' '}
                </span>
              </p>
              <p>
                <b>Section Number:</b>
                {' '}
                <span>
                  {' '}
                  {sectionnumber}
                  {' '}
                </span>
              </p>
              <p>
                <b>Term:</b>
                {' '}
                <span>
                  {' '}
                  {term}
                  {' '}
                </span>
              </p>
              {listItems}
              <button
                type="button"
                className="btn btn-success"
                id="addButton"
                onClick={(e) => AddButtonOnClick(e, props, eventObj)}
              >
                Add
              </button>
            </div>
          </div>
        </div>
      </div>
      <br />
    </div>
  );
}
