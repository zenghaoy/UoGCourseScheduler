import React from 'react';

function CourseListItem(props) {
  const { course } = props;
  const { handleRemoveCourses } = props;
  const { removeEvent } = props;
  const { handleSearchOtherSections } = props;

  function checkButton(locCourse) {
    handleRemoveCourses(locCourse);
    removeEvent(locCourse);
  }

  function searchForOtherSections(locCourse) {
    handleSearchOtherSections(locCourse);
  }

  const removeButtonOnClick = checkButton;
  const searchForSimilarSections = searchForOtherSections;

  return (
    <div className="list-group-item">
      <div className="d-flex flex-wrap">
        <div>
          {course.course_code}
          *
          {course.section_code}
        </div>
        <div className="ms-auto">
          <button
            type="button"
            className="btn btn-primary"
            id="searchSimButton"
            onClick={() => searchForSimilarSections(course)}
          >
            Sections
          </button>
          <button
            type="button"
            className="btn-remove btn btn-danger"
            id="removeButton"
            onClick={() => removeButtonOnClick(course)}
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  );
}
export default CourseListItem;
