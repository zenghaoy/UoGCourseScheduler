import $ from "jquery";
import React, { createContext, useState } from "react";
import FullCalendar from "@fullcalendar/react"; // must go before plugins
import Modal from "react-bootstrap/Modal";
import ReactSwitch from "react-switch";

import Select from "react-select";
import timeGridPlugin from "@fullcalendar/timegrid"; // a plugin!
import ClassCard from "./components/classCard";
import CourseList from "./components/courseList";
import DECourseList from "./components/DECourseList";

export const ThemeContext = createContext(null);

let courses = [];
const semestersList = [];
let winter23 = [];
let fall22 = [];
let searchedCourses = [];
let eventData;
const options = [
  { value: "2022-11-07", label: "Monday" },
  { value: "2022-11-08", label: "Tuesday" },
  { value: "2022-11-09", label: "Wednesday" },
  { value: "2022-11-10", label: "Thursday" },
  { value: "2022-11-11", label: "Friday" },
];

//initialization
$(() => {
  async function fetchJson(pUrl) {
    const response = await fetch(pUrl, { method: "GET" });
    const lists = await response.json();
    return lists;
  }

  (async () => {
    let c = await fetchJson("https://cis3760team204.com/api/winter23");
    winter23 = c.sections;
    c = await fetchJson("https://cis3760team204.com/api/fall22");
    fall22 = c.sections;
    semestersList.push({ key: 1, value: winter23 });
    semestersList.push({ key: 0, value: fall22 });
    courses = fall22;
    console.log(courses);
  })();
});

/*
// use to our advantage that course codes are alphabetical order
function binaryCourseCodeSearch(searchTerm) {
  function binsearch(search, s, e) {
    if (s > e) return -1;

    const mid = Math.floor((s + e) / 2);
    const midstr = courses[mid].course_code;

    if (midstr.startsWith(search)) {
      return mid;
    }
    let i = 0;
    while (i < midstr.length && i < search.length && midstr[i].localeCompare(search[i]) === 0) {
      i += 1;
    }
    const compr = midstr[i].localeCompare(search[i]);
    if (compr > 0) {
      return binsearch(search, s, mid - 1);
    } if (compr < 0) {
      return binsearch(search, mid + 1, e);
    }
    return null;
  }

  const idx = binsearch(searchTerm, 0, courses.length - 1);
  if (idx < 0) {
    return [];
  }

  const ret = [];
  const n = courses.length;

  // since we are looking for a list and not a single result, look before
  let b = idx;
  while (b > -1 && courses[b].course_code.startsWith(searchTerm)) {
    ret.unshift(courses[b]);
    b -= 1;
  }

  // look after
  let a = idx + 1;
  while (a < n && courses[a].course_code.startsWith(searchTerm)) {
    ret.push(courses[a]);
    a += 1;
  }
  return ret;
} */

// use linear search because need to search by both code and name
function linSearch(searchTerm) {
  const ret = [];
  for (let i = 0; i < courses.length; i += 1) {
    if (courses[i].course_code.includes(searchTerm)) {
      ret.push(courses[i]);
    } else if (
      courses[i].course_name.toUpperCase().includes(searchTerm.toUpperCase())
    ) {
      ret.push(courses[i]);
    }
  }
  return ret;
}

