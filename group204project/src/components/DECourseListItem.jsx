import React from 'react';

function DECourseListItem(props) {
  const { course } = props;
  if (course.section_code.includes('DE')) {
    return (
      <div className="de-list-course-item">
        (Distance Education)
        {' '}
        {course.course_code}
        *
        {course.section_code}
        {' '}
        -
        {' '}
        {course.course_name}
      </div>
    );
  }
  return ('');
}
export default DECourseListItem;
