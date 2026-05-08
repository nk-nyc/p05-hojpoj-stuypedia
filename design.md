## TEAM HOJPOJ
## STUYPEDIA

### TARGET SHIP DATE: 06/15/26
| name | email | primary role |
| ----|----|---|
| Natalie Keiger | nataliek54@nycstudents.net | PM, backend & data |
| Sophia Chi | sophiac188@nycstudents.net | Devo, frontend |
| Michelle Chen | michellec397@nycstudents.net | Devo, backend |

# SUMMARY
Stuypedia is a website specific for Stuyvesant students. Thie website allows students to view data about their classes and teachers. Data will be from previous students who had the class and filled out the google form survey. Students can also access a calendar with a task manager.

## PROBLEM BEING SOLVED

## TARGET USERS

## WHY THIS PROJECT MATTERS

# MVP SCOPE

## MVP FEATURES

## STRETCH FEATURES

## EXPLICIT NON-GOALS

# DATA COLLECTION, USAGE & SECURITY
Part of our project is the collection and use of data. To ensure security for students’ accounts, we will hash passwords and store everything under an anonymous username tied to their true username (NYCDOE user).

| key  | type |  notes    |
|-------|-----|-------|
| user | TEXT  | must be unique |
| pass   | TEXT  | will be stored as a hash   |
| anon_user | TEXT  | anonymous username generated for users to be displayed |
| id (PK) | INTEGER  | must be unique |

In order to verify a user, they must answer a series of stuy-related questions (for now, subject to change) Once verified, a student is given an anonymous username (like on Piazza) but their login remains their NYCDOE user and chosen password.

## ACQUISITION OF DATA

Our data will be collected primarily from existing users. When a user signs in, they are first prompted to add five classes that they have either taken or are currently taking and must answer a series of questions about those classes. From there, they are able to view data trends in any classes and can select for classes that they may want to take. Data to start out the website will come from a Google form we will share.

## SPECIFIC DATA

For each teacher's section of each class, we hope to collect:
* Average homework workload (hrs)
* Average difficulty (1-5)
* Average enjoyment (1-5)
* Average test difficulty (1-5)
* Resources they found helpful (will be a list of options for them to check off)
* Overall rating (1-5)

These data will be displayed to students when they view each class section. Additionally, we will allow students to add to a collective **calendar**.

# TECHNOLOGY STACK 
| layer | tools |
| ---- | ----|
| Database | SQlite |
| Frontend Framework | undecided |
| Authentication | flask sessions |
| Backend | .... |

## CALENDAR

The calendar will be student-managed. Students can select whether the day is an A or B day and which type as well as what time schedule the day has. In addition to that, students can create **events** in categories such as test, project due date, AP, and celebration. Students will be able to verify other users' events or report them if they are innacurate. All students will be able to view the collective calendar and filter it for which classes they want to view.

## DATA STORAGE

We will use MongoDB for its flexibility in data storage. Each class will be a collection of nested documents containing individual reviews. Review documents will look like the following:
```
{
  _id: '0239d987ash39287hsd',
  class: 'AP Biology',
  teacher: 'Maggio',
  date_issued: 05-07-2026,
  homework: 4,
  difficulty: 5,
  enjoyment: 4,
  test_diff: 2,
  resources: ['quizlet', 'amoeba sisters'],
  overall: 4

}
```

These documents will be stored by class in collections. Students will be able to view trends in data for each class and teacher pair.

# TASKS
| task | name | due date | status |
|-----|----|-----|----|
| design.md | everyone | 5/11 | 🟡 in progress 🟡 |
| | | | |
| | | | |
| | | | |
