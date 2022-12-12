// import { render } from "react-dom";
// import { searchedCourses } from "../App";

export default function AddButtonOnClick(e, props, eventObj) {
  // props contains a json object that should also contain the meeting times, etc

  const c = JSON.parse(props.course);
  let copy = [];
  copy = props.selectedCourses;
  let sameCourse = false;

  copy.forEach((element) => {
    if (element.course_code === c.course_code && element.section_code === c.section_code) {
      sameCourse = true;
    }
  });

  if (copy.length >= 5) {
    window.alert('Cannot have more than 5 courses added.');
  } else if (sameCourse) {
    window.alert('Cannot add the same course twice.');
  } else {
    copy.push(c);
    props.setSelectedCourses(copy);
    props.addEvent(eventObj);
  }
}
