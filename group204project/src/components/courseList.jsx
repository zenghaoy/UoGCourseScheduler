import React from 'react';
import CourseListItem from './courseListItem';

function CourseList(
  {
    selectedCourses,
    handleRemoveCourses,
    removeEvent,
    handleSearchOtherSections,
  },
) {
  return (
    selectedCourses.map((course) => (
      <CourseListItem
        course={course}
        handleRemoveCourses={handleRemoveCourses}
        removeEvent={removeEvent}
        handleSearchOtherSections={handleSearchOtherSections}
        key={Math.random(100000)}
      />
    ))
  );
}

export default CourseList;

// course = props.course
// handleRemoveCourses = props.handleRemoveCourses
// removeEvent = props.removeEvent
