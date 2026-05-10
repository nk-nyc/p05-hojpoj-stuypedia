## TEAM HOJPOJ
## STUYPEDIA

### TARGET SHIP DATE: 06/15/26
| name | email | primary role |
| ----|----|---|
| Natalie Keiger | nataliek54@nycstudents.net | PM, backend & data |
| Sophia Chi | sophiac188@nycstudents.net | Devo, frontend |
| Michelle Chen | michellec397@nycstudents.net | Devo, backend |

# SUMMARY
Stuypedia is a website specific for Stuyvesant students. This website allows students to view data about their classes and teachers. Data will be from previous students who had the class and filled out the google form survey. Students can also access a calendar with a task manager.

## PROBLEM BEING SOLVED
Talos, Jupiter, Gmails, Facebook Groups, Rate My teacher, Google Classroom, it's all too much! Stuypedia is cartered to the student in order to make the unnecessary part of the student life as smooth as possible.

## TARGET USERS
- Mainly Stuyvesant high school students
- maybe teachers if they want to see what students think about them.

## WHY THIS PROJECT MATTERS
This project is important because students already have a hard life so we want to make the inconvient and downright annoying part of their life easier. 

# MVP SCOPE

## CORE FEATURES
1. Register & Login
2. Calendar & Task Manager
3. Event & Test Adding
4. View Teacher Ratings
   
## STRETCH FEATURES
1. Study resource uploads
2. Better authentication

## EXPLICIT NON-GOALS
1. AI usage
---
# TECHNOLOGY STACK

| Layer | Selected Tool |
|---|---|
| Backend Framework | Flask |
| Frontend Framework | none |
| Database | SQLite |
| Authentication | Flask sessions unless you have good reason/need to deviate |
### WHY THIS STACK WAS CHOSEN
Our team is familiar with these tools and they are sufficient enough to get the task done. 

---

# TEAM OWNERSHIP PLAN
| Team Member | Primary Ownership | Secondary Ownership | Specific Deliverables |
|---|---|---|---|
|Natalie |  Back-end development | Data management | working calendar, collection of data |
|Sophia | Front-end development | Data management | aesthetically pleasing pages |
|Michelle | Back-end development | Front-end development | task adding/removal  |

---
# COMPONENT MAP
MERMAID

# SITE MAP
```
Login / Register
   ↓
Dashboard
   ├── Calender
   ├── Find your Class
       └── [Class] Rating
           └── Teacher Ratings
       └── Student Input Data Page
   ├── Resources Link
   └── Profile
```

# KEY USER STORIES
### eg0
As a __________, I want to __________ so that...

### eg1
As a __________, I want to __________ so that...

### Sophia
As a Stuy student, I want to create a platform so that students can conveniently access all the materials they need in one place.  


# DATA DESIGN
Part of our project is the collection and use of data. To ensure security for students’ accounts, we will hash passwords and store everything under an anonymous username tied to their true username (NYCDOE user).

| key  | type |  notes    |
|-------|-----|-------|
| user | TEXT  | must be unique |
| pass   | TEXT  | will be stored as a hash   |
| anon_user | TEXT  | anonymous username generated for users to be displayed |
| id (PK) | INTEGER  | must be unique |

In order to verify a user, they must answer a series of stuy-related questions (for now, subject to change) Once verified, a student is given an anonymous username (like on Piazza) but their login remains their NYCDOE user and chosen password.

Reviews for classes will be stored by review ID.

| key | type | notes |
|----|-------|------|
| id | INTEGER | PK, unique |
| class | TEXT | |
| teacher | TEXT | |
| user | TEXT | original username of user |
| homework | INTEGER | 1-5 rating of how long homework took |
| test | INTEGER | 1-5 rating of test difficulty |
| workload | INTEGER | 1-5 rating of workload |
| enjoyment | INTEGER | 1-5 rating of class enjoyment |

Events will be stored as such:

| key | type | notes |
|----|------|----|
| id | INTEGER | PK, unique |
| name | TEXT | |
| date | TEXT | stored as DD-MM-YYYY HH-MM-SS |
| description | TEXT | | 
| class | INTEGER | 0 if no associated class |
| teacher | INTEGER | 0 if no associated teacher |
| type | TEXT | "test", "project", "meeting", etc. |


# TESTING PLAN
We will test the register and login component by crating an account and logging on. We will test the calendar feature by creating, detailing, viewing, moving, and deleting tasks. We will test the teacher profile feature by viewing if the teachers have all the correct information on their page. 

# Timeline
## Week 1 Goals: 
- Get the bare minimum skeleton of the website working (5/15)
## Week 2 Goals: 
- Complete the core features and debug (5/22)
## Week 3 Goals: 
- Polish the website and fix and bugs (5/29)
## Internal Deadlines: 
-Record video demoing the product on May 29


# Completion Criteria (_a.k.a._ "Definition of 'Done'")
Project is considered complete when all of the following are true:
1. User can create accounts and login
1. User can create, delete, and move tasks on their calendar
1. User can view the gallery of teachers and their profiles with all the class information on them

# Open Questions
* How do we more thoroughly authenticate users?
* Do we have admin? If not, how do we ensure appropriate behavior by students?

# Appendix
{Any relevant info that is useful but would have interrupted narrative flow above, or cluttered the information portrayed}

# Other: Specific Component Details

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


## CALENDAR

The calendar will be student-managed. Students can select whether the day is an A or B day and which type as well as what time schedule the day has. In addition to that, students can create **events** in categories such as test, project due date, AP, and celebration. Students will be able to verify other users' events or report them if they are innacurate. All students will be able to view the collective calendar and filter it for which classes they want to view.
