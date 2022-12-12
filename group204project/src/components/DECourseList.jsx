import React from 'react';
import DECourseListItem from './DECourseListItem';

function DECourseList({ selectedCourses }) {
  return (
    selectedCourses.map((course) => {
      if (selectedCourses.length) {
        return (
          <DECourseListItem
            course={course}
            key={Math.random(100000)}
          />
        );
      }
      return ('');
    })
  );
}

export default DECourseList;

// course = props.course
// handleRemoveCourses = props.handleRemoveCourses
// removeEvent = props.removeEvent
