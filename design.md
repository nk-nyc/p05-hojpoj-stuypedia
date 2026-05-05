# TEAM Hojpoj
## ROSTER
Natalie Keiger: PM \
Sophia Chi: Devo \
Michelle Chen: Devo

# OVERVIEW
blah blah

# DATA COLLECTION & SECURITY
Part of our project is the collection and use of data. To ensure security for students’ accounts, we will hash passwords and store everything under an anonymous username tied to their true username (NYCDOE user).

| key  | type |  notes    |
|-------|-----|-------|
| user | TEXT  | must be unique |
| pass   | TEXT  | will be stored as a hash   |
| anon_user | TEXT  | anonymous username generated for users to be displayed |
| id (PK) | INTEGER  | must be unique |

In order to verify a user, we will have them submit an image of their Stuy ID. Admin users will be able to verify those images from their account. Once verified, a student is given an anonymous username (like on Piazza) but their login remains their NYCDOE user and chosen password.