function App() {
  const [searchcourses, setSearchCourses] = useState([]);
  const [displayMsg, setDisplayMsg] = useState([""]);
  const [searchTerm, setSearchTerm] = useState("");
  const [prevSearch, setPrevSearch] = useState("");
  const [events, setEvents] = useState([[], []]);
  const [eventsDisplay, setEventsDisplay] = useState([]);
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [selectedSemesterCourses, setSelectedSemesterCourses] = useState([
    [],
    [],
  ]);
  const [distEdCourses, setSelectedDistEdCourses] = useState([]);
  const [selectedDistEdCoursesSemester, setSelectedDistEdCoursesSemester] =
    useState([]);
  const [selectedSemester, setSelectedSemester] = useState(0);
  const [daysOff, setDaysOff] = useState([]);
  const [show, setShow] = useState(false);
  const [readerSetup, setReaderSetup] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const semesters = [
    { key: "Fall 2022", value: 0 },
    { key: "Winter 2023", value: 1 },
  ];

  function setCourses(x) {
    setSelectedCourses(x);
  }

  function setDistEdCourses(x) {
    if (x.section_code.includes("DE")) {
      setSelectedDistEdCourses(x);
    }
    console.log(distEdCourses);
  }

  function updateSelectedCourse(x, y, semIndex) {
    const selectedCourse = [...selectedSemesterCourses];
    const selectedDECourse = [...selectedDistEdCoursesSemester];
    selectedCourse[semIndex] = x.slice();
    selectedDECourse[semIndex] = y.slice();
    setSelectedSemesterCourses(selectedCourse);
    setSelectedDistEdCoursesSemester(selectedDECourse);
    // console.log(semIndex);
    // console.log(selectedCourse);
  }

  function isOverlapRem(element, locEvents) {
    let lap = false;
    locEvents.forEach((eve) => {
      if (
        Date.parse(element.start) <= Date.parse(eve.end) &&
        Date.parse(element.end) >= Date.parse(eve.start) &&
        element.id !== eve.id
      ) {
        lap = true;
      }
    });
    return lap;
  }

  function removeEvent(course) {
    const updatedEvents = [...events];
    const semIndex = selectedSemester;
    for (let i = updatedEvents[semIndex].length - 1; i >= 0; i -= 1) {
      if (
        updatedEvents[semIndex][i].course_code === course.course_code &&
        updatedEvents[semIndex][i].section_code === course.section_code
      ) {
        updatedEvents[semIndex].splice(i, 1);
      }
    }
    updatedEvents.forEach((eve) => {
      if (!isOverlapRem(eve, events[semIndex])) {
        eve.color = "#3788d8";
      }
    });

    setEvents(updatedEvents);
    setEventsDisplay(updatedEvents[semIndex].slice());
  }

  function generatePDF() {
    const searchCourse = document.getElementById("searchCourse");
    searchCourse.style.display = "none";
    const themeColour = document.getElementById("themeColour");
    themeColour.style.display = "none";
    const helpSection = document.getElementById("helpSection");
    helpSection.style.display = "none";
    const displayArea = document.getElementById("display_area");
    if (typeof displayArea !== "undefined" && displayArea !== null) {
      displayArea.style.display = "none";
    }
    const emptySearchMsg = document.getElementById("emptySearchMsg");
    if (typeof emptySearchMsg !== "undefined" && emptySearchMsg !== null) {
      emptySearchMsg.style.display = "none";
    }
    const submitButton2 = document.getElementById("submitButton2");
    submitButton2.style.display = "none";

    window.print();

    searchCourse.style.display = "block";
    themeColour.style.display = "block";
    helpSection.style.display = "block";
    if (typeof displayArea !== "undefined" && displayArea !== null) {
      displayArea.style.display = "block";
    }
    if (typeof emptySearchMsg !== "undefined" && emptySearchMsg !== null) {
      emptySearchMsg.style.display = "block";
    }
    submitButton2.style.display = "block";
  }

  function screenReaderSetup() {
    const msg = new SpeechSynthesisUtterance();
    const tags = document.querySelectorAll("h1, p");
    tags.forEach((tag) => {
      tag.addEventListener("click", (e) => {
        msg.text = e.target.innerText;
        speechSynthesis.speak(msg);
      });
    });
  }

  function screenReaderStart() {
    speechSynthesis.cancel();
    speechSynthesis.resume();
    if (!readerSetup) {
      screenReaderSetup();
      setReaderSetup(true);
    }
  }

  function screenReaderStop() {
    speechSynthesis.cancel();
    speechSynthesis.pause();
  }
  // function getAllEvent(){
  //   let updatedEvents = [...events];
  //   console.log("getAllEvent "+ updatedEvents.length);
  //   console.log(updatedEvents);
  // }
  const eventpopup = (eve) => {
    // eslint-disable-next-line
    const courseCode = eve.event._def.extendedProps.course_code;
    // eslint-disable-next-line
    const section = eve.event._def.extendedProps.section_code;
    const eventDataT = courses.filter(
      (course) =>
        course.course_code === courseCode && course.section_code === section
    );
    // eslint-disable-next-line
    eventData = eventDataT[0];
    // console.log(eventData);
    handleShow();
  };

  function handleRemoveCourses(course) {
    const copy = selectedCourses;
    let removeIndex = 0;
    for (let i = 0; i < copy.length; i += 1) {
      if (
        copy[i].course_code === course.course_code &&
        copy[i].section_code === course.section_code
      ) {
        removeIndex = i;
      }
      if (copy[i].section_code.includes("DE")) {
        // numDESelected -= 1;
      }
    }
    copy.splice(removeIndex, 1);
    setSelectedCourses(copy);
    // removeEvent(course);
    // const container = document.getElementById('selected-courses');
    // render(<>Selected Courses:
    //  {copy.map((m) => <div>{m.course_code}*{m.section_code}
    //  <button type="button" className="btn btn-danger"
    //  id="removeButton"
    //  onClick={e => RemoveButtonOnClick(e, m,  handleRemoveCourses,removeEvent)}>Remove</button>
    //  </div>)}</>,container);
  }

  function handleSearch() {
    console.log("handle search");
    const searchTerms = searchTerm.split(" ");

    if (searchTerm !== "") {
      console.log(prevSearch);
      searchedCourses = [];
      if (typeof searchTerms[0] !== "undefined") {
        searchedCourses = linSearch(searchTerms[0].toUpperCase());
      }
      if (typeof searchTerms[1] !== "undefined") {
        searchedCourses = searchedCourses.filter((x) =>
          x.section_code.includes(searchTerms[1])
        );
      }

      if (searchedCourses.length === 0) {
        setDisplayMsg([`The search term '${searchTerm}' yielded no results.`]);
      } else {
        setDisplayMsg([""]);
      }
    }
    setPrevSearch(searchTerm);
    setSearchCourses(searchedCourses);
  }

  function changeSemester(e) {
    console.log("changed sem: " + e.target.value);
    const updatedEvents = [...events];
    const semIndex = parseInt(e.target.value, 10);
    const newSelectedCourses = [...selectedSemesterCourses][semIndex].splice();
    // save current "selectedCourses" to backend array.
    updateSelectedCourse(selectedCourses, distEdCourses, selectedSemester);

    // change semester to new semester
    setSelectedSemester(semIndex);

    // populate "selectedCourses" from backend array.
    setSelectedCourses(selectedSemesterCourses[semIndex]);

    // populate searchCourses, EventDisplay.
    setSearchCourses(newSelectedCourses[semIndex]);
    setEventsDisplay(updatedEvents[semIndex].slice());
    courses = semestersList.find((x) => x.key === semIndex).value;
    setSearchCourses([]);
    console.log("searchedCourses" + searchcourses.length);
  }

  function handleChange(e) {
    //console.log(e.target.value);
    setSearchTerm(e.target.value);
  }

  function handleSearchOtherSections(course) {
    document.getElementById("searchCourse").value = course.course_code;
    setSearchTerm(document.getElementById("searchCourse").value);
    document.getElementById("submitButton2").click();
    handleSearch();
  }

  function isOverlap(element, locEvents) {
    let lap = false;
    locEvents.forEach((eve) => {
      if (
        Date.parse(element.start) <= Date.parse(eve.end) &&
        Date.parse(element.end) >= Date.parse(eve.start)
      ) {
        lap = true;
      }
    });
    return lap;
  }

  function addEvent(eventJson) {
    const updatedEvents = [...events];
    const semIndex = selectedSemester;
    eventJson.forEach((element) => {
      if (isOverlap(element, events[semIndex])) {
        element.color = "#FF0000";
      }
      updatedEvents[semIndex].push(element);
    });
    setEvents(updatedEvents);
    setEventsDisplay(updatedEvents[semIndex].slice());
    // console.log(eventsDisplay);
  }

  const handleDayChange = (event) => {
    setDaysOff(event);
  };

  function updateDate(day) {
    let vret;
    if (day.endsWith("AM")) {
      vret = day.replace("AM", ":00");
    } else if (day.endsWith("PM") && day.substring(0, 2) === "12") {
      vret = day.replace("PM", ":00");
    } else {
      vret = day.replace("PM", ":00");
      vret = parseInt(vret.substring(0, 2), 10) + 12 + vret.substring(2);
    }
    return vret;
  }

  function genEvents() {
    const semIndex = selectedSemester;
    let count = 5 - selectedCourses.length;
    let cnum;
    while (count > 0) {
      cnum = Math.floor(Math.random() * (3065 - 0 + 1)) + 0;
      const c = courses[cnum];
      if (c !== null && c !== undefined) {
        const code = c.course_code;
        const sectioncode = c.section_code;
        const meetingInfo = c.meeting_information;
        const eventObj = [];
        let isValid = true;
        if (meetingInfo) {
          if (
            meetingInfo[0].type !== "Distance" &&
            meetingInfo[0].days === "TBA"
          ) {
            isValid = false;
          }
          const lecLab = meetingInfo.filter(
            (d) =>
              (d.type === "LEC" || d.type === "LAB" || d.type === "SEM") &&
              d.time !== "TBA"
          );
          lecLab.forEach((element) => {
            const times = element.time.split("-");
            const timeStart = updateDate(times[0]);
            const timeEnd = updateDate(times[1]);
            element.days.forEach((d) => {
              let day;
              // eslint-disable-next-line default-case
              switch (d) {
                case "Mon":
                  day = "2022-11-07";
                  break;
                case "Tues":
                  day = "2022-11-08";
                  break;
                case "Wed":
                  day = "2022-11-09";
                  break;
                case "Thur":
                  day = "2022-11-10";
                  break;
                case "Fri":
                  day = "2022-11-11";
                  break;
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
        } else {
          isValid = false;
        }
        selectedCourses.forEach((element) => {
          if (element.course_code === c.course_code) {
            isValid = false;
          }
        });
        for (let i = 0; i < eventObj.length; i += 1) {
          const element = eventObj[i];
          if (isOverlap(element, events[semIndex])) {
            isValid = false;
          }
          for (let j = 0; j < daysOff.length; j += 1) {
            const day = daysOff[j];
            if (element.start !== undefined && element.start !== null) {
              const day2 = element.start.split("T")[0];
              if (day2 === day.value) {
                isValid = false;
              }
            }
          }
        }
        if (isValid) {
          // console.log(c);
          selectedCourses.push(c);
          setSelectedCourses(selectedCourses);
          count -= 1;
          addEvent(eventObj);
        }
      }
    }
  }

  const [theme, setTheme] = useState("dark");

  const toggleTheme = () => {
    setTheme((curr) => (curr === "light" ? "dark" : "light"));
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <div className="App" id={theme}>
        <div className="background">
          <main className="px-3 main">
            <div className="container">
              <div className="row">
                <div className="title">
                  <h1>Course Scheduler</h1>
                </div>
                <div className="switch">
                  <p className="switch-label" id="themeColour">
                    Theme:{" "}
                  </p>
                  <ReactSwitch
                    onChange={toggleTheme}
                    checked={theme === "dark"}
                  />
                </div>
                <div className="d-flex flex-wrap">
                  <div className="col-4 left-column">
                    <div className="d-flex flex-column">
                      <div className="helpSection" id="helpSection">
                        <p>
                          <div className="d-flex justify-content-between screen-style">
                            <div className="switch-label" id="screenReader">
                              Screen Reader:
                            </div>
                            <div className="form-check" id="startButton">
                              <input
                                className="form-check-input"
                                type="radio"
                                name="flexRadioDefault"
                                id="flexRadioDefault1"
                                onClick={(e) => screenReaderStart(e)}
                              />
                              <div className="switch-label">Start</div>
                            </div>
                            <div className="form-check" id="stopButton">
                              <input
                                className="form-check-input"
                                type="radio"
                                name="flexRadioDefault"
                                id="flexRadioDefault1"
                                onClick={(e) => screenReaderStop(e)}
                              />
                              <div className="switch-label">Stop</div>
                            </div>
                          </div>
                        </p>
                        <br />
                        <p>
                          <a
                            target="_blank"
                            rel="noreferrer noopener"
                            href="https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/"
                          >
                            <b>View All Courses Here</b>
                          </a>
                        </p>
                        <p>
                          <a
                            target="_blank"
                            rel="noreferrer noopener"
                            href="https://docs.google.com/document/d/1W_r34yZ49-1PSVUQPxVHFEgMuL_hSTQ0W44V_SreGzA/edit?usp=sharing"
                          >
                            <b>View User Guide</b>
                          </a>
                        </p>
                      </div>
                      <hr />
                      <p>
                        <div className="switch-label">Semester:</div>
                      </p>
                      <div className="genSection">
                        <p>
                          <select
                            onChange={(e) => changeSemester(e)}
                            defaultValue="Fall 2022"
                            className="form-select form-select-sm"
                          >
                            {semesters.map((sem) => (
                              <option key={sem.key} value={sem.value}>
                                {sem.key}
                              </option>
                            ))}
                          </select>
                          <hr />
                          {selectedCourses.length !== 0 ? (
                            <div className="selected-label">
                              Selected Courses:
                            </div>
                          ) : (
                            <div />
                          )}
                          <ul className="list-group">
                            <CourseList
                              selectedCourses={selectedCourses}
                              handleRemoveCourses={handleRemoveCourses}
                              removeEvent={removeEvent}
                              handleSearchOtherSections={
                                handleSearchOtherSections
                              }
                            />
                          </ul>
                          {selectedCourses.length !== 0 ? <hr /> : <div />}
                          <div className="switch-label">
                            Generate Schedule with Days Off:
                          </div>
                          <div className="weekday" id="genSchedule">
                            <Select
                              onChange={(e) => handleDayChange(e)}
                              className="weekday-dropdown"
                              placeholder="Select days off..."
                              options={options}
                              isMulti
                            />
                            <br />
                            <button
                              id="genButton"
                              type="button"
                              className="btn btn-primary"
                              onClick={(e) => genEvents(e)}
                            >
                              Generate Schedule
                            </button>
                          </div>
                        </p>
                      </div>
                      <hr />
                      <div className="searchSection">
                        <p>
                          <div className="label-input">
                            <div className="input-group">
                              <input
                                type="text"
                                className="form-control width100"
                                id="searchCourse"
                                placeholder="Enter course code here"
                                onChange={(e) => handleChange(e)}
                              />
                              <span className="input-group-btn">
                                <button
                                  id="submitButton2"
                                  type="button"
                                  className="btn btn-primary"
                                  onClick={(e) => handleSearch(e)}
                                >
                                  Search
                                </button>
                              </span>
                            </div>
                          </div>
                          <Modal show={show} onHide={handleClose}>
                            <div className="modal-pre" id={theme}>
                              <div className="modal-style">
                                <Modal.Header closeButton>
                                  <Modal.Title>Course Info</Modal.Title>
                                </Modal.Header>
                                <Modal.Body>
                                  <div>
                                    <span>
                                      {"Course:   "}
                                      {eventData?.course_name}{" "}
                                      {eventData?.course_code}{" "}
                                      {eventData?.section_code}
                                    </span>
                                    <br />
                                    <span>
                                      {"Course Level:   "}
                                      {eventData?.academic_level}
                                    </span>
                                    <br />
                                    <span>
                                      {"Credits:   "}
                                      {eventData?.credits}
                                    </span>
                                    <br />
                                    <span>
                                      {"Professor:   "}
                                      {eventData?.faculty}
                                    </span>
                                    <br />
                                    <span>
                                      {"Location:   "}
                                      {eventData?.location} {eventData?.term}
                                    </span>
                                    <br />
                                    <span>
                                      {"Status:   "}
                                      {eventData?.status}
                                    </span>
                                    <br />
                                    <span>
                                      {"Capacity:   "}
                                      {eventData?.available_capacity}/
                                      {eventData?.max_capacity}
                                    </span>
                                    <br />
                                  </div>
                                </Modal.Body>
                                <Modal.Footer>
                                  <button
                                    type="button"
                                    className="btn btn-danger"
                                    onClick={handleClose}
                                  >
                                    Close
                                  </button>
                                </Modal.Footer>
                              </div>
                            </div>
                          </Modal>
                          {searchcourses.length !== 0 ? (
                            <div className="course-display" id="display_area">
                              <br />
                              {displayMsg.map((m) => (
                                <div key={m}>{m}</div>
                              ))}
                              {searchcourses.map((c) => (
                                <ClassCard
                                  addEvent={addEvent}
                                  removeEvent={removeEvent}
                                  remove={handleRemoveCourses}
                                  setSelectedCourses={setCourses}
                                  selectedCourses={selectedCourses}
                                  course={JSON.stringify(c)}
                                  key={c.section_number}
                                  selectedSemester={selectedSemester}
                                />
                              ))}
                            </div>
                          ) : (
                            <div className="search-label" id="emptySearchMsg">
                              Search for Courses!
                            </div>
                          )}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="col-8" id="canvas">
                    <p>
                      <div className="d-flex flex-column">
                        <div className="ms-auto">
                          <button
                            id="pdfButton"
                            type="button"
                            className="btn btn-primary"
                            onClick={(e) => generatePDF(e)}
                          >
                            Generate PDF
                          </button>
                        </div>
                        <br />
                        <div>
                          <DECourseList
                            selectedCourses={selectedCourses}
                            setSelectedCourses={setDistEdCourses}
                          />
                        </div>
                        <br />
                        <div>
                          <FullCalendar
                            plugins={[timeGridPlugin]}
                            initialView="timeGrid"
                            dayCount={5}
                            dayHeaderFormat={{ weekday: "long" }}
                            stickyHeaderDates
                            weekends={false}
                            initialDate="2022-11-07"
                            headerToolbar={false}
                            allDaySlot={false}
                            showNonCurrentDates
                            handleWindowResize
                            slotMinTime="07:00"
                            slotMaxTime="24:00"
                            events={eventsDisplay}
                            height="auto"
                            width="auto"
                            eventClick={eventpopup}
                          />
                        </div>
                        {/* <p>{testInnerArray}</p> */}
                      </div>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </ThemeContext.Provider>
  );
}

export default App;
