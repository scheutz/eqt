DROP TABLE IF EXISTS CoursePart_ScheduleCode;
DROP TABLE IF EXISTS Course_Profile;
DROP TABLE IF EXISTS ScheduleCode;
DROP TABLE IF EXISTS CoursePart;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Profile;


CREATE TABLE "Course" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "course_code" VARCHAR(100) UNIQUE NOT NULL,
  "course_name" TEXT NOT NULL,
  "advancement_level" VARCHAR(10) NOT NULL,
  "credits" INTEGER
);

CREATE TABLE "CoursePart" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "semester" INTEGER,
  "term" INTEGER,
  "course" INTEGER NOT NULL REFERENCES "Course" ("id")
);

CREATE INDEX "idx_coursepart_semester" ON "CoursePart" ("semester");
CREATE INDEX "idx_coursepart_semesterterm" ON "CoursePart" ("semester", "term");
CREATE INDEX "idx_coursepart__course" ON "CoursePart" ("course");

CREATE TABLE "Profile" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "name" VARCHAR(50) NOT NULL,
  "abbreviation" VARCHAR(10) NOT NULL,
  "type" VARCHAR(20) NOT NULL,
  "programme" VARCHAR(50) NOT NULL,
  "university" VARCHAR(50) NOT NULL
);

CREATE INDEX "idx_profile_name" ON "Profile" ("abbreviation");
CREATE INDEX "idx_profile_nameprogramme" ON "Profile" ("abbreviation", "programme");


CREATE TABLE "Course_Profile" (
  "course" INTEGER NOT NULL REFERENCES "Course" ("id"),
  "profile" INTEGER NOT NULL REFERENCES "Profile" ("id"),
  "required" BOOLEAN NOT NULL,
  PRIMARY KEY ("course", "profile")
);

CREATE INDEX "idx_course_profile__profile" ON "Course_Profile" ("profile");

-- Code = 0 represents that code is not applicable
CREATE TABLE "ScheduleCode" (
  "schedule_code" INTEGER NOT NULL,
  "course_part" INTEGER NOT NULL REFERENCES "CoursePart" ("id"),
  PRIMARY KEY ("schedule_code", "course_part")
);



